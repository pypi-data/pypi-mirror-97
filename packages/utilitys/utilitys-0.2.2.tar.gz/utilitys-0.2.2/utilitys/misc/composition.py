import typing as t

T = t.TypeVar('T')
class CompositionMixin:
  _exposedObjs = []

  def __new__(cls, *args, **kwargs):
    obj = super().__new__(cls)
    obj._exposedObjs = []
    return obj

  def exposes(self, obj: T) -> T:
    """Adds methods from *fn* not shadowed by *self* to *self*'s mro"""
    self._exposedObjs.append(obj)
    return obj

  def __getattr__(self, item):
    for obj in self._exposedObjs:
      if hasattr(obj, item):
        return getattr(obj, item)
    # works, and is necessary in case a different base class also defines __getattr__
    # noinspection PyUnresolvedReferences
    return super().__getattr__(item)