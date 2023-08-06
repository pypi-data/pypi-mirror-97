#!/usr/bin/env python
# pylint: disable=C0111


def is_empty(val) -> bool:
  if val is None:
    return True

  if isinstance(val, (dict, list)):
    return not val

  return False


def is_not_empty(val) -> bool:
  return not is_empty(val)
