import typing as t
import weakref
from contextlib import contextmanager
from enum import Flag, auto
from pathlib import Path
from warnings import warn

from pyqtgraph.Qt import QtCore, QtWidgets
from pyqtgraph.parametertree import Parameter
from pyqtgraph.parametertree.parameterTypes import GroupParameter

from . import PrjParam
from .procwrapper import NestedProcWrapper
from .. import fns
from ..processing import *
from ..typeoverloads import FilePath
import utilitys
from ..fns import warnLater

__all__ = [
  'RunOpts', 'ParamEditor', 'ParamEditorDockGrouping', 'EditorPropsMixin', 'SPAWNED_EDITORS'
]

Signal = QtCore.Signal

class RunOpts(Flag):
  NONE = 0
  BTN = auto()
  ON_CHANGED = auto()
  ON_CHANGING = auto()
  ON_APPLY = auto()

def _mkRunDict(proc: ProcessStage, btnOpts: t.Union[PrjParam, dict]):
  defaultBtnOpts = dict(name=proc.name, type='shortcut')
  if isinstance(btnOpts, PrjParam):
    # Replace falsy helptext with func signature
    btnOpts = btnOpts.toPgDict()
  if btnOpts is not None:
    # Make sure param type is not overridden
    btnOpts.pop('type', None)
    defaultBtnOpts.update(btnOpts)
  if len(defaultBtnOpts.get('tip', '')) == 0 and isinstance(proc, AtomicProcess):
    defaultBtnOpts['tip'] = fns.docParser(proc.func.__doc__)['top-descr']
  if len(proc.input.hyperParamKeys) > 0:
    # In this case, a descriptive name isn't needed since the func name will be
    # present in the parameter group
    defaultBtnOpts['name'] = 'Run'
  return defaultBtnOpts


"""
Eventually, it would be nice to implemenet a global search bar that can find/modify
any action, shortcut, etc. from any parameter. This tracker is an easy way to fascilitate
such a feature. A `class:FRPopupLineEditor` can be created with a model derived from
all parameters from SPAWNED_EDITORS, thereby letting a user see any option from any
param editor.
"""

class ParamEditor(QtWidgets.QDockWidget):
  sigParamStateCreated = Signal(str)
  sigChangesApplied = Signal(dict)
  sigParamStateDeleted = Signal(str)

  _baseRegisterPath: t.Sequence[str] = ()
  """
  Classes typically register all their properites in bulk under the same group of
  parameters. This property will be overridden (see :meth:`setBaseRegisterPath`) by
  the class name of whatever class is currently registering properties.
  """

  def __init__(self, parent=None, paramList: t.List[t.Dict] = None, saveDir: FilePath=None,
               fileType='param', name=None, topTreeChild: Parameter = None,
               **kwargs):
    """
    GUI controls for user-interactive parameters within a QtWidget (usually main window). Each window consists of
    a parameter tree and basic saving capabilities.

    :param parent: GUI parent of this window
    :param paramList: User-editable parameters. This is often *None* and parameters
      are added dynamically within the code.
    :param saveDir: When "save" is performed, the resulting settings will be saved
      here.
    :param fileType: The filetype of the saved settings. E.g. if a settings configuration
      is saved with the name "test", it will result in a file "test.&lt;fileType&gt;"
    :param name: User-readable name of this parameter editor
    :param topTreeChild: Generally for internal use. If provided, it will
      be inserted into the parameter tree instead of a newly created parameter.
    """
    super().__init__(parent)
    self.hide()
    cls = type(self)
    # Place in list so an empty value gets unpacked into super constructor
    if paramList is None:
      paramList = []
    if name is None:
      name = fns.nameFormatter(fns.clsNameOrGroup(cls).replace('Editor', ''))

    if saveDir is not None:
      saveDir = Path(saveDir)

    self.registeredPrjParams: t.List[PrjParam] = []
    """
    Keeps track of all parameters registerd as properties in this editor. Useful for
    inspecting which parameters are in an editor without traversing the parameter tree
    and reconstructing the name, tooltip, etc.
    """

    self.procToParamsMapping: t.Dict[ProcessStage, GroupParameter] = {}
    """
    Keeps track of registered functions (or prcesses) and their associated
    gui parameters
    """

    self.dock = self
    """Records whether this is a standalone dock or nested inside a ParamEditorDockGrouping"""

    self.name = name
    """Human readable name (for settings menu)"""

    self.saveDir = saveDir
    """Internal parameters for saving settings"""
    self.fileType = fileType
    """Used under the hood to name saved states"""

    # -----------
    # Construct parameter tree
    # -----------
    self.params = Parameter.create(name='Parameters', type='group', children=paramList)

    self.params.sigStateChanged.connect(self._paramTreeChanged)

    topParam = self.params
    if topTreeChild is not None:
      topParam = topTreeChild
    self.tree = fns.flexibleParamTree(topParam, showTop=False)

    self._stateBeforeEdit = self.params.saveState()
    self.lastAppliedName = None

    self._buildGui()

    SPAWNED_EDITORS.append(weakref.proxy(self))

  def _paramTreeChanged(self, *_args, **_kwargs):
    self._stateBeforeEdit = self.params.saveState()

  def applyChanges(self):
    """Broadcasts that this parameter editor has updated changes"""
    # Don't emit any signals if nothing changed
    newState = self.params.saveState(filter='user')
    outDict = self.params.getValues()
    if self._stateBeforeEdit != newState:
      self._stateBeforeEdit = newState
      self.sigChangesApplied.emit(outDict)
    return outDict

  def saveParamValues(self, saveName: str=None, paramState: dict=None, allowOverwriteDefault=False,
                      includeDefaults=False, blockWrite=False):
    """
    * Returns dict on successful parameter save and emits sigParamStateCreated.
    * Returns None if no save name was given
    """
    if saveName is None or self.saveDir is None:
      return None
    elif paramState is None:
      paramState = fns.paramValues(self.params, includeDefaults=includeDefaults or allowOverwriteDefault)
    # Remove non-useful values
    if not blockWrite and self.saveDir is not None:
      self.saveDir.mkdir(parents=True, exist_ok=True)
      fns.saveToFile(paramState, self.formatFileName(saveName),
                 allowOverwriteDefault=allowOverwriteDefault)
    # self.applyChanges()
    self.lastAppliedName = saveName
    self.sigParamStateCreated.emit(str(saveName))
    return paramState

  def saveCurStateAsDefault(self):
    return self.saveParamValues('Default', allowOverwriteDefault=True)

  def _loadParamState(self, stateName: str, stateDict: dict=None, applyChanges=True):
    # Bug in pyqtgraph restore state doesn't play nice when parameters have connected functions outside the parameter
    # item, so re-implement without inserting or removing children
    loadDict = self._parseStateDict(stateName, stateDict)
    with self.params.treeChangeBlocker():
      fns.applyParamOpts(self.params, loadDict)
    if applyChanges:
      self.applyChanges()
    self.lastAppliedName = stateName
    return loadDict

  def loadParamValues(self, stateName: t.Union[str, Path],
                      stateDict: dict=None,
                      candidateParams: t.List[Parameter]=None,
                      applyChanges=True):
    """
    Can restore a state created by `fns.paramValues` If extra keys were saved (other than just 'value'), `hasExtraKeys`
    must be set to *True*
    """
    loadDict = self._parseStateDict(stateName, stateDict)
    # First check for extra keys, will be the case if 'children' is one of the keys. Can't do value-loading in that case,
    # must do state-loading instead
    if 'children' in loadDict:
      return self._loadParamState(stateName, stateDict)
    
    if candidateParams is None:
      candidateParams = fns.params_flattened(self.params)
      
    def validName(param, name):
      return name in (param.opts['title'], param.name())
    def checkParentChain(param, name):
      if not param:
        return False
      return validName(param, name) or checkParentChain(param.parent(), name)
    
    unhandled = {}
    # Copy for mutable object
    for kk, vv in loadDict.items():
      if isinstance(vv, dict):
        # Successively traverse down child tree
        curCandidates = [p for p in candidateParams if checkParentChain(p, kk)]
        self.loadParamValues('', vv, curCandidates, applyChanges=False)
      else:
        unhandled[kk] = vv
    with self.params.treeChangeBlocker():
      for kk, vv in unhandled.items():
        matches = [p for p in candidateParams if validName(p, kk)]
        if len(matches) == 1:
          matches[0].setValue(vv)
        elif len(matches) == 0:
          warnLater(f'No matching parameters for key {kk}. Ignoring.', UserWarning)
        else:
          raise ValueError(f'Multiple matching parameters for key {kk}:\n'
                           f'{matches}')
    if applyChanges:
      self.applyChanges()
    self.lastAppliedName = stateName
    return fns.paramValues(self.params, includeDefaults=True)


  def formatFileName(self, stateName: t.Union[str, Path]=None):
    if stateName is None:
      stateName = self.lastAppliedName
    suffix = f'.{self.fileType}'
    stateName = stateName or suffix
    stateName = Path(stateName)
    if self.saveDir is None:
      # Prevents ValueError at the final return
      return stateName
    elif not stateName.is_absolute():
      stateName = self.saveDir / stateName
    if not stateName.suffix:
      stateName = stateName.with_suffix(suffix)
    return stateName

  def _parseStateDict(self, stateName: t.Union[str, Path], stateDict: dict=None):
    return fns.resolveYamlDict(self.formatFileName(stateName), stateDict)[1]

  def deleteParamState(self, stateName: str):
    filename = self.formatFileName(stateName)
    if not filename.exists():
      return
    filename.unlink()
    self.sigParamStateDeleted.emit(stateName)

  def registerProps(self, constParams: t.List[PrjParam], namePath:t.Sequence[str]=(),
                     asProperty=True, **extraOpts):
    """
    Registers a list of proerties and returns an array of each. For parameter descriptions,
    see :func:`PrjParamEditor.registerProp`.
    """
    outProps = []
    with self.params.treeChangeBlocker():
      for param in constParams:
        outProps.append(self.registerProp(param, namePath, asProperty, **extraOpts))
    return outProps

  def registerProp(self, constParam: PrjParam=None, namePath: t.Sequence[str]=(),
                   asProperty=True, overrideBasePath: t.Sequence[str]=None, **etxraOpts):
    """
    Registers a property defined by *constParam* that will appear in the respective
    parameter editor.

    :param constParam: Object holding parameter attributes such as name, type,
      help text, etc. If *None*, defaults to a 'group' type
    :param namePath: If None, defaults to the top level of the parameters for the
      current class (or paramHolder). *namePath* represents the parent group
      to whom the newly registered parameter should be added
    :param asProperty: If True, creates a property object bound to getter and setter
      for the new param. Otherwise, returns the param itself. If asProperty is false,
      the returned parameter must be evaluated to obtain a value, e.g.
      x = registerProp(..., asProperty=False); myVal = x.value()
    :param overrideBasePath: Whether to use the base path specified by ParamEditor._baseRegisterPath
      (if *None*) or this specified override
    :param etxraOpts: Extra options passed directly to the created :class:`pyqtgraph.Parameter`

    :return: Property bound to this value in the parameter editor
    """
    paramOpts = constParam.toPgDict()
    paramOpts.update(etxraOpts)

    if overrideBasePath is None:
      namePath = tuple(self._baseRegisterPath) + tuple(namePath)
    else:
      namePath = tuple(overrideBasePath) + tuple(namePath)
    paramForEditor = fns.getParamChild(self.params, *namePath, chOpts=paramOpts)

    self.registeredPrjParams.append(constParam)
    if not asProperty:
      return paramForEditor

    @property
    def paramAccessor(_clsObj):
      return paramForEditor.value()

    @paramAccessor.setter
    def paramAccessor(_clsObj, newVal):
      paramForEditor.setValue(newVal)

    return paramAccessor

  def registerFunc(self, func: t.Callable, *, runOpts=RunOpts.BTN,
                   namePath:t.Tuple[str, ...]=(),
                   paramFormat = None,
                   overrideBasePath: t.Sequence[str]=None,
                   btnOpts: t.Union[PrjParam, dict]=None,
                   nest=True,
                   returnParam=False,
                   **kwargs):
    """
    Like `registerProp`, but for functions instead along with interactive parameters
    for each argument. A button is added for the user to force run this function as
    well. In the case of a function with no parameters, the button will be named
    the same as the function itself for simplicity

    :param namePath:  See `registerProp`
    :param func: Function to make interactive
    :param runOpts: Combination of ways this function can be run. Multiple of these
      options can be selected at the same time using the `|` operator.
        * If RunOpts.BTN, a button is present as described.
        * If RunOpts.ON_CHANGE, the function is run when parameter values are
          finished being changed by the user
        * If RunOpts.ON_CHANGING, the function is run every time a value is altered,
          even if the value isn't finished changing.
        * If RunOpts.ON_APPLY, the function is run when "Apply" is pressed. This is useful for when some functions
          must be run simultaneously.
    :param paramFormat: Formatter which turns variable names into display names. The default takes variables in pascal
      case (e.g. variableName) or snake case (e.g. variable_name) and converts to Title Case (e.g. Variable Name).
      Custom functions must have the signature (str) -> str. To change default behavior, see `nameFormat.set()`.
    :param overrideBasePath: See :meth:`~ParamEditor.registerProp`
    :param btnOpts: Overrides defaults for button used to run this function. If
      `RunOpts.BTN` is not in `RunOpts`, these values are ignored.
    :param nest: If *True*, functions with multiple default arguments will have these nested
      inside a group parameter bearing the function name. Otherwise, they will be added
      directly to the parent parameter specified by `namePath` + `baseRegisterPath`
    :param returnParam: Whether to return the parent parameter associated with this newly
      registered function
    :param kwargs: All additional kwargs are passed to AtomicProcess when wrapping the function.
    """
    if not isinstance(func, ProcessStage):
      proc: ProcessStage = AtomicProcess(func, **kwargs)
    else:
      proc = func
    # Define caller out here that takes no params so qt signal binding doesn't
    # screw up auto parameter population
    def runProc():
      return proc.run()

    def runpProc_changing(_param: Parameter, newVal: t.Any):
      forwardedOpts = ProcessIO(**{_param.name(): newVal})
      return proc.run(forwardedOpts)

    if overrideBasePath is None:
      namePath = tuple(self._baseRegisterPath) + tuple(namePath)
    else:
      namePath = tuple(overrideBasePath) + tuple(namePath)

    topParam = fns.getParamChild(self.params, *namePath)
    if len(proc.input.hyperParamKeys) > 0:
      # Check if proc params already exist from a previous addition
      wrapped = NestedProcWrapper(proc, topParam, paramFormat or fns.nameFormatter, treatAsAtomic=True, nestHyperparams=nest)
      parentParam = wrapped.parentParam
      for param in parentParam:
        if runOpts & RunOpts.ON_CHANGED:
          param.sigValueChanged.connect(runProc)
        if runOpts & RunOpts.ON_CHANGING:
          param.sigValueChanging.connect(runpProc_changing)
    else:
      parentParam: GroupParameter = topParam
    if runOpts & RunOpts.BTN:
      runBtnDict = _mkRunDict(proc, btnOpts)
      if not nest:
        # Make sure button name is correct
        runBtnDict['name'] = proc.name
      runBtn = fns.getParamChild(parentParam, chOpts=runBtnDict)
      runBtn.sigActivated.connect(runProc)
    if runOpts & RunOpts.ON_APPLY:
      self.sigChangesApplied.connect(runProc)
    self.procToParamsMapping[proc] = parentParam

    if returnParam:
      return proc, parentParam
    return proc

  @classmethod
  def buildClsToolsEditor(cls, forCls: type, name: str=None):
    groupName = fns.clsNameOrGroup(forCls)
    lowerGroupName = groupName.lower()
    if name is None:
      name = groupName
    if not name.endswith('Tools'):
      name = name + ' Tools'
    toolsEditor = cls(fileType=lowerGroupName.replace(' ', ''), name=name)
    for btn in (toolsEditor.saveAsBtn, toolsEditor.applyBtn, toolsEditor.expandAllBtn,
                toolsEditor.collapseAllBtn):
      btn.hide()
    return toolsEditor

  def createMenuOpt(self, overrideName=None, parentMenu: QtWidgets.QMenu=None):
    if overrideName is None:
      overrideName = self.name
    editAct = QtWidgets.QAction('Open ' + overrideName, self)
    if self.saveDir is None:
      # No save options are possible, just use an action instead of dropdown menu
      newMenuOrAct = editAct
      if parentMenu is not None:
        parentMenu.addAction(newMenuOrAct)
    else:
      newMenuOrAct = QtWidgets.QMenu(overrideName, self)
      newMenuOrAct.addAction(editAct)
      newMenuOrAct.addSeparator()
      def populateFunc():
        self.addDirItemsToMenu(newMenuOrAct)
      self.sigParamStateCreated.connect(populateFunc)
      # Initialize default menus
      populateFunc()
      if parentMenu is not None:
        parentMenu.addMenu(newMenuOrAct)
    editAct.triggered.connect(self.show)
    return newMenuOrAct

  def actionsMenuFromProcs(self, title: str=None, nest=True, parent: QtWidgets.QWidget=None, outerMenu: QtWidgets.QMenu=None):
    title = title or self.dock.name
    if nest and outerMenu:
      menu = QtWidgets.QMenu(title, parent)
      outerMenu.addMenu(menu)
    elif outerMenu:
      menu = outerMenu
    else:
      menu = QtWidgets.QMenu(title, parent)
    for proc in self.procToParamsMapping:
      menu.addAction(proc.name, lambda _p=proc: _p.run())
    return menu

  def addDirItemsToMenu(self, parentMenu: QtWidgets.QMenu, removeExistingChildren=True):
    """Helper function for populating menu from directory contents"""
    # We don't want all menu children to be removed, since this would also remove the 'edit' and
    # separator options. So, do this step manually. Remove all actions after the separator
    if self.saveDir is None:
      return
    dirGlob = self.saveDir.glob(f'*.{self.fileType}')
    # Define outside for range due to loop scoping
    def _loader(name):
      def _call():
        self.loadParamValues(name)
      return _call
    if removeExistingChildren:
      encounteredSep = False
      for ii, action in enumerate(parentMenu.children()):
        action: QtWidgets.QAction
        if encounteredSep:
          parentMenu.removeAction(action)
        elif action.isSeparator():
          encounteredSep = True
    # TODO: At the moment param files that start with '.' aren't getting included in the
    #  glob
    for name in dirGlob:
      # glob returns entire filepath, so keep only filename as layout name
      name = name.with_suffix('').name
      curAction = parentMenu.addAction(name)
      curAction.triggered.connect(_loader(name))

  @classmethod
  @contextmanager
  def setBaseRegisterPath(cls, *path: str):
    oldPath = cls._baseRegisterPath
    cls._baseRegisterPath = path
    yield
    cls._baseRegisterPath = oldPath

  def _buildGui(self, **kwargs):
    self.setWindowTitle(self.name)
    self.setObjectName(self.name)

    # -----------
    # Additional widget buttons
    # -----------
    self.expandAllBtn = QtWidgets.QPushButton('Expand All')
    self.collapseAllBtn = QtWidgets.QPushButton('Collapse All')
    self.saveAsBtn = QtWidgets.QPushButton('Save As...')
    self.applyBtn = QtWidgets.QPushButton('Apply')

    # -----------
    # Widget layout
    # -----------
    children = [
      [self.expandAllBtn, self.collapseAllBtn],
      self.tree,
      [self.saveAsBtn, self.applyBtn]
    ]
    if self.saveDir is None:
      self.saveAsBtn.hide()
    self.dockContentsWidget = utilitys.widgets.EasyWidget.buildWidget(children)
    self.centralLayout = self.dockContentsWidget.easyChild.layout_
    self.setWidget(self.dockContentsWidget)


    # self.setLayout(centralLayout)
    self.tree.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    # -----------
    # UI Element Signals
    # -----------
    self.expandAllBtn.clicked.connect(lambda: fns.setParamsExpanded(self.tree))
    self.collapseAllBtn.clicked.connect(lambda: fns.setParamsExpanded(self.tree, False))
    self.saveAsBtn.clicked.connect(self.saveParamValues_gui)
    self.applyBtn.clicked.connect(self.applyChanges)

  def __repr__(self):
    selfCls = type(self)
    oldName: str = super().__repr__()
    # Remove module name for brevity
    oldName = oldName.replace(f'{selfCls.__module__}.{selfCls.__name__}',
                              f'{selfCls.__name__} \'{self.name}\'')
    return oldName

  def show(self):
    if self.dock is self:
      return super().show()
    if isinstance(self.dock, ParamEditorDockGrouping):
      tabs: QtWidgets.QTabWidget = self.dock.tabs
      dockIdx = tabs.indexOf(self.dockContentsWidget)
      tabs.setCurrentIndex(dockIdx)
    self.tree.resizeColumnToContents(0)
    # Necessary on MacOS
    self.dock.setWindowState(QtCore.Qt.WindowActive)
    self.dock.raise_()
    self.dock.show()
    # Necessary on Windows
    self.activateWindow()
    self.applyBtn.setFocus()

  def reject(self):
    """
    If window is closed apart from pressing 'accept', restore pre-edit state
    """
    self.params.restoreState(self._stateBeforeEdit, removeChildren=False)
    super().reject()

  def saveParamValues_gui(self):
    saveName = fns.dialogGetSaveFileName(self, 'Save As', self.lastAppliedName)
    self.saveParamValues(saveName)

class ParamEditorDockGrouping(QtWidgets.QDockWidget):
  """
  When multiple parameter editor windows should be grouped under the same heading,
  this class is responsible for performing that grouping.
  """
  def __init__(self, editors: t.List[ParamEditor]=None, dockName:str='', parent=None):
    super().__init__(parent)
    self.tabs = QtWidgets.QTabWidget(self)
    self.hide()

    if editors is None:
      editors = []

    if len(dockName) == 0 and len(editors) > 0:
      dockName = editors[0].name
    dockName = dockName.replace('&', '')
    self.name = dockName

    self.editors = []
    self.addEditors(editors)

    mainLayout = QtWidgets.QVBoxLayout()
    mainLayout.addWidget(self.tabs)
    centralWidget = QtWidgets.QWidget()
    centralWidget.setLayout(mainLayout)
    self.setWidget(centralWidget)
    self.setObjectName(dockName)
    self.setWindowTitle(dockName)

    self.biggestMinWidth = 0

  def addEditors(self, editors: t.Sequence[ParamEditor]):
    minWidth = 0
    for editor in editors:
      editor.tree.resizeColumnToContents(0)
      if editor.width() > minWidth:
        minWidth = int(editor.width()*0.8)
      # "Main Image Settings" -> "Settings"
      tabName = self.getTabName(editor)
      self.tabs.addTab(editor.dockContentsWidget, tabName)
      editor.dock = self
      self.editors.append(editor)
    self.biggestMinWidth = minWidth

  def removeEditors(self, editors: t.Sequence[ParamEditor]):
    for editor in editors:
      idx = self.editors.index(editor)
      self.tabs.removeTab(idx)
      editor.dock = editor
      del self.editors[idx]

  def setParent(self, parent: QtWidgets.QWidget=None):
    super().setParent(parent)
    for editor in self.editors:
      editor.setParent(parent)

  def getTabName(self, editor: ParamEditor):
    if self.name in editor.name and len(self.name) > 0:
      tabName = editor.name.split(self.name)[1][1:]
      if len(tabName) == 0:
        tabName = editor.name
    else:
      tabName = editor.name
    return tabName

  def createMenuOpt(self, overrideName=None, parentMenu: QtWidgets.QMenu=None):
    if overrideName is None:
      overrideName = self.name
    if parentMenu is None:
      parentMenu = QtWidgets.QMenu(overrideName, self)
    # newMenu = create_addMenuAct(self, parentBtn, dockEditor.name, True)
    for editor in self.editors: # type: ParamEditor
      # "Main Image Settings" -> "Settings"
      tabName = self.getTabName(editor)
      nameWithoutBase = tabName
      editor.createMenuOpt(overrideName=nameWithoutBase, parentMenu=parentMenu)
    return parentMenu


class EditorPropsMixin:
  __groupingName__: str = None

  REGISTERED_GROUPINGS = set()
  def __new__(cls, *args, **kwargs):
    if cls.__groupingName__ is None:
      cls.__groupingName__ = fns.nameFormatter(cls.__name__)
    if cls not in cls.REGISTERED_GROUPINGS:
      basePath = (cls.__groupingName__,)
      if basePath[0] == '':
        basePath = ()
      with ParamEditor.setBaseRegisterPath(*basePath):
        cls.__initEditorParams__()
      cls.REGISTERED_GROUPINGS.add(cls)
    return super().__new__(cls, *args, **kwargs)

  @classmethod
  def __initEditorParams__(cls):
    pass

SPAWNED_EDITORS: t.List[ParamEditor] = []