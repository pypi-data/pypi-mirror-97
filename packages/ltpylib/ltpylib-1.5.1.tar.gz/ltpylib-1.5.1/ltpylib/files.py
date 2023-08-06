#!/usr/bin/env python
# pylint: disable=C0111
import itertools
import json
import os
import re
from pathlib import Path
from typing import AnyStr, Callable, List, Match, Pattern, Sequence, Set, Tuple, Union

# NB: replacement matching groups should be in the \1 format instead of $1
from ltpylib import strings


def convert_to_path(path: Union[Path, str]) -> Path:
  if isinstance(path, str):
    return Path(path)

  return path


def replace_matches_in_file(
  file: Union[str, Path],
  search_string: str,
  replacement: Union[str, Callable[[Match], str]],
  quote_replacement: Union[bool, str] = False,
  wrap_replacement_in_function: Union[bool, str] = False,
  force_replace: bool = False,
  flags: Union[int, re.RegexFlag] = 0,
) -> bool:
  if isinstance(quote_replacement, str):
    quote_replacement = strings.convert_to_bool(quote_replacement)

  if isinstance(wrap_replacement_in_function, str):
    wrap_replacement_in_function = strings.convert_to_bool(wrap_replacement_in_function)

  if isinstance(force_replace, str):
    force_replace = strings.convert_to_bool(force_replace)

  if isinstance(flags, str):
    flags = strings.convert_to_number(flags)

  if quote_replacement and isinstance(replacement, str):
    replacement = re.escape(replacement)
  elif wrap_replacement_in_function and isinstance(replacement, str):
    replacement_content = replacement

    def replacement_function(match: Match) -> str:
      return replacement_content

    replacement = replacement_function

  content = read_file(file)
  content_new = re.sub(search_string, replacement, content, flags=flags)

  if content != content_new:
    write_file(file, content_new)
    return True
  elif force_replace and re.search(search_string, content, flags=flags):
    write_file(file, content_new)
    return True

  return False


def replace_strings_in_file(
  file: Union[str, Path],
  search_string: str,
  replacement: str,
  count: int = -1,
  force_replace: bool = False,
) -> bool:
  if isinstance(count, str):
    count = strings.convert_to_number(count)

  if isinstance(force_replace, str):
    force_replace = strings.convert_to_bool(force_replace)

  content: str = read_file(file)
  content_new = content.replace(search_string, replacement, count)

  if content != content_new:
    write_file(file, content_new)
    return True
  elif force_replace and search_string in content:
    write_file(file, content_new)
    return True

  return False


def remove_matching_lines_in_file(
  file: Union[str, Path],
  search_string: str,
  quote_search_string: bool = False,
  flags: Union[int, re.RegexFlag] = 0,
) -> bool:
  if isinstance(quote_search_string, str):
    quote_search_string = strings.convert_to_bool(quote_search_string)

  if isinstance(flags, str):
    flags = strings.convert_to_number(flags)

  if quote_search_string:
    search_string = re.escape(search_string)

  content: str = read_file(file)
  matcher = re.compile(search_string, flags=flags)
  has_match = False
  new_lines = []
  for line in content.splitlines():
    if matcher.search(line):
      has_match = True
    else:
      new_lines.append(line)

  if has_match:
    write_file(file, "\n".join(new_lines))
    return True

  return False


def chmod_proc(perms: str, file: Union[str, Path]) -> int:
  import subprocess

  file = convert_to_path(file)

  return subprocess.call(["chmod", perms, file.as_posix()])


def read_file(file: Union[str, Path]) -> AnyStr:
  file = convert_to_path(file)

  with open(file.as_posix(), 'r') as fr:
    content = fr.read()
  return content


def read_json_file(file: Union[str, Path]) -> Union[dict, list]:
  file = convert_to_path(file)

  with open(file.as_posix(), 'r') as fr:
    loaded_json = json.load(fr)
  return loaded_json


def read_file_n_lines(file: Union[str, Path], n_lines: int = -1) -> List[str]:
  file = convert_to_path(file)

  lines: List[str] = []
  with open(file.as_posix()) as fr:
    if n_lines < 0:
      while True:
        line = fr.readline()
        if not line:
          break
        lines.append(line.rstrip('\n'))
    else:
      for n in range(n_lines):
        line = fr.readline()
        if not line:
          break
        lines.append(line.rstrip('\n'))

  return lines


def write_file(file: Union[str, Path], contents: AnyStr):
  file = convert_to_path(file)

  with open(file.as_posix(), 'w') as fw:
    fw.write(contents)


def append_file(file: Union[str, Path], contents: AnyStr):
  file = convert_to_path(file)

  with open(file.as_posix(), 'a') as fw:
    fw.write(contents)


def list_files(base_dir: Path, globs: List[str] = ('**/*',)) -> List[Path]:
  files: Set[Path] = set()
  file: Path = None
  for file in list(itertools.chain(*[base_dir.glob(glob) for glob in globs])):
    if file.is_file():
      files.add(file)

  files_list = list(files)
  files_list.sort()
  return files_list


def list_dirs(base_dir: Path, globs: List[str] = ('**/*',)) -> List[Path]:
  dirs: Set[Path] = set()
  child_dir: Path = None
  for child_dir in list(itertools.chain(*[base_dir.glob(glob) for glob in globs])):
    if child_dir.is_dir():
      dirs.add(child_dir)

  dirs_list = list(dirs)
  dirs_list.sort()
  return dirs_list


def filter_files_with_matching_line(files: List[Union[str, Path]], regexes: List[Union[str, Pattern]], check_n_lines: int = 1) -> List[Path]:
  filtered: List[Path] = []
  for file in files:
    lines = read_file_n_lines(file, check_n_lines)
    has_match = False
    for line in lines:
      for regex in regexes:
        if re.search(regex, line):
          has_match = True
          break

      if has_match:
        break

    if not has_match:
      filtered.append(file)

  return filtered


def find_children(
  base_dir: Union[Path, str],
  break_after_match: bool = False,
  max_depth: int = -1,
  include_dirs: bool = True,
  include_files: bool = True,
  match_absolute_path: bool = False,
  include_patterns: Sequence[str] = None,
  exclude_patterns: Sequence[str] = None,
  includes: Sequence[str] = None,
  excludes: Sequence[str] = None,
  recursion_include_patterns: Sequence[str] = None,
  recursion_exclude_patterns: Sequence[str] = None,
  recursion_includes: Sequence[str] = None,
  recursion_excludes: Sequence[str] = None
) -> List[Path]:
  if isinstance(base_dir, str):
    top = str(base_dir)
  else:
    top = base_dir.as_posix()

  found_dirs = []
  return _find_children(
    top,
    found_dirs,
    1,
    break_after_match,
    max_depth,
    include_dirs,
    include_files,
    match_absolute_path,
    include_patterns,
    exclude_patterns,
    includes,
    excludes,
    recursion_include_patterns,
    recursion_exclude_patterns,
    recursion_includes,
    recursion_excludes
  )[1]


def _find_children(
  top: str,
  found_dirs: List[Path],
  current_depth: int,
  break_after_match: bool,
  max_depth: int,
  include_dirs: bool,
  include_files: bool,
  match_absolute_path: bool,
  include_patterns: Sequence[str],
  exclude_patterns: Sequence[str],
  includes: Sequence[str],
  excludes: Sequence[str],
  recursion_include_patterns: Sequence[str],
  recursion_exclude_patterns: Sequence[str],
  recursion_includes: Sequence[str],
  recursion_excludes: Sequence[str]
) -> Tuple[bool, List[Path]]:
  from ltpylib import filters

  found_match = False
  scandir_it = os.scandir(top)
  dirs = []

  with scandir_it:
    while True:
      try:
        try:
          entry = next(scandir_it)
        except StopIteration:
          break
      except OSError:
        return found_match, found_dirs

      try:
        is_dir = entry.is_dir()
      except OSError:
        # If is_dir() raises an OSError, consider that the entry is not
        # a directory, same behaviour than os.path.isdir().
        is_dir = False

      if is_dir and not include_dirs:
        continue
      elif not is_dir and not include_files:
        continue

      child = entry.name
      full_path = os.path.join(top, child)
      test_value = child if not match_absolute_path else full_path
      include = filters.should_include(
        test_value,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        includes=includes,
        excludes=excludes,
      )

      if include:
        found_match = True
        found_dirs.append(Path(full_path))
        if break_after_match:
          break

      if is_dir:
        include_child = filters.should_include(
          test_value,
          include_patterns=recursion_include_patterns,
          exclude_patterns=recursion_exclude_patterns,
          includes=recursion_includes,
          excludes=recursion_excludes,
        )
        if include_child:
          dirs.append(child)

  if (max_depth <= -1 or current_depth < max_depth) and (not found_match or not break_after_match):
    for dirname in dirs:
      _find_children(
        os.path.join(top, dirname),
        found_dirs,
        current_depth + 1,
        break_after_match,
        max_depth,
        include_dirs,
        include_files,
        match_absolute_path,
        include_patterns,
        exclude_patterns,
        includes,
        excludes,
        recursion_include_patterns,
        recursion_exclude_patterns,
        recursion_includes,
        recursion_excludes
      )

  return found_match, found_dirs


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
