import inspect
import multiprocessing as mp
import re
import sys
import typing as t
from ast import literal_eval
from contextlib import contextmanager
from functools import partial, wraps
from inspect import isclass
from io import StringIO
from pathlib import Path
from traceback import format_exception
from typing import Collection, List
from warnings import warn

import docstring_parser as dp
import pandas as pd
from PyQt5 import QtWidgets, QtCore
from pyqtgraph.parametertree import Parameter, ParameterTree
from ruamel.yaml import YAML
from tqdm.auto import tqdm
from utilitys.params import PrjParam
from utilitys.typeoverloads import FilePath
from utilitys.widgets import ScrollableErrorDialog

yaml = YAML()

def mproc_apply(func, iterLst, descr='', iterArgPos=0, extraArgs=(), showProgress=True, applyAsync=True, total=None, pool=None):
  if pool is None:
    pool = mp.Pool()

  if total is None:
    try:
      total = len(iterLst)
    except (AttributeError, TypeError):
      total = None

  callback = None
  if showProgress:
    progBar = tqdm(total=total, desc=descr)
    def updateProgBar(*_):
      progBar.update()
    callback = updateProgBar

  pre_results = []
  errs = {}
  def errCallback(_ii, ex):
    errs[_ii] = str(ex)

  iterable = enumerate(iterLst)
  if applyAsync:
    applyFunc = partial(pool.apply_async, callback=callback, error_callback=lambda ex: errCallback(ii, ex))
  else:
    if showProgress:
      iterable = tqdm(iterable, total=total)
    applyFunc = pool.apply

  extraArgs = tuple(extraArgs)
  for ii, el in iterable:
    curArgs = extraArgs[:iterArgPos]+(el,)+extraArgs[iterArgPos:]
    pre_results.append(applyFunc(func, curArgs))
  pool.close()
  pool.join()
  if len(errs) > 0:
    msg = f'The following errors occurred at the specified list indices:\n'
    for k, v in errs.items():
      msg += f'{k}: {v}\n'
    warn(msg)
  if applyAsync:
    return [res.get() for res in pre_results]
  else:
    return pre_results


def pascalCaseToTitle(name: str, addSpaces=True) -> str:
  """
  Helper utility to turn a PascalCase name to a 'Title Case' title
  :param name: camel-cased name
  :param addSpaces: Whether to add spaces in the final result
  :return: Space-separated, properly capitalized version of :param:`Name`
  """
  if not name:
    return name
  if name.startswith('FR'):
    name = name[2:]
  if addSpaces:
    replace = r'\1 \2'
  else:
    replace = r'\1\2'
  name = re.sub(r'(\w)([A-Z])', replace, name)
  name = name.replace('_', ' ')
  return name.title()

def dynamicDocstring(embed=False, **kwargs):
  """
  Docstrings must be known at compile time. However this prevents expressions like

  ```
  x = ['dog', 'cat', 'squirrel']
  def a(animal: str):
    \"\"\"
    param animal: must be one of {x}
    \"\"\"
  ```

  from compiling. This can make some featurs of function registration difficult, like dynamically generating
  limits for a docstring list. `dynamicDocstring` wrapps a docstring and provides kwargs
  for string formatting.
  Retrieved from https://stackoverflow.com/a/10308363/9463643

  :param embed: Sometimes, the value that should be accessed from the docstring is not recoverable from its string
    representation. YAML knows how to serialize the default types, but it is a pain to write a deserialization protocol
    for every object used as a dynamic reference. To avoid this, `embed` determines whether a `__docObjs__` reference
    should eb attached to the function with the raw object values. I.e. instead of storing the string representation of
    a list kwarg, __docObjs__ would hold a reference to the list itself.
  :param kwargs: List of kwargs to pass to formatted docstring
  """
  def wrapper(obj):
    obj.__doc__ = obj.__doc__.format(**kwargs)
    if embed:
      obj.__docObjs__ = kwargs
    return obj
  return wrapper

def clsNameOrGroup(cls: t.Union[type, t.Any]):
  if not inspect.isclass(cls):
    cls = type(cls)
  if hasattr(cls, '__groupingName__'):
    return cls.__groupingName__
  return pascalCaseToTitle(cls.__name__)


def saveToFile(saveObj, savePath: Path, allowOverwriteDefault=False):
  if not allowOverwriteDefault and savePath.stem.lower() == 'default':
    errMsg = 'Cannot overwrite default setting.\n\'Default\' is automatically' \
             ' generated, so it should not be modified.'
    raise IOError(errMsg)
  else:
    # Known pycharm bug
    # noinspection PyTypeChecker
    with open(savePath, 'w') as saveFile:
      yaml.dump(saveObj, saveFile)

def serAsFrame(ser: pd.Series):
  return ser.to_frame().T

def attemptFileLoad(fpath: FilePath , openMode='r') -> t.Union[dict, bytes]:
  with open(fpath, openMode) as ifile:
    loadObj = yaml.load(ifile)
  return loadObj

def coerceAnnotation(ann: t.Any):
  """
  From a function argument annotation, attempts to find a default value matching
  that annotation. E.g. for the function signature
  `def a(param: int)`
  `inspect` is used to find the signature, and `param`'s annotation would be `int`.
  This function would turn that into `int()`, or 0. Attempts are as follows:
    - If the annotation is a string, attempts are made to convert it to a value, e.g.
      `def a(param: 'int')` will follow the flow of `def a(param: int).Note this
       will fail if the annotation is for a class not in scope upon evaluation.
    - If direct conversion works as described in the docstring, the value is returned.

       * If this fails due to *TypeError*, the following cases are examined:
         * typing.Union (flow is followed for each union type until non-None is
         returned or all types have been examined)
         * typing.List, Tuple, Dict, <builtim>: That builtin is returned

     - All other cases result in *None* being returned.
  """
  if isinstance(ann, str):
    ann = literal_eval(ann)
  try:
    return ann()
  except TypeError:
    # Check for typing types
    if getattr(ann, '__module__', None) == t.__name__:
      if ann.__origin__ is t.Union:
        ann: t.Union
        for arg in ann.__args__:
          ret = coerceAnnotation(arg)
          if ret is not None:
            return ret
      else:
        # Check for typing instances of builtins
        if hasattr(ann, '_name'):
          # Any broad exception is fine
          # noinspection PyBroadException
          try:
            # Not easy without protected member access
            # noinspection PyProtectedMember
            return literal_eval(ann._name.lower())
          except Exception:
            pass
  return None


def create_addMenuAct(mainWin: QtWidgets.QWidget, parentMenu: QtWidgets.QMenu, title: str, asMenu=False) \
    -> t.Union[QtWidgets.QMenu, QtWidgets.QAction]:
  menu = None
  if asMenu:
    menu = QtWidgets.QMenu(title, mainWin)
    act = menu.menuAction()
  else:
    act = QtWidgets.QAction(title)
  parentMenu.addAction(act)
  if asMenu:
    return menu
  else:
    return act


def clearUnwantedParamVals(paramState: dict):
  for _k, child in paramState.get('children', {}).items():
    clearUnwantedParamVals(child)
  if paramState.get('value', True) is None:
    paramState.pop('value')


def paramState_noDefaults(param: Parameter, extraKeys: Collection[str]=('value',), extraTypes: List[type]=None):
  parentDict = {}
  val = param.value()
  if extraTypes is None:
    extraTypes = set()
  extraTypes = tuple(extraTypes)
  if val != param.defaultValue():
    parentDict['value'] = param.value()
    if not extraTypes or isinstance(param, extraTypes):
      for k in set(extraKeys):
        # False positive
        # noinspection PyUnresolvedReferences
        parentDict[k] = param.opts[k]
  if param.hasChildren() and not parentDict:
    inner = {}
    for child in param:
      chDict = paramState_noDefaults(child)
      if len(chDict) > 0:
        inner[child.name()] = paramState_noDefaults(child)
    if len(inner) > 0:
      parentDict['children'] = inner
  return parentDict


def params_flattened(param: Parameter):
  addList = []
  if 'group' not in param.type():
    addList.append(param)
  for child in param.children(): # type: Parameter
    addList.extend(params_flattened(child))
  return addList


def flexibleParamTree(topParam:Parameter=None, showTop=True):
  tree = ParameterTree()
  tree.setTextElideMode(QtCore.Qt.ElideRight)
  tree.header().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
  if topParam is not None:
    tree.setParameters(topParam, showTop)
  return tree


def resolveYamlDict(cfgFname: FilePath, cfgDict: dict=None):
  if cfgDict is not None:
    cfg = cfgDict
  else:
    cfg = attemptFileLoad(cfgFname)
  return Path(cfgFname), cfg


def getParamChild(param: Parameter, *childPath: t.Sequence[str], allowCreate=True, groupOpts:dict=None,
                  chOpts: dict=None):
  if groupOpts is None:
    groupOpts = {}
  groupOpts.setdefault('type', 'group')
  while childPath and childPath[0] in param.names:
    param = param.child(childPath[0])
    childPath = childPath[1:]
  # All future children must be created
  if allowCreate:
    for chName in childPath:
      param = param.addChild(dict(name=chName, **groupOpts))
      childPath = childPath[1:]
  elif len(childPath) > 0:
    # Child doesn't exist
    raise KeyError(f'Children {childPath} do not exist in param {param}')
  if chOpts is not None:
    if chOpts['name'] in param.names:
      param = param.child(chOpts['name'])
    else:
      param = param.addChild(chOpts)
  return param


def dialogGetSaveFileName(parent, winTitle, defaultTxt: str=None)-> t.Optional[str]:
  failedSave = True
  returnVal: t.Optional[str] = None
  while failedSave:
    saveName, ok = QtWidgets.QInputDialog().getText(
      parent, winTitle, winTitle + ':', QtWidgets.QLineEdit.Normal, defaultTxt)
    # TODO: Make this more robust. At the moment just very basic sanitation
    for disallowedChar in ['/', '\\']:
      saveName = saveName.replace(disallowedChar, '')
    if ok and not saveName:
      # User presses 'ok' without typing anything except disallowed characters
      # Keep asking for a name
      continue
    elif not ok:
      # User pressed 'cancel' -- Doesn't matter whether they entered a name or not
      # Stop asking for name
      break
    else:
      # User pressed 'ok' and entered a valid name
      return saveName
  return returnVal


def docParser(docstring: str):
  """
  From a function docstring, extracts relevant information for how to create smarter
    parameter boxes.

  :param docstring: Function docstring
  """
  parsed = dp.parse(docstring)
  descrPieces = [p for p in (parsed.short_description, parsed.long_description) if p is not None]
  descr = ' '.join(descrPieces)
  out = {}
  for param in parsed.params:
    stream = StringIO(param.description)
    paramDoc = yaml.load(stream)
    if isinstance(paramDoc, str):
      paramDoc = {'helpText': paramDoc}
    if paramDoc is None:
      continue
    out[param.arg_name] = PrjParam(name=param.arg_name, **paramDoc)
    if 'pType' not in paramDoc:
      out[param.arg_name].pType = None
  out['top-descr'] = descr
  return out


def paramWindow(param: Parameter):
  tree = flexibleParamTree(param)
  tree.setHeaderHidden(True)
  tree.resizeColumnToContents(0)
  dlg = QtWidgets.QDialog()
  layout = QtWidgets.QVBoxLayout()
  dlg.setLayout(layout)
  layout.addWidget(tree)
  dlg.exec_()


def popupFilePicker(parent=None, winTitle: str='', fileFilter: str='', existing=True, asFolder=False,
                    selectMultiple=False, startDir: str=None, **kwargs) -> t.Optional[t.Union[str, t.List[str]]]:
  """
  Thin wrapper around Qt file picker dialog. Used internally so all options are consistent
  among all requests for external file information

  :param parent: Dialog parent
  :param winTitle: Title of dialog window
  :param fileFilter: File filter as required by the Qt dialog
  :param existing: Whether the file is already existing, or is being newly created
  :param asFolder: Whether the dialog should select folders or files
  :param selectMultiple: Whether multiple files can be selected. If `asFolder` is
    *True*, this parameter is ignored.
  :param startDir: Where in the file system to open this dialog
  :param kwargs: Consumes additional arguments so dictionary unpacking can be used
    with the lengthy file signature. In the future, this may allow additional config
    options.
  """
  fileDlg = QtWidgets.QFileDialog(parent)
  fileMode = fileDlg.AnyFile
  opts = fileDlg.DontUseNativeDialog
  if existing:
    # Existing files only
    fileMode = fileDlg.ExistingFiles if selectMultiple else fileDlg.ExistingFile
  else:
    fileDlg.setAcceptMode(fileDlg.AcceptSave)
  if asFolder:
    fileMode = fileDlg.Directory
    opts |= fileDlg.ShowDirsOnly
  fileDlg.setFileMode(fileMode)
  fileDlg.setOptions(opts)
  fileDlg.setModal(True)
  if startDir is not None:
    fileDlg.setDirectory(startDir)
  fileDlg.setNameFilter(fileFilter)

  fileDlg.setOption(fileDlg.DontUseNativeDialog, True)
  fileDlg.setWindowTitle(winTitle)

  if fileDlg.exec_():
    # Append filter type
    suffMatch = re.search(r'\*\.?(\w+)', fileDlg.selectedNameFilter())
    if suffMatch:
      fileDlg.setDefaultSuffix(suffMatch.group(1))
    fList = fileDlg.selectedFiles()
  else:
    fList = []

  if selectMultiple:
    return fList
  elif len(fList) > 0:
    return fList[0]
  else:
    return None


old_sys_except_hook = sys.excepthook
usingPostponedErrors = False
_eType = t.Union[t.Type[Exception], t.Type[Warning]]


def makeExceptionsShowDialogs(win: QtWidgets.QMainWindow,
                              nonCritErrs: t.Tuple[_eType]=(Warning,)):
  """
  When a qt application encounters an error, it will generally crash the entire
  application even if this is undesirable behavior. This will make qt applications
  show a dialog rather than crashing.
  Use with caution! Maybe the application *should* crash on an error, but this will
  prevent that from happening.
  """
  app = QtWidgets.QApplication.instance()

  # Procedure taken from https://stackoverflow.com/a/40674244/9463643
  def new_except_hook(etype, evalue, tb):
    # Allow sigabort to kill the app
    if etype in [KeyboardInterrupt, SystemExit]:
      app.exit(1)
      app.processEvents()
      raise
    msgWithTrace = ''.join(format_exception(etype, evalue, tb))
    msgWithoutTrace = str(evalue)
    dlg = ScrollableErrorDialog(win, notCritical=issubclass(etype, nonCritErrs),
                                msgWithTrace=msgWithTrace, msgWithoutTrace=msgWithoutTrace)
    dlg.show()
    dlg.exec_()
  def patch_excepthook():
    global usingPostponedErrors
    sys.excepthook = new_except_hook
    usingPostponedErrors = True
  QtCore.QTimer.singleShot(0, patch_excepthook)
  app.processEvents()


def restoreExceptionBehavior():
  app = QtWidgets.QApplication.instance()
  def patch_excepthook():
    global usingPostponedErrors
    sys.excepthook = old_sys_except_hook
    usingPostponedErrors = False
  QtCore.QTimer.singleShot(0, patch_excepthook)
  app.processEvents()


def raiseErrorLater(err: Exception):
  # Fire immediately if not in gui mode
  if not usingPostponedErrors:
    raise err
  # else
  def _raise():
    raise err
  QtCore.QTimer.singleShot(0, _raise)