#!/usr/bin/env python
import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Union

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = '{message}'
DEFAULT_LOG_STYLE = '{'
LOG_FORMAT_WITH_LEVEL = '{levelname:<8} {message}'
LOG_SEP = '------------------------------------------------'


class StdoutStreamHandler(logging.StreamHandler):

  def __init__(self):
    super().__init__(stream=sys.stdout)

  def handleError(self, record):
    err_type, err_value, traceback = sys.exc_info()
    if err_type == BrokenPipeError:
      exit(0)

    super().handleError(record)


def init_logging(
  verbose: bool = None,
  quiet: bool = None,
  log_level: Union[str, int] = None,
  log_format: str = None,
  args: argparse.Namespace = None,
):
  if args:
    if verbose is None and 'verbose' in args:
      verbose = args.verbose
    if log_level is None and 'log_level' in args:
      log_level = args.log_level
    if log_format is None and 'log_format' in args:
      log_format = args.log_format
    if quiet is None and 'quiet' in args:
      quiet = args.quiet

  if verbose:
    log_level = logging.DEBUG
  elif quiet:
    log_level = logging.WARNING
  elif log_level is not None:
    log_level = log_level
  elif os.environ.get('log_level') is not None:
    log_level = os.environ.get('log_level')
  else:
    log_level = DEFAULT_LOG_LEVEL

  logging.basicConfig(
    level=log_level,
    style=DEFAULT_LOG_STYLE,
    format=(log_format or DEFAULT_LOG_FORMAT),
    handlers=[StdoutStreamHandler()],
  )


def is_debug_enabled():
  return logging.root.isEnabledFor(logging.DEBUG)


def log_sep(debug_only=False):
  if debug_only:
    logging.debug(LOG_SEP)
  else:
    logging.info(LOG_SEP)


def create_path_log_info(path: Path, replace_home_dir: bool = True) -> str:
  output = path.as_posix()

  if replace_home_dir:
    output = output.replace(os.getenv('HOME'), '~', 1)

  return output


def log_with_sep(level: int, msg, *args, **kwargs):
  logging.log(level, LOG_SEP)
  logging.log(level, msg, *args, **kwargs)
  logging.log(level, LOG_SEP)


def log_with_title_sep(level: int, title, msg, *args, **kwargs):
  logging.log(level, title)
  logging.log(level, LOG_SEP)
  logging.log(level, msg, *args, **kwargs)
  logging.log(level, '')


def tail_log_file(file: str, *func_args):
  if shutil.which('multitail'):
    log_cmd = ['multitail']
    mt_conf = Path(os.getenv('DOTFILES') + '/multitail.conf')
    if '-F' not in func_args and mt_conf.is_file():
      log_cmd.extend(['-F', mt_conf.as_posix()])

    if '-CS' not in func_args:
      log_cmd.extend(['-CS', 'l4j'])

    if '-n' not in func_args:
      log_cmd.extend(['-n', '1500'])

  else:
    log_cmd = ['tail', '-1500f']

  if func_args:
    log_cmd.extend(func_args)

  log_cmd.append(file)

  subprocess.check_call(log_cmd, universal_newlines=True)


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
