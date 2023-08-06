#!/usr/bin/env python

import logging
import re
from pathlib import Path
from typing import List, Sequence, Pattern, Match, Callable, Union

from ltpylib import files, logs

SKIP_FILE_REGEX: Pattern = re.compile(r"^[^a-zA-Z0-9]*template:skip\s*$")
START_REGEX = re.compile(r"^[^a-zA-Z0-9]*template:start (.*?)$")
END_REGEX = re.compile(r"^[^a-zA-Z0-9]*template:end\s*$")
DEFAULT_CANDIDATE_FILES_GLOBS: Sequence[str] = ('**/*',)
DEFAULT_TEMPLATE_FILES_GLOBS: Sequence[str] = ('**/*.template.*',)


def replace_templates_in_files(
  candidate_files_dir: Path,
  template_dir: Path,
  candidate_files_globs: List[str] = DEFAULT_CANDIDATE_FILES_GLOBS,
  template_files_globs: List[str] = DEFAULT_TEMPLATE_FILES_GLOBS,
  debug_mode: bool = False,
  force_replace: bool = False
) -> bool:
  candidate_files: List[Path] = files.filter_files_with_matching_line(
    files.list_files(candidate_files_dir, candidate_files_globs),
    [SKIP_FILE_REGEX],
    check_n_lines=2,
  )
  if not candidate_files:
    logging.warning("No candidate files found: candidate_files_dir=%s candidate_files_globs=%s", candidate_files_dir.as_posix(), candidate_files_globs)
    return False

  logs.log_with_title_sep(logging.DEBUG, 'Candidate Files', '\n'.join([file.absolute().as_posix() for file in candidate_files]))

  template_files: List[Path] = files.list_files(template_dir, template_files_globs)
  if not template_files:
    logging.warning("No template files found: template_dir=%s template_files_globs=%s", template_dir.as_posix(), template_files_globs)
    return False

  logs.log_with_title_sep(logging.DEBUG, 'Template Files', '\n'.join([file.absolute().as_posix() for file in template_files]))

  for template_file in template_files:
    replace_template(candidate_files, template_file, debug_mode=debug_mode, force_replace=force_replace)

  return True


def replace_template(candidate_files: List[Path], template_file: Path, debug_mode: bool = False, force_replace: bool = False):
  template_file_content: str = files.read_file(template_file)

  lines = []
  found_start = False
  search_string: str = ''

  for line in template_file_content.splitlines():
    if found_start:
      if END_REGEX.fullmatch(line):
        break

      lines.append(line)
    elif START_REGEX.fullmatch(line):
      found_start = True
      search_string = START_REGEX.fullmatch(line).group(1)

  if not lines or not search_string:
    logging.error('Something went wrong, skipping template: template_file=%s lines_count=%s search_string=%s', template_file.as_posix(), len(lines), search_string)
    return

  replacement_str: str = '\n'.join(lines)
  replacement: Union[str, Callable[[Match], str]] = replacement_str

  search_string_groups = re.compile(search_string).groups
  if search_string_groups > 0:

    def repl(match: Match) -> str:
      groups = match.groupdict()
      repl_string = ""
      if "start" in groups:
        repl_string += groups.get("start")

      repl_string += replacement_str

      if "end" in groups:
        repl_string += groups.get("end")

      return repl_string

    replacement = repl

  logs.log_with_title_sep(logging.DEBUG, 'template_file', template_file.as_posix())
  logs.log_with_title_sep(logging.DEBUG, 'search_string', search_string)
  logs.log_with_title_sep(logging.DEBUG, 'replacement_str', replacement_str)

  if not debug_mode:
    for file in candidate_files:
      if file.absolute().as_posix() == template_file.absolute().as_posix():
        continue

      if files.replace_matches_in_file(file, search_string, replacement, quote_replacement=False, force_replace=force_replace):
        logging.info("Replaced template: %s -> %s", template_file.as_posix(), file.as_posix())


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
