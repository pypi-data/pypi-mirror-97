from __future__ import annotations

import typing as t
from textwrap import wrap
from warnings import warn

import cv2 as cv
import numpy as np
import pandas as pd
import pyqtgraph as pg
from matplotlib import cm
from matplotlib.pyplot import colormaps
from pyqtgraph import GraphicsScene
from pyqtgraph.Qt import QtWidgets, QtGui, QtCore
from pyqtgraph.graphicsItems.LegendItem import ItemSample
from pyqtgraph.graphicsItems.ScatterPlotItem import drawSymbol
from pyqtgraph.graphicsItems.ViewBox.ViewBoxMenu import ViewBoxMenu
from pyqtgraph.parametertree import Parameter
from typing_extensions import Literal
from numpy.distutils.misc_util import is_sequence

from utilitys.fns import nameFormatter, pascalCaseToTitle, params_flattened, \
  dynamicDocstring, getParamChild
from utilitys.misc import CompositionMixin
from utilitys.typeoverloads import FilePath
from . import params
from .constants import PrjEnums
from .params.prjparam import PrjParam

# Taken directly from https://stackoverflow.com/a/20610786/9463643
# Many things can cause this statement to fail
# noinspection PyBroadException
try:
  from pyqtgraph.Qt import QtWidgets
  from qtconsole.rich_jupyter_widget import RichJupyterWidget
  from qtconsole.inprocess import QtInProcessKernelManager
  from IPython.lib import guisupport

except Exception:
  from pyqtgraph.console import ConsoleWidget
else:

  class ConsoleWidget(RichJupyterWidget):
    """ Convenience class for a live IPython console widget. We can replace the standard banner using the customBanner argument"""
    def __init__(self,text=None,*args,**kwargs):
      if not text is None: self.banner=text
      super().__init__(*args,**kwargs)
      self.kernel_manager = kernel_manager = QtInProcessKernelManager()
      kernel_manager.start_kernel()
      # kernel_manager.kernel.gui = 'qt5'
      self.kernel_client = kernel_client = self._kernel_manager.client()
      kernel_client.start_channels()

      def stop():
        kernel_client.stop_channels()
        kernel_manager.shutdown_kernel()
      self.exit_requested.connect(stop)

      namespace = kwargs.get('namespace', {})
      namespace.setdefault('__console__', self)
      self.pushVariables(namespace)
      parent = kwargs.get('parent', None)
      if parent is not None:
        self.setParent(parent)

    def pushVariables(self,variableDict):
      """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
      self.kernel_manager.kernel.shell.push(variableDict)
    def clearTerminal(self):
      """ Clears the terminal """
      self._control.clear()
    def printText(self,text):
      """ Prints some plain text to the console """
      self._append_plain_text(text)
    def executeCommand(self,command):
      """ Execute a command in the frame of the console widget """
      self._execute(command,False)


class ScrollableErrorDialog(QtWidgets.QDialog):
  def __init__(self, parent: QtWidgets.QWidget=None, notCritical=False,
               msgWithTrace='', msgWithoutTrace=''):
    super().__init__(parent)
    style = self.style()
    self.setModal(True)

    if notCritical:
      icon = style.standardIcon(style.SP_MessageBoxInformation)
      self.setWindowTitle('Information')
    else:
      icon = style.standardIcon(style.SP_MessageBoxCritical)
      self.setWindowTitle('Error')

    self.setWindowIcon(icon)
    verticalLayout = QtWidgets.QVBoxLayout(self)


    scrollArea = QtWidgets.QScrollArea(self)
    scrollArea.setWidgetResizable(True)
    scrollAreaWidgetContents = QtWidgets.QWidget()


    scrollLayout = QtWidgets.QVBoxLayout(scrollAreaWidgetContents)

    # Set to message with trace first so sizing is correct
    msgLbl = QtWidgets.QLabel(msgWithTrace, scrollAreaWidgetContents)
    msgLbl.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse
                                      | QtCore.Qt.TextSelectableByKeyboard)
    msgLbl.setTextFormat(QtCore.Qt.PlainText)
    scrollLayout.addWidget(msgLbl, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
    scrollArea.setWidget(scrollAreaWidgetContents)
    verticalLayout.addWidget(scrollArea)

    btnLayout = QtWidgets.QHBoxLayout()
    ok = QtWidgets.QPushButton('Ok', self)
    toggleTrace = QtWidgets.QPushButton('Toggle Stack Trace', self)
    btnLayout.addWidget(ok)
    btnLayout.addWidget(toggleTrace)
    spacerItem = QtWidgets.QSpacerItem(ok.width(), ok.height(),
                                       QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Minimum)
    ok.clicked.connect(self.close)

    sh = self.sizeHint()
    newWidth = max(sh.width(), self.width())
    newHeight = max(sh.height(), self.height())
    self.resize(newWidth, newHeight)

    showTrace = False
    def updateTxt():
      nonlocal showTrace
      if showTrace:
        newText = msgWithTrace
        msgLbl.setTextFormat(QtCore.Qt.PlainText)
      else:
        newLines = msgWithoutTrace.splitlines()
        allLines = []
        for line in newLines:
          if line == '': line = [line]
          else: line = wrap(line)
          allLines.extend(line)
        newText = '<br>'.join(allLines)
        msgLbl.setTextFormat(QtCore.Qt.RichText)
      showTrace = not showTrace
      msgLbl.setText(newText)

    self.msgLbl = msgLbl
    toggleTrace.clicked.connect(lambda: updateTxt())

    btnLayout.addItem(spacerItem)
    verticalLayout.addLayout(btnLayout)
    self.toggleTrace = toggleTrace
    ok.setFocus()
    updateTxt()

class PopupLineEditor(QtWidgets.QLineEdit):
  def __init__(self, parent: QtWidgets.QWidget=None, model: QtCore.QAbstractItemModel=None,
               placeholderText='Press Tab or type...', clearOnComplete=True,
               forceMatch=True):
    super().__init__(parent)
    self.setPlaceholderText(placeholderText)
    self.clearOnComplete = clearOnComplete
    self.forceMatch = forceMatch

    if model is not None:
      self.setModel(model)

  def setModel(self, model: QtCore.QAbstractListModel):
    completer = QtWidgets.QCompleter(model, self)
    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    completer.setCompletionRole(QtCore.Qt.DisplayRole)
    completer.setFilterMode(QtCore.Qt.MatchContains)
    if self.clearOnComplete:
      completer.activated.connect(lambda: QtCore.QTimer.singleShot(0, self.clear))

    self.textChanged.connect(lambda: self.resetCompleterPrefix())

    self.setCompleter(completer)

  # TODO: Get working with next prev focusing for smoother logic
  # def focusNextPrevChild(self, nextChild: bool):
  #   if self.forceMatch and self.text() not in self.completer().model().stringList():
  #     dummyFocusEv = QtGui.QFocusEvent(QtCore.QEvent.FocusOut)
  #     self.focusOutEvent(dummyFocusEv)
  #     return False
  #   return super().focusNextPrevChild(nextChild)

  def _chooseNextCompletion(self, incAmt=1):
    completer = self.completer()
    popup = completer.popup()
    if popup.isVisible() and popup.currentIndex().isValid():
      nextIdx = (completer.currentRow()+incAmt)%completer.completionCount()
      completer.setCurrentRow(nextIdx)
    else:
      completer.complete()
    popup.show()
    popup.setCurrentIndex(completer.currentIndex())
    popup.setFocus()

  def event(self, ev: QtCore.QEvent):
    if ev.type() != ev.KeyPress:
      return super().event(ev)

    ev: QtGui.QKeyEvent
    key = ev.key()
    if key == QtCore.Qt.Key_Tab:
      incAmt = 1
    elif key == QtCore.Qt.Key_Backtab:
      incAmt = -1
    else:
      return super().event(ev)
    self._chooseNextCompletion(incAmt)
    return True

  def focusOutEvent(self, ev: QtGui.QFocusEvent):
    reason = ev.reason()
    if reason in [QtCore.Qt.TabFocusReason, QtCore.Qt.BacktabFocusReason,
                  QtCore.Qt.OtherFocusReason]:
      # Simulate tabbing through completer options instead of losing focus
      self.setFocus()
      completer = self.completer()
      if completer is None:
        return
      incAmt = 1 if reason == QtCore.Qt.TabFocusReason else -1

      self._chooseNextCompletion(incAmt)
      ev.accept()
      return
    else:
      super().focusOutEvent(ev)

  def clear(self):
    super().clear()

  def resetCompleterPrefix(self):
    if self.text() == '':
      self.completer().setCompletionPrefix('')


class _DEFAULT_OWNER: pass
"""None is a valid owner, so create a sentinel that's not valid"""
btnCallable = t.Callable[[PrjParam], t.Any]
class ButtonCollection(QtWidgets.QGroupBox):
  def __init__(self, parent=None, title: str=None, btnParams: t.Collection[PrjParam]=(),
               btnTriggerFns: t.Union[btnCallable, t.Collection[btnCallable]]=(),
               exclusive=True, asToolBtn=True,
               **createOpts):
    super().__init__(parent)
    self.lastTriggered: t.Optional[PrjParam] = None
    self.uiLayout = QtWidgets.QHBoxLayout(self)
    self.btnGroup = QtWidgets.QButtonGroup(self)
    self.paramToFuncMapping: t.Dict[PrjParam, btnCallable] = dict()
    self.paramToBtnMapping: t.Dict[PrjParam, QtWidgets.QPushButton] = dict()
    self.asToolBtn = asToolBtn
    if title is not None:
      self.setTitle(title)
    self.btnGroup.setExclusive(exclusive)

    if not isinstance(btnTriggerFns, t.Iterable):
      btnTriggerFns = [btnTriggerFns]*len(btnParams)
    for param, fn in zip(btnParams, btnTriggerFns):
      self.create_addBtn(param, fn, **createOpts)

  def create_addBtn(self, btnParam: PrjParam, triggerFn: btnCallable, checkable=False, **createOpts):
    if btnParam in self.paramToBtnMapping:
      # Either already exists or wasn't designed to be a button
      return
    createOpts.setdefault('asToolBtn', self.asToolBtn)
    newBtn = self.createBtn(btnParam, **createOpts)
    if checkable:
      newBtn.setCheckable(True)
      oldTriggerFn = triggerFn
      # If the button is checkable, only call this function when the button is checked
      def newTriggerFn(param: PrjParam):
        if newBtn.isChecked():
          oldTriggerFn(param)
      triggerFn = newTriggerFn
    newBtn.clicked.connect(lambda: self.callFuncByParam(btnParam))

    self.addBtn(btnParam, newBtn, triggerFn)
    return newBtn

  def clear(self):
    for button in self.paramToBtnMapping.values():
      self.btnGroup.removeButton(button)
      self.uiLayout.removeWidget(button)
      button.deleteLater()

    self.paramToBtnMapping.clear()
    self.paramToFuncMapping.clear()

  def addFromExisting(self, other: ButtonCollection, which: t.Collection[PrjParam]=None):
    for (param, btn), func in zip(other.paramToBtnMapping.items(), other.paramToFuncMapping.values()):
      if which is None or param in which:
        self.addBtn(param, btn, func)

  def addBtn(self, param: PrjParam, btn: QtWidgets.QPushButton, func: btnCallable):
    self.btnGroup.addButton(btn)
    self.uiLayout.addWidget(btn)
    self.paramToFuncMapping[param] = func
    self.paramToBtnMapping[param] = btn

  @classmethod
  def createBtn(cls, btnOpts: PrjParam, baseBtn: QtWidgets.QAbstractButton=None, asToolBtn=False,
                parent=None, **kwargs):
    if asToolBtn:
      btnType = QtWidgets.QToolButton
    else:
      btnType = QtWidgets.QPushButton
    tooltipText = btnOpts.helpText
    if baseBtn is not None:
      newBtn = baseBtn
    else:
      newBtn = btnType(parent)
      newBtn.setText(btnOpts.name)
    if 'icon' in btnOpts.opts:
      newBtn.setText('')
      newBtn.setIcon(QtGui.QIcon(str(btnOpts.opts['icon'])))
      tooltipText = btnOpts.addHelpText(btnOpts.name)
    newBtn.setToolTip(tooltipText)
    reg = params.pgregistered.ShortcutParameter.REGISTRY
    if reg is not None:
      reg.registerButton(btnOpts, newBtn, **kwargs)
    return newBtn

  def callFuncByParam(self, param: PrjParam):
    if param is None:
      return
    # Ensure function is called in the event it requires a button to be checked
    btn = self.paramToBtnMapping[param]
    if btn.isCheckable():
      btn.setChecked(True)
    self.paramToFuncMapping[param](param)
    self.lastTriggered = param

  def addByParam(self, param: Parameter, copy=True, **registerOpts):
    """
    Adds a button to a group based on the parameter. Also works for group params
    that have an acttion nested.
    """
    for param in params_flattened(param):
      curCopy = copy
      if param.type() in ['action', 'shortcut'] and param.opts.get('guibtn', True):
        existingBtn = None
        try:
          existingBtn = next(iter(param.items)).button
        except (StopIteration, AttributeError):
          curCopy = True
        if curCopy:
          self.create_addBtn(PrjParam(**param.opts), lambda *args: param.activate(),
                             **registerOpts)
        else:
          self.addBtn(PrjParam(**param.opts), existingBtn, existingBtn.click)

  @classmethod
  def fromToolsEditors(cls,
                       editors: t.Sequence[params.ParamEditor],
                       title='Tools',
                       ownerClctn: ButtonCollection=None,
                       **registerOpts):
    if ownerClctn is None:
      ownerClctn = cls(title=title, exclusive=True)

    for editor in editors:
      ownerClctn.addByParam(editor.params, **registerOpts)

    return ownerClctn

  def toolbarFormat(self):
    """
    Returns a list of buttons + title in a format that's easier to add to a toolbar, e.g.
    doesn't require as much horizontal space
    """
    title = self.title()
    out: t.List[QtWidgets.QWidget] = [] if title is None else [QtWidgets.QLabel(self.title())]
    for btn in self.paramToBtnMapping.values():
      out.append(btn)
    return out

_layoutTypes = t.Union[Literal['H'], Literal['V']]
class EasyWidget:
  def __init__(self, children: t.Sequence[t.Union[QtWidgets.QWidget, EasyWidget]],
               layout: str=None, useSplitter=False, baseWidget: QtWidgets.QWidget=None):
    if baseWidget is None:
      baseWidget = QtWidgets.QWidget()
    self.children_ = children
    self.useSplitter = useSplitter
    if layout == 'V':
      orient = QtCore.Qt.Vertical
      layout = QtWidgets.QVBoxLayout
    elif layout == 'H':
      orient = QtCore.Qt.Horizontal
      layout = QtWidgets.QHBoxLayout
    else:
      orient = layout = None
    self.orient_ = orient

    if useSplitter:
      self.layout_ = QtWidgets.QSplitter(orient)
      self.widget_ = self.layout_
    else:
      self.widget_ = baseWidget
      try:
        self.layout_ = layout()
        self.widget_.setLayout(self.layout_)
      except TypeError:
        # When win is none
        self.layout_ = None

  def build(self):
    if self.layout_ is None:
      raise ValueError('Top-level orientation must be set to "V" or "H" before adding children')
    if self.orient_ == QtCore.Qt.Horizontal:
      chSuggested = 'V'
    elif self.orient_ == QtCore.Qt.Vertical:
      chSuggested = 'H'
    else:
      chSuggested = None

    for ii, child in enumerate(self.children_):
      self.addChild(child, chSuggested)

  def addChild(self, child: t.Union[QtWidgets.QWidget, t.Sequence, EasyWidget], suggestedLayout:str=None):
    if isinstance(child, QtWidgets.QWidget):
      self.layout_.addWidget(child)
    else:
      child = self.listChildrenWrapper(child, suggestedLayout)
      # At this point, child should be an EasyWidget
      child.build()
      self.layout_.addWidget(child.widget_)

  @classmethod
  def listChildrenWrapper(cls, children: t.Union[t.Sequence, EasyWidget], maybeNewLayout: str=None):
    if not isinstance(children, EasyWidget):
      children = cls(children)
    if children.layout_ is None and maybeNewLayout is not None:
      children = cls(children.children_, maybeNewLayout, children.useSplitter)
    return children

  @classmethod
  def buildMainWin(cls, children: t.Union[t.Sequence, EasyWidget], win: QtWidgets.QMainWindow=None, layout='V', **kwargs):
    if win is None:
      win = QtWidgets.QMainWindow()
    if isinstance(children, t.Sequence):
      children = cls(children, layout=layout, **kwargs)

    children.build()
    win.easyChild = children
    win: HasEasyChild
    win.setCentralWidget(children.widget_)
    return win

  @classmethod
  def buildWidget(cls, children: t.Union[t.Sequence, EasyWidget], layout='V', **kwargs):
    builder = cls(children, layout=layout, **kwargs)
    builder.build()
    retWidget: HasEasyChild = builder.widget_
    retWidget.easyChild = builder
    return retWidget

class HasEasyChild(QtWidgets.QMainWindow):
  """Provided just for type checking purposes"""
  easyChild: EasyWidget


class ImageViewer(CompositionMixin, pg.PlotWidget):
  sigMouseMoved = QtCore.Signal(object) # ndarray(int, int) xy pos rel. to image

  def __init__(self, imgSrc: np.ndarray=None, **kwargs):
    super().__init__(**kwargs)
    self.pxColorLbl, self.mouseCoordsLbl = None, None
    """
    Set these to QLabels to have up-to-date information about the image coordinates
    under the mouse    
    """
    self.toolsEditor = params.ParamEditor(name='Region Tools')
    vb = self.getViewBox()
    self.menu: QtWidgets.QMenu = vb.menu
    self.menu.clear()
    self.oldVbMenu: ViewBoxMenu = vb.menu
    # Disable default menus
    self.plotItem.ctrlMenu = None
    self.sceneObj.contextMenu = None

    self.setAspectLocked(True)
    vb.invertY()

    # -----
    # IMAGE
    # -----
    self.imgItem = self.exposes(pg.ImageItem())
    self.imgItem.setZValue(-100)
    self.addItem(self.imgItem)
    if imgSrc is not None:
      self.setImage(imgSrc)

  def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
    super().mouseMoveEvent(ev)
    pos = ev.pos()
    relpos = self.imgItem.mapFromScene(pos)
    xyCoord = np.array([relpos.x(), relpos.y()], dtype=int)
    if (self.imgItem.image is None
        or np.any(xyCoord < 0)
        or np.any(xyCoord > np.array(self.imgItem.image.shape[:2][::-1]) - 1)):
      return
    imgValue = self.imgItem.image[xyCoord[1], xyCoord[0],...].astype(int)
    self.updateCursorInfo(xyCoord, imgValue)
    self.sigMouseMoved.emit(xyCoord)

  def updateCursorInfo(self, xyPos: np.ndarray, pxValue: np.ndarray):
    if pxValue is None: return
    if self.mouseCoordsLbl is not None:
      self.mouseCoordsLbl.setText(f'Mouse (x,y): {xyPos[0]}, {xyPos[1]}')

    if self.pxColorLbl is None:
      return
    self.pxColorLbl.setText(f'Pixel Color: {pxValue}')
    if self.imgItem.qimage is None:
      return
    # Cheap way of splitting the int32 return value into uint8 RGBA
    imColor = np.array([self.imgItem.qimage.pixel(*xyPos)], 'uint32').view('uint8')
    grayClr = np.mean(imColor[:3])
    fontColor = 'black' if grayClr > 127 else 'white'
    self.pxColorLbl.setStyleSheet(f'background:rgba{tuple(imColor)}; color:{fontColor}')

  def setImage(self, imgSrc: t.Union[FilePath, np.ndarray]=None):
    """
    Allows the user to change the main image either from a filepath or array data
    """
    if isinstance(imgSrc, FilePath.__args__):
      # TODO: Handle alpha channel images. For now, discard that data
      imgSrc = cv.imread(str(imgSrc), cv.IMREAD_UNCHANGED)
      if imgSrc.ndim > 3:
        # Alpha channels cause unexpected results for most image processors. Avoid this
        # by chopping it off until otherwise needed
        imgSrc = imgSrc[:,:,0:3]
      if imgSrc.ndim == 3:
        imgSrc = cv.cvtColor(imgSrc, cv.COLOR_BGR2RGB)

    if imgSrc is None:
      self.imgItem.clear()
    else:
      self.imgItem.setImage(imgSrc)

  def widgetContainer(self, asMainWin=True, showTools=True, **kwargs):
    """
    Though this is a PlotWidget class, it has a lot of widget children (toolsEditor group, buttons) that are
    not visible when spawning the widget. This is a convenience method that creates a new, outer widget
    from all teh graphical elements of an EditableImage.

    :param asMainWin: Whether to return a QMainWindow or QWidget
    :param showTools: If `showMainWin` is True, this determines whether to show the tools
      editor with the window
    :param kwargs: Passed to either EasyWidget.buildMainWin or EasyWidget.BuildWidget,
      depending on the value of `asMainWin`
    """
    if asMainWin:
      wid = EasyWidget.buildMainWin(self._widgetContainerChildren(), **kwargs)
      self.mouseCoordsLbl = QtWidgets.QLabel()
      self.pxColorLbl = QtWidgets.QLabel()
      wid.statusBar().addWidget(self.mouseCoordsLbl)
      wid.statusBar().addWidget(self.pxColorLbl)
      wid.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.toolsEditor)
      if showTools:
        self.toolsEditor.show()
    else:
      wid = EasyWidget.buildWidget(self._widgetContainerChildren(), **kwargs)
    return wid

  def show_exec(self):
    win = self.widgetContainer(True)
    QtCore.QTimer.singleShot(0, win.showMaximized)
    QtCore.QCoreApplication.instance().exec_()


  def _widgetContainerChildren(self):
    """
    Returns the children that should be added to the container when widgetContainer()
    is called
    """
    return [self]

class CompositorItemSample(ItemSample):
  def paint(self, p: QtGui.QPainter, *args):
    opts = self.item.opts

    if opts.get('antialias'):
      p.setRenderHint(p.Antialiasing)
    symbol = opts.get('symbol', None)
    p.translate(0, 14)
    drawSymbol(p, symbol, opts['size'], pg.fn.mkPen(opts['pen']),
               pg.fn.mkBrush(opts['brush']))

class CompositorLegend(pg.LegendItem):

  def paint(self, p: QtGui.QPainter, *args):
    br = self.boundingRect()
    p.setPen(self.opts['pen'])
    p.setBrush(self.opts['brush'])
    p.drawRoundedRect(br, 5, 5)

class MaskCompositor(ImageViewer):
  def __init__(self, img: np.ndarray=None):
    super().__init__()
    # -----
    # Create properties
    # -----
    self.legend = CompositorLegend(offset=(5,5), horSpacing=5, brush='ccce', pen='k')

    self.recordDf = pd.DataFrame(columns=['name', 'item', 'scatter', 'opacity']).set_index('name')

    self.legendFontArgs = {'size': '11pt', 'color': 'k', 'bold': True}
    self.curZ = 2

    # -----
    # Configure relationships
    # -----
    self.legend.setParentItem(self.plotItem)
    self.viewbox: pg.ViewBox = self.getViewBox()

    self.masksParam = getParamChild(self.toolsEditor.params, 'Overlays')
    self.allVisible = True
    # for ax in 'left', 'bottom', 'right', 'top':
    #   self.mainImg.plotItem.hideAxis(ax)
    # self.mainImg.setContentsMargins(0, 0, 0, 0)
    def newFmt(name):
      if name.startswith('set'):
        name = name.replace('set', '')
      name = pascalCaseToTitle(name)
      return name
    with nameFormatter.set(newFmt):
      self.toolsEditor.registerFunc(self.setOverlayProperties, runOpts=params.RunOpts.ON_CHANGED)
      self.toolsEditor.registerFunc(self.save)
      self.toolsEditor.registerFunc(lambda: self.imgItem.setVisible(not self.imgItem.isVisible()),
                                    name='Toggle Image Visible')
      self.toolsEditor.registerFunc(lambda: self.legend.setVisible(not self.legend.isVisible()),
                                    name='Toggle Legend Visible')
      self.toolsEditor.registerFunc(self.toggleAllVisible, namePath=('Overlays',))
    if img is not None:
      self.setImage(img)

  def _addItemCtrls(self, record: pd.Series):
    item = record['item']
    def maskOpts(_, visible=True):
      item.setVisible(visible)
    newParam = getParamChild(self.masksParam,
                             chOpts={'name': record.name, 'type': 'bool', 'value': True})
    newParam.sigValueChanged.connect(maskOpts)

  def setBaseImage(self, baseImg: np.ndarray, clearOverlays=True):
    # self.winSz = baseImg.shape[:2][::-1]
    # self.viewbox.setRange(
    #   xRange=[0, imgItem.shape[1]], yRange=[0, imgItem.shape[0]], padding=0
    # )
    self.setImage(baseImg)
    # self.refreshWinContents()
    if clearOverlays:
      self.clearOverlays()

  def setImage(self, *args, **kwargs):
    super().setImage(*args, **kwargs)
    self._updateLegendPos()


  def addMask(self, mask: np.ndarray, name:str=None, ignoreIfBlank=False, update=True):
    if ignoreIfBlank and not np.any(mask):
      return
    newRecord = {}

    name = self._getUniqueName(name)

    curScat = pg.ScatterPlotItem(symbol='s', width=5)
    self.legend.addItem(CompositorItemSample(curScat), name=name)
    newRecord['scatter'] = curScat

    toAdd = pg.ImageItem(mask)
    toAdd.setZValue(self.curZ + 1)
    self.viewbox.addItem(toAdd)
    newRecord['item'] = toAdd

    newRecord['opacity'] = -1

    rec = pd.Series(newRecord, name=name)
    self._addRecord(rec, update)
    return rec

  def _addRecord(self, rec: pd.Series, update=True):
    self.recordDf = self.recordDf.append(rec)
    self.curZ += 1

    self._addItemCtrls(rec)

    if update:
      self._updateGraphics()

  def addImageItem(self, item: pg.ImageItem, **kwargs):
    kwargs.setdefault('scatter', None)
    kwargs.setdefault('opacity', -1)
    name = self._getUniqueName(kwargs.pop('name', None))
    update = kwargs.pop('update', True)
    newRecord = dict(item=item, **kwargs)

    item.setZValue(self.curZ + 1)
    self.viewbox.addItem(item)

    rec = pd.Series(newRecord, name=name)
    self._addRecord(rec, update)

  def addMasks(self, masks: t.List[np.ndarray], names: t.Sequence[t.Optional[str]]=None, ignoreIfBlank=False):
    if names is None:
      names = [None]*len(masks)
    for mask, name in zip(masks, names):
      self.addMask(mask, name, ignoreIfBlank, update=False)
    self._updateGraphics()

  def _getUniqueName(self, baseName:str=None):
    if baseName is None:
      baseName = '[No Name]'
    ii = 2
    name = baseName
    while name in self.recordDf.index:
      name = f'{baseName} {ii}'
      ii += 1
    return name

  def addLabelImg(self, labelImg: np.ndarray, names='Label', ignoreBackground=True):
    """
    Splits a label mask into its constituent labels and adds a mask for each unique label.

    :param labelImg: Grayscale label mask of integers
    :param names: Base name of each label. E.g. if 3 labels are present in the image, the
      resulting masks will be named <name> 1, <name> 2, <name 3>. Alternatively,
      a list of names can be provided
    :param ignoreBackground: Whether a mask should be added for 0-valued labels (typically
      0 is used to denote background / non-label values)
    """
    labels = np.unique(labelImg)
    if ignoreBackground:
      labels = labels[labels > 0]
    newMasks = [labelImg == label for label in labels]
    if not is_sequence(names):
      names = [f'{names} {ii}' for ii in labels]
    self.addMasks(newMasks, names)


  def setLegendFontStyle(self, startItemIdx=0, **lblTxtArgs):
    for item in self.legend.items[startItemIdx:]:
      for single_item in item:
        if isinstance(single_item, pg.LabelItem):
          single_item.setText(single_item.text, **lblTxtArgs)

  @dynamicDocstring(cmapVals=colormaps())
  def setOverlayProperties(self, colormap='Set1', opacity=0.5):
    """
    Sets overlay properties
    :param colormap:
      pType: popuplineeditor
      limits: {cmapVals}
    :param opacity:
      limits: [0,1]
      step: 0.1
    """
    maskNames = np.array([s is not None for s in self.recordDf['scatter']])
    names = self.recordDf.index[maskNames]
    numMasks = len(names)
    cmap = cm.get_cmap(colormap, numMasks)
    colors = cmap(np.arange(numMasks))
    colors = (colors*255).astype('uint8')
    backgroundClr = [0,0,0,0]
    # Filter out names without associated scatters
    for name, color in zip(names, colors):
      # Make sure alpha is not carried over
      brush, pen = pg.mkBrush(color), pg.mkPen(color)
      self.recordDf.at[name, 'scatter'].setData(symbol='s', brush=brush, pen=pen, width=5)
    for name, color in zip(names, colors):
      curLut = np.array([backgroundClr, color])
      itemOpacity = self.recordDf.at[name, 'opacity']
      if itemOpacity < 0:
        itemOpacity = opacity
      self.recordDf.at[name, 'item'].setOpts(levels=[0,1], lut=curLut, opacity=itemOpacity)
    self.setLegendFontStyle(**self.legendFontArgs)

    # Handle all non-mask items now
    for name, remainingRec in self.recordDf[~maskNames].iterrows():
      curOpacity = remainingRec['opacity']
      if curOpacity < 0:
        curOpacity = opacity
      remainingRec['item'].setOpacity(curOpacity)

  def _updateLegendPos(self):
    imPos = self.imgItem.mapToScene(self.imgItem.pos())
    self.legend.autoAnchor(imPos)

  def _updateGraphics(self):
    self.setOverlayProperties()

  def clearOverlays(self):
    for imgItem in self.recordDf['item']:
      self.viewbox.removeItem(imgItem)
    self.recordDf = self.recordDf.drop(self.recordDf.index)
    self.legend.clear()
    self.toolsEditor.params.child('Overlays').clearChildren()

  def toggleAllVisible(self):
    for param in self.masksParam:
      if param.type() == 'bool':
        param.setValue(not self.allVisible)
    self.allVisible = not self.allVisible

  def save(self, saveFile: FilePath='', cropToViewbox=False, toClipboard=False, floatLegend=False) -> bool:
    """
    :param saveFile:
      helpText: Save destination. If blank, no file is created.
      existing: False
      pType: filepicker
    :param toClipboard: Whether to copy to clipboard
    :param cropToViewbox: Whether to only save the visible portion of the image
    :param floatLegend: Whether to ancor the legend in the top-left corner (if *False*) or
      put it exactly where it is positioned currently (if *True*). In the latter case, it may not appear if out of view
      and `cropToViewbox` is *True*.
    """
    if self.imgItem.isVisible():
      saveImg = self.imgItem.getPixmap()
    else:
      saveImg = QtGui.QPixmap(*self.imgItem.image.shape[:2][::-1])
    painter = QtGui.QPainter(saveImg)

    visibleMasks = [p.name() for p in params_flattened(self.masksParam) if p.value()]
    for name, item in self.recordDf['item'].iteritems():
      if name in visibleMasks:
        painter.setOpacity(item.opacity())
        item.paint(painter)
    painter.setOpacity(1.0)

    if cropToViewbox:
      maxBnd = np.array(self.image.shape[:2][::-1]).reshape(-1,1) - 1
      vRange = np.array(self.viewbox.viewRange()).astype(int)
      vRange = np.clip(vRange, 0, maxBnd)
      # Convert range to topleft->bottomright
      pts = QtCore.QPoint(*vRange[:,0]), QtCore.QPoint(*vRange[:,1])
      # Qt doesn't do so well overwriting the original reference
      origRef = saveImg
      saveImg = origRef.copy(QtCore.QRect(*pts))
      painter.end()
      painter = QtGui.QPainter(saveImg)
    if self.legend.isVisible():
      # Wait to paint legend until here in case cropping is active
      self._paintLegend(painter, floatLegend)

    if toClipboard:
      QtWidgets.QApplication.clipboard().setImage(saveImg.toImage())

    saveFile = str(saveFile)
    if saveFile and not saveImg.save(str(saveFile)):
      warn('Image compositor save failed', UserWarning)
    return saveImg


  def _paintLegend(self, painter: QtGui.QPainter, floatLegend=False):
    oldPos = self.legend.pos()
    try:
      exportScene = GraphicsScene(parent=None)
      oldScale = max(np.clip(0.5/np.array(self.imgItem.pixelSize()), 1, np.inf))
      exportScene.addItem(self.legend)
      self.legend.setScale(oldScale)
      # Legend does not scale itself, handle this
      painter.save()
      if floatLegend:
        viewPos = self.viewbox.viewRect()
        viewX = max(viewPos.x(), 0)
        viewY = max(viewPos.y(), 0)
        imPos = self.legend.mapRectToItem(self.imgItem, self.legend.rect())
        painter.translate(int(imPos.x() - viewX), int(imPos.y() - viewY))
      exportScene.render(painter)
      self.legend.setScale(1/oldScale)
      painter.restore()
    finally:
      self.legend.setParentItem(self.plotItem)
      self.legend.autoAnchor(oldPos, relative=False)

class PandasTableModel(QtCore.QAbstractTableModel):
  """
  Class to populate a table view with a pandas dataframe
  """
  sigDataChanged = QtCore.Signal(object)
  defaultEmitDict = {'deleted': np.array([]), 'changed': np.array([]), 'added': np.array([])}

  # Will be set in 'changeDefaultRows'
  df: pd.DataFrame
  _defaultSer: pd.Series

  def __init__(self, defaultSer: pd.Series, parent=None):
    super().__init__(parent)
    self.changeDefaultRows(defaultSer)
    self._nextRowId = 0

  def rowCount(self, parent=None):
    return self.df.shape[0]

  def columnCount(self, parent=None):
    return self.df.shape[1]

  def data(self, index, role=QtCore.Qt.DisplayRole):
    if index.isValid():
      value = self.df.iloc[index.row(), index.column()]
      if role == QtCore.Qt.DisplayRole:
        return str(value)
      elif role == QtCore.Qt.EditRole:
        return value
    return None

  def setData(self, index: QtCore.QModelIndex, value: t.Any, role:int=QtCore.Qt.ItemDataRole) -> bool:
    super().setData(index, role)
    row = index.row()
    col = index.column()
    oldVal = self.df.iat[row, col]
    # Try-catch for case of numpy arrays
    noChange = oldVal == value
    try:
      if noChange:
        return True
    except ValueError:
      # Happens with array comparison
      pass
    self.df.iat[row, col] = value
    self.sigDataChanged.emit()
    return True

  def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
    if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
      return self.df.columns[section]

  def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
    return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

  def addDfRows(self, rowData: pd.DataFrame, addType = PrjEnums.ADD_TYPE_NEW, emitChange=True):
    toEmit = self.defaultEmitDict.copy()
    if addType == PrjEnums.ADD_TYPE_NEW:
      # Treat all comps as new -> set their IDs to guaranteed new values
      newIds = np.arange(self._nextRowId, self._nextRowId + len(rowData), dtype=int)
      rowData.set_index(newIds, inplace=True, verify_integrity=False)
      # For new data without all columns, add missing values to ensure they're correctly filled
      if np.setdiff1d(rowData.columns, self.df.columns).size > 0:
        rowData = self.makeDefaultDfRows(len(rowData), rowData)
    else:
      # Merge may have been performed with new comps (id -1) mixed in
      needsUpdatedId = rowData.index == -1
      newIds = np.arange(self._nextRowId, self._nextRowId + np.sum(needsUpdatedId), dtype=int)
      rowData.index[needsUpdatedId] = newIds

    # Merge existing IDs and add new ones
    changedIdxs = np.isin(rowData.index, self.df.index, assume_unique=True)
    changedIds = rowData.index[changedIdxs]
    addedIds = rowData.index[~changedIdxs]

    # Signal to table that rows should change
    self.layoutAboutToBeChanged.emit()
    # Ensure indices overlap with the components these are replacing
    self.df.update(rowData)
    toEmit['changed'] = changedIds

    # Finally, add new comps
    compsToAdd = rowData.loc[addedIds]
    self.df = pd.concat((self.compDf, compsToAdd), sort=False)
    toEmit['added'] = addedIds

    # Retain type information
    self._coerceDfTypes()

    self.layoutChanged.emit()

    self._nextRowId = np.max(self.compDf.index.to_numpy(), initial=-1) + 1

    if emitChange:
      self.sigCompsChanged.emit(toEmit)
    return toEmit

  def removeDfRows(self, idsToRemove: t.Sequence[int], emitChange=True):
    toEmit = self.defaultEmitDict.copy()
    # Generate ID list
    existingCompIds = self.compDf.index
    idsToRemove = np.asarray(idsToRemove)

    # Do nothing for IDs not actually in the existing list
    idsActuallyRemoved = np.isin(idsToRemove, existingCompIds, assume_unique=True)
    if len(idsActuallyRemoved) == 0:
      return toEmit
    idsToRemove = idsToRemove[idsActuallyRemoved]

    tfKeepIdx = np.isin(existingCompIds, idsToRemove, assume_unique=True, invert=True)

    # Reset manager's component list
    self.layoutAboutToBeChanged.emit()
    self.df = self.df.iloc[tfKeepIdx, :]
    self.layoutChanged.emit()

    # Preserve type information after change
    self._coerceDfTypes()

    # Determine next ID for new components
    self._nextRowId = 0
    if np.any(tfKeepIdx):
      self._nextRowId = np.max(existingCompIds[tfKeepIdx].to_numpy()) + 1

    # Reflect these changes to the component list
    toEmit['deleted'] = idsToRemove
    if emitChange:
      self.sigCompsChanged.emit(toEmit)

  def makeDefaultDfRows(self, numRows=1, initData: pd.DataFrame=None):
    """
    Create a dummy table populated with default values from the class default pd.Series. If `initData` is provided, it
    must have numRows entries and correspond to columns from the default series. these columns will be overridden by
    the init data.
    """
    if numRows == 0:
      return pd.DataFrame(columns=self._defaultSer.index)
    outDf = pd.DataFrame([self._defaultSer] * numRows)
    if initData is not None:
      outDf.update(initData.set_index(outDf.index))
    return outDf

  def changeDefaultRows(self, defaultSer: pd.Series):
    self.beginResetModel()
    self._defaultSer = defaultSer
    self.removeDfRows(self.df.index)
    self.df = self.makeDefaultDfRows(0)
    self.endResetModel()

  def _coerceDfTypes(self):
    """
    Pandas currently has a bug where datatypes are not preserved after update operations.
    Current workaround is to coerce all types to their original values after each operation
    """
    for ii, col in enumerate(self.df.columns):
      idealType = type(self._defaultSer[col])
      if not np.issubdtype(self.df.dtypes[ii], idealType):
        try:
          self.df[col] = self.df[col].astype(idealType)
        except (TypeError, ValueError):
          continue