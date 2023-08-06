#!/usr/bin/env python

import logging
import subprocess
from pathlib import Path
from typing import List, Union

from ltpylib import files, procs


def prettify(
  files_to_prettify: Union[Path, List[Path]],
  type: str = None,
  debug_mode: bool = False,
  verbose: bool = False,
):
  if not isinstance(files_to_prettify, list):
    files_to_prettify = [files_to_prettify]

  for file in files_to_prettify:
    if type:
      file_type = type
    else:
      file_type = file.suffix[1:]

    func_for_type = globals()["prettify_" + file_type + "_file"]
    if not callable(func_for_type):
      raise ValueError("Unsupported file type: file=%s type=%s" % (file.as_posix(), file_type))

    func_for_type(file, debug_mode=debug_mode, verbose=verbose)
    if verbose:
      logging.debug("Updated %s", file.as_posix())


def prettify_html_file(
  file: Path,
  debug_mode: bool = False,
  verbose: bool = False,
):
  tidy_args = [
    "tidy",
    "-icm",
    "-wrap",
    "200",
    "--doctype",
    "omit",
    "--indent",
    "yes",
    "--vertical-space",
    "no",
  ]

  if not verbose:
    tidy_args.extend([
      "-quiet",
      "--show-warnings",
      "no",
    ])

  tidy_args.append(file.as_posix())

  result = procs.run(tidy_args)
  check_proc_result(file, result, should_have_stdout=False, allow_exit_codes=[0, 1])


def prettify_json_file(
  file: Path,
  debug_mode: bool = False,
  verbose: bool = False,
):
  result = procs.run(["jq", "--sort-keys", ".", file.as_posix()])
  check_proc_result(file, result)
  files.write_file(file, result.stdout)


def prettify_xml_file(
  file: Path,
  debug_mode: bool = False,
  verbose: bool = False,
):
  result = procs.run(["xmllint", "--format", file.as_posix()])
  check_proc_result(file, result)
  files.write_file(file, result.stdout)


def prettify_yaml_file(
  file: Path,
  debug_mode: bool = False,
  verbose: bool = False,
):
  result = procs.run(["yq", "--yaml-roundtrip", "--indentless-lists", "--sort-keys", ".", file.as_posix()])
  check_proc_result(file, result)
  files.write_file(file, result.stdout)


def check_proc_result(file: Path, result: subprocess.CompletedProcess, should_have_stdout: bool = True, allow_exit_codes: List[int] = None):
  exit_code = result.returncode
  proc_succeeded = exit_code == 0
  if allow_exit_codes and exit_code in allow_exit_codes:
    proc_succeeded = True

  if should_have_stdout and not result.stdout:
    raise Exception("Issue prettifying file: file=%s status=%s stderr=%s" % (file.as_posix(), exit_code, result.stderr))

  if result.stderr:
    if proc_succeeded:
      logging.warning(result.stderr)
    else:
      raise Exception("Issue prettifying file: file=%s status=%s stderr=%s stdout=%s" % (file.as_posix(), exit_code, result.stderr, result.stderr))

  if not proc_succeeded:
    result.check_returncode()
