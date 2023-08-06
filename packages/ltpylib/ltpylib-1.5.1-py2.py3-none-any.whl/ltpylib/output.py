#!/usr/bin/env python
import json
import os

from typing import List, Sequence, Union

from ltpylib.common_types import TypeWithDictRepr


def colorize_json(json_data: Union[str, dict, Sequence], pygments_style: str = None) -> Union[bytes, str]:
  import pygments
  from pygments.formatters.terminal import TerminalFormatter
  from pygments.formatters.terminal256 import Terminal256Formatter
  from pygments.lexers.data import JsonLexer

  if not pygments_style:
    pygments_style = os.getenv("PYGMENTS_STYLE", "solarized-light")

  return pygments.highlight(
    json_data if isinstance(json_data, str) or json_data is None else prettify_json(json_data, colorize=False),
    JsonLexer(),
    Terminal256Formatter(style=pygments_style) if '256' in os.environ.get('TERM', '') else TerminalFormatter(style=pygments_style),
  )


def is_output_to_terminal() -> bool:
  import sys

  return sys.stdout.isatty()


def prettify_json(obj, remove_nulls: bool = False, colorize: bool = False) -> str:
  if remove_nulls:
    from ltpylib import dicts

    obj = json.loads(
      prettify_json(obj, remove_nulls=False, colorize=False),
      object_hook=dicts.remove_nulls_and_empty,
    )
  output = json.dumps(
    obj,
    sort_keys=True,
    indent='  ',
    default=lambda x: getattr(x, '__dict__', str(x)),
  )

  if colorize:
    output = colorize_json(output)

  return output


def prettify_json_remove_nulls(obj) -> str:
  return prettify_json(obj, remove_nulls=True)


def dicts_to_csv(data: List[dict], showindex: bool = False) -> str:
  from pandas import DataFrame

  data_frame = DataFrame(data)
  return data_frame.to_csv(index=showindex)


def dicts_to_markdown_table(data: Union[List[dict], List[TypeWithDictRepr]], showindex: bool = False, tablefmt: str = "github") -> str:
  import tabulate

  from pandas import DataFrame

  if len(data) > 0 and isinstance(data[0], TypeWithDictRepr):
    data_as_class: List[TypeWithDictRepr] = data
    data = [val.as_dict() for val in data_as_class]

  data_frame = DataFrame(data)
  return tabulate.tabulate(
    data_frame,
    showindex=showindex,
    headers=data_frame.columns,
    tablefmt=tablefmt,
  )


def sort_csv_rows(rows: List[str]) -> List[str]:
  return [rows[0]] + sorted(rows[1:])
