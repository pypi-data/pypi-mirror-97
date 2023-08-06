#!/usr/bin/env python
# pylint: disable=C0111
from typing import List, Union

from ltpylib import checks, strings


def convert_keys_to_snake_case(
  obj: Union[dict, list],
  recursive: bool = False,
) -> Union[dict, list]:
  if isinstance(obj, list):
    objs = obj
  else:
    objs = [obj]

  for obj_dict in objs:
    dict_items = list(obj_dict.items())
    for key, val in dict_items:
      key_snake_case = strings.to_snake_case(key)
      if key != key_snake_case:
        obj_dict[key_snake_case] = obj_dict.pop(key)

      if recursive and isinstance(val, dict):
        convert_keys_to_snake_case(
          val,
          recursive=recursive,
        )
      elif recursive and isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
        for inner_val in val:
          convert_keys_to_snake_case(
            inner_val,
            recursive=recursive,
          )

  return obj


def convert_string_values_to_correct_type(
  obj: Union[dict, list],
  convert_numbers: bool = True,
  convert_booleans: bool = True,
  use_decimal: bool = False,
  recursive: bool = False,
) -> Union[dict, list]:
  if isinstance(obj, list):
    objs = obj
  else:
    objs = [obj]

  for obj_dict in objs:
    for key, val in obj_dict.items():
      if isinstance(val, str):
        if convert_numbers and strings.is_number(val):
          obj_dict[key] = strings.convert_to_number(val, use_decimal=use_decimal)
        elif convert_booleans and strings.is_boolean(val):
          obj_dict[key] = strings.convert_to_bool(val)
      elif recursive and isinstance(val, dict):
        convert_string_values_to_correct_type(
          val,
          convert_numbers=convert_numbers,
          convert_booleans=convert_booleans,
          use_decimal=use_decimal,
          recursive=recursive,
        )
      elif recursive and isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
        for inner_val in val:
          convert_string_values_to_correct_type(
            inner_val,
            convert_numbers=convert_numbers,
            convert_booleans=convert_booleans,
            use_decimal=use_decimal,
            recursive=recursive,
          )

  return obj


def find(key: str, obj: dict) -> List[dict]:
  if isinstance(obj, dict):
    for k, v in obj.items():
      if k == key:
        yield v
      else:
        for res in find(key, v):
          yield res
  elif isinstance(obj, list):
    for d in obj:
      for res in find(key, d):
        yield res

  # for k, v in obj.items():
  #   if k == key:
  #     yield v
  #   elif isinstance(v, dict):
  #     for res in find(key, v):
  #       yield res
  #   elif isinstance(v, list):
  #     for d in v:
  #       for res in find(key, d):
  #         yield res


def remove_nulls(dict_with_nulls: dict) -> dict:
  return {key: val for (key, val) in dict_with_nulls.items() if val is not None}


def remove_nulls_and_empty(dict_with_nulls: dict) -> dict:
  return {key: val for (key, val) in dict_with_nulls.items() if checks.is_not_empty(val)}


if __name__ == "__main__":
  import sys

  result = globals()[sys.argv[1]](*sys.argv[2:])
  if result is not None:
    print(result)
