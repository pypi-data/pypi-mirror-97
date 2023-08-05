from typing import Callable, Any, Dict, Sequence, Union
from warnings import warn

from pyqtgraph.Qt import QtWidgets, QtCore, QtGui

from ..fns import clsNameOrGroup, params_flattened, getParamChild, warnLater
from .parameditor import ParamEditor, PrjParam


class ShortcutsEditor(ParamEditor):

  def __init__(self, **kwargs):
    kwargs.setdefault('fileType', 'shortcut')
    kwargs.setdefault('name', 'Tool Shortcuts')
    super().__init__(**kwargs)

  def _checkUniqueShortcut(self, shortcutOpts: PrjParam):
    # TODO: Find way to preserve old shortcuts, in case multuple other operations
    #   were bound to this shortcut and lost
    if any(shortcutOpts.name == p.name() and shortcutOpts.value == p.defaultValue() for p in params_flattened(self.params)):
      self.deleteShortcut(shortcutOpts)

  def _createSeq(self, shortcutOpts: Union[PrjParam, dict],
                 namePath: Sequence[str]=(),
                 overrideBasePath: Sequence[str]=None,
                 **kwargs):
    if overrideBasePath is None:
      namePath = tuple(self._baseRegisterPath) + tuple(namePath)
    else:
      namePath = tuple(overrideBasePath) + tuple(namePath)
    # Round-trip to set helptext, ensure all values are present
    if isinstance(shortcutOpts, dict): shortcutOpts = PrjParam(**shortcutOpts)
    shcForCreate = shortcutOpts.toPgDict()
    shcForCreate['type'] = 'keyseq'
    param = getParamChild(self.params, *namePath, chOpts=shcForCreate)
    param.sigValueChanged.connect(lambda _p, val: self.maybeAmbigWarning(val))
    self.maybeAmbigWarning(param.value())

    return param

  def registerShortcut(self, shortcutOpts: PrjParam, func: Callable,
                   funcArgs: tuple=(), funcKwargs: dict=None, overrideOwnerObj: Any=None,
                   **kwargs):
    self._checkUniqueShortcut(shortcutOpts)
    if funcKwargs is None:
      funcKwargs = {}
    if overrideOwnerObj is None:
      overrideOwnerObj = shortcutOpts.opts.get('ownerObj', None)
    if overrideOwnerObj is None:
      raise ValueError('Solo functions registered to shortcuts must have an owner.\n'
                       f'This is not the case for {func}')
    kwargs.setdefault('namePath', (clsNameOrGroup(overrideOwnerObj),))
    param = self._createSeq(shortcutOpts, **kwargs)
    shc = QtWidgets.QShortcut(overrideOwnerObj)
    shc.setContext(QtCore.Qt.WidgetWithChildrenShortcut)

    shc.activatedAmbiguously.connect(lambda: self.maybeAmbigWarning(param.value()))

    def onChange(_param, key):
      shc.setKey(key)
      self.maybeAmbigWarning(key)
    param.sigValueChanged.connect(onChange)
    onChange(param, param.value())

    def onActivate():
      func(*funcArgs, **funcKwargs)
    shc.activated.connect(onActivate)

    return param

  def registerAction(self, btnOpts: PrjParam, action: QtWidgets.QAction, **kwargs):
    self._checkUniqueShortcut(btnOpts)

    param = self._createSeq(btnOpts, **kwargs)
    action.setToolTip(btnOpts.helpText)
    def shcChanged(_param, newSeq: str):
      action.setShortcut(newSeq)

    param.sigValueChanged.connect(shcChanged)
    shcChanged(None, btnOpts.value)
    return param

  def registerButton(self, btnOpts: PrjParam,
                     baseBtn: QtWidgets.QAbstractButton,
                     **kwargs):
    if btnOpts.value is None:
      # Either the shortcut wasn't given a value or wasn't requested, or already exists
      return None
    self._checkUniqueShortcut(btnOpts)
    param = self._createSeq(btnOpts, **kwargs)

    def shcChanged(_param, newSeq: str):
      newTooltipText = f'Shortcut: {newSeq}'
      tip = btnOpts.addHelpText(newTooltipText, replace=False)
      baseBtn.setToolTip(tip)
      baseBtn.setShortcut(newSeq)
    param.sigValueChanged.connect(shcChanged)
    shcChanged(None, btnOpts.value)
    return param

  def maybeAmbigWarning(self, shortcut: str):
    conflicts = [p.name() for p in params_flattened(self.params) if p.value() == shortcut]
    if len(conflicts) > 1:
      warn(f'Ambiguous shortcut: {shortcut}\n'
           f'Perhaps multiple shortcuts are assigned the same key sequence? Possible conflicts:\n'
           f'{conflicts}',
           UserWarning)

  def deleteShortcut(self, shortcutParam: Union[str, PrjParam]):
    if isinstance(shortcutParam, str):
      shortcutParam = PrjParam(shortcutParam)
    matches = [p for p in params_flattened(self.params) if p.name() == shortcutParam['name']]

    formatted = f'<{shortcutParam["name"]}: {shortcutParam["value"]}>'
    if len(matches) == 0:
      warnLater(f'Shortcut param {formatted} does not exist. No delete performed.')
      return
    for match in matches:
      # Set shortcut key to nothing to prevent its activation
      match.setValue('')
      match.remove()


  def registerProp(self, *args, **etxraOpts):
    """
    Properties should never be registered as shortcuts, so make sure this is disallowed
    """
    raise AttributeError('Cannot register property/attribute as a shortcut')

  def registerFunc(self, *args, **kwargs):
    """Functions should not be registered as shortcuts"""
    raise AttributeError('Cannot register function as a shortcut. See `registerShortcut` instead.')