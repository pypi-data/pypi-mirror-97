#!/usr/bin/env python
# pylint: disable=C0111
from typing import List, Union

EMPTY_LIST: frozenset = frozenset([])
EMPTY_MAP: tuple = tuple(sorted({}.items()))


def flatten_list_of_possible_csv_strings(vals: List[str], sep: str = ",") -> List[str]:
  if not vals:
    return vals

  flattened = []
  for val in vals:
    flattened.extend(val.split(sep))

  return flattened


def to_csv(values: Union[List, None], sep: str = ",") -> Union[str, None]:
  return sep.join(values) if values else None
