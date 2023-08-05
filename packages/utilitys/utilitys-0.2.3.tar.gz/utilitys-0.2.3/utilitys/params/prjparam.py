from __future__ import annotations

import html
from typing import Optional, Collection, Sequence

import numpy as np

_specialKeys = ['name', 'value', 'helpText', 'pType']
class _UNSPECIFIED_DEFAULT: pass
class PrjParam:
  def __init__(self, name: str, value=None, pType: Optional[str]=None, helpText='',
               **opts):
    """
    Encapsulates parameter information use within the main application

    :param name: Display name of the parameter
    :param value: Initial value of the parameter. This is used within the program
      to infer parameter type, shape, comparison methods, etc.
    :param pType: Type of the variable if not easily inferrable from the value itself.
      For instance, class:`FRShortcutParameter<s3a.views.parameditors.FRShortcutParameter>`
      is indicated with string values (e.g. 'Ctrl+D'), so the user must explicitly specify
      that such an :class:`PrjParam` is of type 'shortcut' (as defined in
      :class:`FRShortcutParameter<s3a.views.parameditors.FRShortcutParameter>`)
      If the type *is* easily inferrable, this may be left blank.
    :param helpText: Additional documentation for this parameter.
    :param opts: Additional options associated with this parameter
    """
    if opts is None:
      opts = {}
    if pType is None:
      # Infer from value
      pType = type(value).__name__.lower()
    ht = helpText or opts.get('tip', None)
    if ht:
      # TODO: Checking for mightBeRichText fails on pyside2? Even though the function
      # is supposed to exist?
      ht = html.escape(ht)
      # Makes sure the label is displayed as rich text
      helpText = f'<qt>{ht}</qt>'
    self.name = name
    self.value = value
    self.pType = pType
    self.helpText = helpText
    self.opts = opts

    self.group: Optional[Collection[PrjParam]] = None
    """
    PrjParamGroup to which this parameter belongs, if this parameter is part of
      a group. This is set by the PrjParamGroup, not manually
    """

  def toPgDict(self):
    """
    Simple conversion function from PrjParams used internally to the dictionary form expected
    by pyqtgraph parameters
    """
    opts = self.opts.copy()
    opts.pop('type', 'name')
    paramOpts = dict(name=self.name, type=self.pType,
                     **opts)
    if len(self.helpText) > 0 and not paramOpts.get('tip', None):
      paramOpts['tip'] = self.helpText
    if self.pType == 'group' and self.value is not None:
      paramOpts.update(children=self.value)
    else:
      paramOpts.update(value=self.value)
    return paramOpts

  def __str__(self):
    return f'{self.name}'

  def __repr__(self):
    return f'{self.name}: <{self.pType}>'

  def __lt__(self, other):
    """
    Required for sorting by value in component table. Defer to alphabetic
    sorting
    :param other: Other :class:`PrjParam` member for comparison
    :return: Whether `self` is less than `other`
    """
    return str(self) < str(other)

  def __eq__(self, other):
    # TODO: Highly naive implementation. Be sure to make this more robust if it needs to be
    #   for now assume only other prjparamss will be passed in
    return repr(self) == repr(other)

  def __hash__(self):
    # Since every param within a group will have a unique name, just the name is
    # sufficient to form a proper hash
    return hash(self.name,)

  def toNumeric(self, data: Sequence, offset:bool=None, rescale=False, returnUnique=False):
    """
    Useful for converting string-like or list-like parameters to integer representations.
    If self's `value` is non-numeric data (e.g. strings):
       - First, the parameter is searched for a 'limits' property. This will contain all
         possible values this field could be.
       - If no limits exist, unique values in the input data will be considered the
         limits
    :param data: Array-like data to be turned into numeric values according to the parameter type
    :param offset: Whether to offset entries (increment all numeric outputs by 1). This
      is useful when 0 is indicative of e.g. a background label, but also the numeric
      value corresponding to the first possible set entry. If `offset` is *True*, output
      values will be incremented by 1 as described. If *False*, they won't. If *None*,
      offset will be applied depending on the parameter type. If already numeric, no offset
      will be applied. Otherwise, `offset` will be *True*.
    :param rescale: If *True*, values will be rescaled to the range 0-1. `offset` is ignored
      in that case.
    :param returnUnique: Whether to also return an array of the unique values within `data`.
      If data is already numeric, *None* is returned instead of this array.
   """
    numericVals = np.asarray(data).copy()
    if numericVals.size == 0:
      return numericVals
    if not np.issubdtype(type(self.value), np.number):
      if offset is None:
        offset = True
      # Check for limits that indicate the exhaustive list of possible values.
      # Otherwise, just use the unique values of this set as the limits
      if 'limits' in self.opts:
        listLims = list(self.opts['limits'])
        numericVals = np.array([listLims.index(v) for v in numericVals])
      else:
        listLims, numericVals = np.unique(numericVals, return_inverse=True)
    else:
      listLims = None
    if offset and not rescale:
      numericVals += 1
    if rescale:
      maxVal = len(listLims) if listLims is not None else np.max(data)
      if maxVal > 0:
        # Can't use /= since dtype may change
        numericVals =  numericVals / maxVal
    if returnUnique:
      return numericVals, listLims
    return numericVals

  def __getitem__(self, item):
    if item in _specialKeys:
      return getattr(self, item)
    return self.opts[item]

  def __setitem__(self, key, value):
    if key in _specialKeys:
      setattr(self, key, value)
    else:
      self.opts[key] = value

  def get(self, item, default=_UNSPECIFIED_DEFAULT):
    try:
      return self[item]
    except KeyError:
      if default is _UNSPECIFIED_DEFAULT:
        raise
      return default

  def keys(self):
    return list(self.opts.keys()) + _specialKeys

  def __contains__(self, item):
    return item in _specialKeys or item in self.opts

  def addHelpText(self, prependText='', postfixText='', replace=True):
    # Outside <qt> tags
    helpText = self.helpText
    if helpText.startswith('<qt>'):
      unwrappedHelpText = helpText[4:-5]
    else:
      unwrappedHelpText = helpText
    if len(prependText) > 0 and len(helpText) > 0 or len(postfixText) > 0:
      prependText += '<br>'
    curText = prependText + unwrappedHelpText
    if len(postfixText) > 0:
      curText += '<br>' + postfixText
    newHelpText = f'<qt>{curText}</qt>'
    if replace:
      self.helpText = newHelpText
    return newHelpText