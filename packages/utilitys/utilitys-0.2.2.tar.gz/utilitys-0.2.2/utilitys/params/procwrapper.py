from __future__ import annotations

from functools import singledispatch
from functools import wraps
from typing import List, Sequence, Callable

from pyqtgraph.parametertree import Parameter
from pyqtgraph.parametertree.parameterTypes import GroupParameter

from .prjparam import PrjParam
from .. import fns
from ..misc import CompositionMixin
from ..processing import *

__all__ = ['NestedProcWrapper']

def atomicRunWrapper(proc: AtomicProcess, names: Sequence[str], params: Sequence[Parameter]):
  oldRun = proc.run
  @wraps(oldRun)
  def newRun(io: ProcessIO = None, disable=False, **runKwargs) -> ProcessIO:
    newIo = {name: param.value() for name, param in zip(names, params)}
    proc.input.update(**newIo)
    return oldRun(io, disable, **runKwargs)
  return newRun

def procRunWrapper(proc: NestedProcess, groupParam: Parameter):
  oldRun = proc.run
  @wraps(oldRun)
  def newRun(io: ProcessIO = None, disable=False, **runKwargs):
    proc.disabled = not groupParam.opts['enabled']
    return oldRun(io, disable=disable, **runKwargs)
  return newRun

@singledispatch
def addStageToParam(stage: ProcessStage, parentParam: Parameter, **kwargs):
  pass

@addStageToParam.register
def addAtomicToParam(stage: AtomicProcess, parentParam: Parameter,
                 argNameFormat: Callable[[str], str]=None, **kwargs):
  docParams = fns.docParser(stage.func.__doc__)
  parentParam.setOpts(tip=docParams['top-descr'])
  params: List[Parameter] = []
  for key in stage.input.hyperParamKeys:
    val = stage.input[key]
    curParam = docParams.get(key, None)
    if curParam is None:
      curParam = PrjParam(name=key, value=val)
    else:
      if val is not stage.input.FROM_PREV_IO:
        curParam.value = val
      if curParam.pType is None:
        curParam.pType = type(val).__name__
    paramDict = curParam.toPgDict()
    if argNameFormat is not None and 'title' not in paramDict:
      paramDict['title'] = argNameFormat(key)
    pgParam = fns.getParamChild(parentParam, chOpts=paramDict)
    _hookupCondition(parentParam, pgParam)
    params.append(pgParam)
  stage.run = atomicRunWrapper(stage, stage.input.hyperParamKeys, params)
  return stage

def _hookupCondition(parentParam: Parameter, chParam: Parameter):
  condition = chParam.opts.get('condition', None)
  if not condition:
    return
  _locals = {p.name(): p.value() for p in parentParam}
  if isinstance(condition, str):
    def cndtnCallable():
      exec(f'__out__ = bool({condition})', {}, _locals)
      # noinspection PyUnresolvedReferences
      return _locals['__out__']
  else:
    cndtnCallable = condition
  def onChanged(param, val):
    _locals[param.name()] = val
    if cndtnCallable():
      chParam.show()
    else:
      chParam.hide()

  ch = None
  for ch in parentParam: ch.sigValueChanging.connect(onChanged)
  # Triger in case condition is initially false
  if ch:
    onChanged(ch, ch.value())


@addStageToParam.register
def addNestedToParam(stage: NestedProcess, parentParam: Parameter, nestHyperparams=True,
                     argNameFormat: Callable[[str], str]=None, treatAsAtomic=False, **kwargs):
  if treatAsAtomic:
    collapsed = AtomicProcess(stage.run, stage.name, mainResultKeys=stage.mainResultKeys,
                              mainInputKeys=stage.mainInputKeys)
    collapsed.input = stage.input
    addAtomicToParam(collapsed, parentParam, argNameFormat)
    return
  stage.run = procRunWrapper(stage, parentParam)
  # Special case of a process comprised of just one atomic function
  if len(stage.stages) == 1 and isinstance(stage.stages[0], AtomicProcess):
    # isinstance ensures the type will be correct
    # noinspection PyTypeChecker
    addAtomicToParam(stage.stages[0], parentParam)
    return
  outerParent = parentParam
  for childStage in stage.stages:
    pType = 'atomicgroup'
    if childStage.allowDisable:
      pType = 'procgroup'
    if nestHyperparams:
      paramDict = PrjParam(name=childStage.name, pType=pType, value=[],
                          enabled=not childStage.disabled).toPgDict()
      parentParam = fns.getParamChild(outerParent, chOpts=paramDict)
    else:
      parentParam = outerParent
    addStageToParam(childStage, parentParam)

class NestedProcWrapper(CompositionMixin):
  def __init__(self, processor: ProcessStage, parentParam: GroupParameter=None,
               argNameFormat: Callable[[str], str] = None, treatAsAtomic=False, nestHyperparams=True):
    self.processor = self.exposes(processor)
    self.algName = processor.name
    self.argNameFormat = argNameFormat
    self.treatAsAtomic = treatAsAtomic
    self.nestHyperparams = nestHyperparams
    if parentParam is None:
      parentParam = Parameter.create(name=self.algName, type='group')
    elif nestHyperparams:
      parentParam = fns.getParamChild(parentParam, self.algName)
    self.parentParam : GroupParameter = parentParam
    self.addStage(self.processor)

  def addStage(self, stage: ProcessStage):
    addStageToParam(stage, self.parentParam, argNameFormat=self.argNameFormat,
                    treatAsAtomic=self.treatAsAtomic, nestHyperparams=self.nestHyperparams)

  def setStageEnabled(self, stageIdx: Sequence[str], enabled: bool):
    paramForStage = self.parentParam.child(*stageIdx)
    prevEnabled = paramForStage.opts['enabled']
    if prevEnabled != enabled:
      paramForStage.menuActTriggered('Toggle Enable')

  def __repr__(self) -> str:
    selfCls = type(self)
    oldName: str = super().__repr__()
    # Remove module name for brevity
    oldName = oldName.replace(f'{selfCls.__module__}.{selfCls.__name__}',
                              f'{selfCls.__name__} \'{self.algName}\'')
    return oldName

  @classmethod
  def getNestedName(cls, curProc: ProcessStage, nestedName: List[str]):
    if len(nestedName) == 0 or isinstance(curProc, AtomicProcess):
      return curProc
    # noinspection PyUnresolvedReferences
    for stage in curProc.stages:
      if stage.name == nestedName[0]:
        if len(nestedName) == 1:
          return stage
        else:
          return cls.getNestedName(stage, nestedName[1:])