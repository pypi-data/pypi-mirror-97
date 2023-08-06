#!/usr/bin/env python
import re
from pathlib import Path
from typing import List, Union
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import xmltodict

from ltpylib import files, procs


def xq(file: Union[str, Path], expr: str, remove_null: bool = True, raw_output: bool = True) -> str:
  if isinstance(file, str):
    file = Path(file)

  xq_command: List[str] = ['xq']

  if remove_null:
    expr += ' | select (.!=null)'

  if raw_output:
    xq_command.append('--raw-output')

  xq_command.extend([expr, file.as_posix()])

  result: str = procs.run_and_parse_output(xq_command, check=True)[1].strip()

  if result == "":
    return None

  return result


def parse_xml_to_dict(file: Union[str, Path]) -> dict:
  if isinstance(file, str):
    file = Path(file)

  with open(file.as_posix()) as fd:
    return xmltodict.parse(fd.read())


def parse_xml(file: Union[str, Path], remove_namespace: bool = True) -> Element:
  if isinstance(file, str):
    file = Path(file)

  if remove_namespace:
    xml_string: str = re.sub(' xmlns="[^"]+"', '', files.read_file(file), count=1)
    return ElementTree.fromstring(xml_string)

  return ElementTree.parse(file.as_posix()).getroot()


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
