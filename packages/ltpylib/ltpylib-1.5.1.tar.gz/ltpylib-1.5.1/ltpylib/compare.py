#!/usr/bin/env python
import os
import tempfile

from ltpylib import files, procs


def diff_git(initial: str, updated: str, add_suffix: str = None):
  suffix_prefix = ('.' + add_suffix) if add_suffix else ''

  ifd, initial_temp_file = tempfile.mkstemp(suffix=suffix_prefix + '.initial')
  ufd, updated_temp_file = tempfile.mkstemp(suffix=suffix_prefix + '.updated')
  os.close(ifd)
  os.close(ufd)

  files.write_file(initial_temp_file, initial)
  files.write_file(updated_temp_file, updated)

  result = procs.run(
    [
      'git',
      'diff',
      '--color=always',
      '--no-index',
      '--color-words',
      '-w',
      initial_temp_file,
      updated_temp_file,
    ],
    check=False,
  )

  os.remove(initial_temp_file)
  os.remove(updated_temp_file)

  return result.stdout
