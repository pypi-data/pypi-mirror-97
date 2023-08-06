#!/usr/bin/env python
# pylint: disable=C0111
import logging
import re
from pathlib import Path
from typing import Sequence, Union


def should_include(
  test_value: Union[str, Path],
  include_patterns: Sequence[str] = None,
  exclude_patterns: Sequence[str] = None,
  includes: Sequence[str] = None,
  excludes: Sequence[str] = None,
  verbose: bool = False
) -> bool:
  return not should_skip(
    test_value,
    include_patterns=include_patterns,
    exclude_patterns=exclude_patterns,
    includes=includes,
    excludes=excludes,
    verbose=verbose,
  )


def should_skip(
  test_value: Union[str, Path],
  include_patterns: Sequence[str] = None,
  exclude_patterns: Sequence[str] = None,
  includes: Sequence[str] = None,
  excludes: Sequence[str] = None,
  verbose: bool = False
) -> bool:
  if not include_patterns and not exclude_patterns and not includes and not excludes:
    return False

  if isinstance(test_value, str):
    test_str = str(test_value)
  else:
    test_str = test_value.as_posix()

  if excludes and test_str in excludes:
    if verbose:
      logging.info('Excluded: %s', test_str)
    return True

  if includes:
    if test_str in includes:
      if verbose:
        logging.info('Included: %s', test_str)
      return False
    elif not include_patterns:
      return True

  if exclude_patterns:
    for regex in exclude_patterns:
      if re.search(regex, test_str):
        if verbose:
          logging.info('Excluded by pattern: pattern=%s path=%s', regex, test_str)
        return True

  if include_patterns:
    for regex in include_patterns:
      if re.search(regex, test_str):
        if verbose:
          logging.info('Included by pattern: pattern=%s path=%s', regex, test_str)
        return False

    return True

  return False


def should_skip_from_cmds(
  test_value: Union[str, Path],
  include_commands: Sequence[str] = None,
  exclude_commands: Sequence[str] = None,
  verbose: bool = False,
) -> bool:
  from ltpylib import procs

  if not include_commands and not exclude_commands:
    return False

  if isinstance(test_value, str):
    test_str = str(test_value)
  else:
    test_str = test_value.as_posix()

  if exclude_commands:
    for command in exclude_commands:
      result = procs.run(
        command,
        cwd=test_str,
        universal_newlines=True,
        shell=True,
        executable='/usr/local/bin/bash',
      )
      if result.returncode == 0:
        if verbose:
          logging.info('Skipped path: path=%s command=%s', test_str, command)
        return True

  if include_commands:
    for command in include_commands:
      result = procs.run(
        command,
        cwd=test_str,
        universal_newlines=True,
        shell=True,
        executable='/usr/local/bin/bash',
      )
      if result.returncode == 0:
        if verbose:
          logging.info('Included path: path=%s command=%s', test_str, command)
        return False

    return True

  return False


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
