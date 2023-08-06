#!/usr/bin/env python
# pylint: disable=C0111
import inspect
from typing import ClassVar, List, Tuple

SIMPLE_TYPES: Tuple[type] = (str, bool, int, float)


def create_typing_description(val) -> str:
  if isinstance(val, list):
    if len(val) == 0:
      return "List[str]"
    else:
      return "List[%s]" % create_typing_description(val[0])
  else:
    return type_name(val)


def type_name(val) -> str:
  return type(val).__name__


def get_functions_of_class(
  inspect_class: ClassVar,
  include_private: bool = False,
  include_signature: bool = False,
) -> List[str]:
  result: List[str] = []
  functions = inspect.getmembers(inspect_class, predicate=inspect.isfunction)
  for func in functions:
    if not include_private and func[0].startswith("_"):
      continue

    func_info: str = func[0]

    if include_signature:
      func_sig: str = str(inspect.signature(func[1])).replace("(self, ", "(", 1).replace("(self)", "()", 1)
      func_info += func_sig

    result.append(func_info)

  return result
