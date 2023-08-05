from __future__ import annotations

from typing import Optional, Callable, Sequence

from pyqtgraph.Qt import QtWidgets

from . import parameditor as pe, ShortcutParameter
from .prjparam import PrjParam
from ..fns import create_addMenuAct, paramWindow


class ParamEditorPlugin(pe.EditorPropsMixin):
  """
  Primitive plugin which can interface with window functionality. When this class is overloaded,
  the child class is given a reference to the main window and the main window is made aware of the
  plugin's existence. For interfacing with table fields, see the special case of
  :class:`TableFieldPlugin`
  """
  name: str=None
  """
  Name of this plugin as it should appear in the plugin menu
  """

  menu: QtWidgets.QMenu=None
  """
  Menu of additional options that should appear under this plugin
  """

  dock: Optional[pe.ParamEditorDockGrouping]
  """
  Docks that should be shown in a main window's menu bar. By default, just the toolsEditor is shown.
  If multiple param editors must be visible, manually set this property to a
  :class:`PrjParamEditorDockGrouping` as performed in :class:`XYVerticesPlugin`.
  """
  toolsEditor: pe.ParamEditor
  """Param Editor window which holds user-editable properties exposed by the programmer"""

  _showFuncDetails=False
  """If *True*, a menu option will be added to edit parameters for functions that need them"""

  _makeMenuShortcuts=True
  """Whether shortcuts should be added to menu options"""

  _toolsEditorName:str=None
  """Name of the class tools editor. If not provided, defaults to '<class name> Tools'"""

  win = None
  """Reference to the application main window"""

  @property
  def parentMenu(self):
    """
    When this plugin is added, its options will be visible under a certain menu or toolbar. Where it is placed is
    determined by this value, which is usually the window's menu bar
    """
    return self.win.menuBar()

  @classmethod
  def __initEditorParams__(cls):
    """
    Creates most of the necessary components for interacting with editor properties including
    a dock that can be placed in a main window, a tools editor for registering properties and
    functions, and a dropdown menu for accessing these functions.
    """
    cls.dock = pe.ParamEditorDockGrouping(dockName=cls.name)
    cls.toolsEditor = pe.ParamEditor.buildClsToolsEditor(cls, cls._toolsEditorName)
    if cls._showFuncDetails:
      cls.dock.addEditors([cls.toolsEditor])
    cls.menu = QtWidgets.QMenu(cls.name)

  def __init__(self, *args, **kwargs):
    if self.dock is not None:
      self.dock.createMenuOpt(parentMenu=self.menu)
      self.menu.addSeparator()

  def registerFunc(self, func: Callable, submenuName:str=None, editor:pe.ParamEditor=None, **kwargs):
    """
    :param func: Function to register
    :param submenuName: If provided, this function is placed under a breakout menu with this name
    :param editor: If provided, the function is registered here instead of the plugin's tool editor
    :param kwargs: Forwarded to `ParamEditor.registerFunc`
    """
    if editor is None:
      editor = self.toolsEditor
    paramPath = []
    if submenuName is not None:
      paramPath.append(submenuName)
      parentMenu = None
      for act in self.menu.actions():
        if act.text() == submenuName and act.menu():
          parentMenu = act.menu()
          break
      if parentMenu is None:
        parentMenu = create_addMenuAct(editor, self.menu, submenuName, True)
        editor.params.addChild(dict(name=submenuName, type='group'))
    else:
      parentMenu = self.menu

    shcValue = opts = None
    if 'btnOpts' in kwargs:
      opts = PrjParam(**kwargs['btnOpts'])
      opts.opts.setdefault('ownerObj', self)
      kwargs.setdefault('name', opts.name)
      kwargs['btnOpts'] = opts
      shcValue = opts.value
    proc = editor.registerFunc(func, **kwargs)
    act = parentMenu.addAction(proc.name)
    if ShortcutParameter.REGISTRY and shcValue and self._makeMenuShortcuts:
      ShortcutParameter.REGISTRY.registerAction(opts, act,
                                                namePath=(self.__groupingName__,))

    act.triggered.connect(lambda: proc(win=self.win))
    return proc

  def registerPopoutFuncs(self, funcList: Sequence[Callable], nameList: Sequence[str]=None, groupName:str=None, btnOpts: PrjParam=None):
    # TODO: I really don't like this. Consider any refactoring option that doesn't
    #   have an import inside a function
    if groupName is None and btnOpts is None:
      raise ValueError('Must provide either group name or button options')
    elif btnOpts is None:
      btnOpts = PrjParam(groupName)
    if groupName is None:
      groupName = btnOpts.name
    act = self.menu.addAction(groupName, lambda: paramWindow(self.toolsEditor.params.child(groupName)))
    if nameList is None:
      nameList = [None]*len(funcList)
    for title, func in zip(nameList, funcList):
      self.toolsEditor.registerFunc(func, name=title, namePath=(groupName,))
    if ShortcutParameter.REGISTRY and btnOpts.value and self._makeMenuShortcuts:
      ShortcutParameter.REGISTRY.registerAction(btnOpts, act,
                                                namePath=(self.__groupingName__,))

    self.menu.addSeparator()


  def attachWinRef(self, win):
    self.win = win
    self.menu.setParent(self.parentMenu, self.menu.windowFlags())


def dockPluginFactory(name_: str=None, editors: Sequence[pe.ParamEditor]=None):
  class DummyPlugin(ParamEditorPlugin):
    name = name_

    @classmethod
    def __initEditorParams__(cls):
      super().__initEditorParams__()
      if editors is not None:
        cls.dock.addEditors(editors)
  return DummyPlugin