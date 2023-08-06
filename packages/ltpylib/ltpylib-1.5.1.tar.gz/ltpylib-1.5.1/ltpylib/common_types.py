#!/usr/bin/env python


class TypeWithDictRepr(object):

  def __repr__(self) -> str:
    return str(self.__dict__)

  def as_dict(self) -> dict:
    return dict(self.__dict__)


class DataWithUnknownProperties(TypeWithDictRepr):

  def __init__(self, values: dict = None, skip_field_if_no_unknown: bool = False):
    if not skip_field_if_no_unknown or values:
      self.unknown_properties: dict = values if values else None


class DataWithUnknownPropertiesAsAttributes(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    if values:
      self._has_unknown_properties: bool = True
      for item in values.items():
        setattr(self, str(item[0]), item[1])

      values.clear()

    DataWithUnknownProperties.__init__(self, values=None, skip_field_if_no_unknown=True)

  @property
  def has_unknown_properties(self) -> bool:
    return getattr(self, "_has_unknown_properties", False)
