#!/usr/bin/env python
# pylint: disable=C0111

import re
import urllib.parse as urllib_parse
from typing import Callable, List

StrConverter = Callable[[str], str]

SEARCH_SEP_CHARS: List[str] = [
  " ",
  "_",
  "-",
  ".",
]


def stripper(val: str) -> str:
  return val.strip()


def lower_case(val: str) -> str:
  return val.lower()


def alphanum_only(val: str) -> str:
  return re.sub(r'[^a-zA-Z0-9]', '', val)


def num_only(val: str) -> str:
  return re.sub(r'[^0-9.]', '', val)


def url_encode(val: str) -> str:
  return urllib_parse.quote_plus(val)


def url_decode(val: str) -> str:
  return urllib_parse.unquote_plus(val)


def dict_to_url_params(params: dict) -> str:
  return urllib_parse.urlencode(params)


def to_camel_case(val: str, sep: str = None) -> str:
  if not val:
    return val

  if sep is None:
    if val.count(" ") > 0:
      sep = " "
    else:
      count: int = -1
      for sep_char in SEARCH_SEP_CHARS:
        sep_char_count = val.count(sep_char)
        if sep_char_count > count:
          count = sep_char_count
          sep = sep_char

  val = re.sub(r'[^a-zA-Z0-9 ]', ' ', val.lower().replace(sep, " ")).title()
  return (val[0:1].lower() + val[1:]).replace(" ", "")


def to_snake_case(val: str, sep: str = None) -> str:
  if not val:
    return val

  if sep is None:
    if val.count(" ") > 0:
      sep = " "
    else:
      count: int = -1
      for sep_char in SEARCH_SEP_CHARS:
        sep_char_count = val.count(sep_char)
        if sep_char_count > count:
          count = sep_char_count
          sep = sep_char

  val = re.sub(r'[^a-zA-Z0-9 ]', ' ', val.lower().replace(sep, " "))
  return "_".join(val.lower().split())


def _main():
  import sys

  result = globals()[sys.argv[1]](*sys.argv[2:])
  if result is not None:
    print(result)


if __name__ == "__main__":
  try:
    _main()
  except KeyboardInterrupt:
    exit(130)
