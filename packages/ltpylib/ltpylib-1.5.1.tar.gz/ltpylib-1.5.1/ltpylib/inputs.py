#!/usr/bin/env python
import logging
import os
import subprocess
import sys
from typing import List, Sequence

from ltpylib import procs, strings
from ltpylib.strings import strip_color_codes


def confirm(question: str = 'Continue?', default: str = None) -> bool:
  """Ask a yes/no question via raw_input() and return their answer.

  "question" is a string that is presented to the user.
  "default" is the presumed answer if the user just hits <Enter>.
      It must be "yes" (the default), "no" or None (meaning
      an answer is required of the user).

  The "answer" return value is True for "yes" or False for "no".
  """
  valid = {
    "yes": True,
    "y": True,
    "ye": True,
    "no": False,
    "n": False,
  }
  if default is None:
    prompt = "\n[y/n]> "
  elif default == "yes" or default == "y":
    prompt = "\n[Y/n]> "
  elif default == "no" or default == "n":
    prompt = "\n[y/N]> "
  else:
    raise ValueError("invalid default answer: '%s'" % default)

  while True:
    choice = input(question + prompt).lower()
    if default is not None and choice == '':
      return valid[default]
    elif choice in valid:
      return valid[choice]
    else:
      logging.error("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def confirm_default_yes(question: str = 'Continue?') -> bool:
  return confirm(question=question, default="y")


def check_auto_confirm() -> bool:
  auto_confirm = os.getenv("auto_confirm")
  return auto_confirm is not None and strings.is_boolean(auto_confirm) and strings.convert_to_bool(auto_confirm)


def ask_for_input(prompt: str = 'Please input value.') -> str:
  return input(prompt + '\n> ')


def create_fzf_select_prompt_command(
  header: str = None,
  no_sort: bool = True,
  layout: str = "reverse",
  multi: bool = False,
  ansi: bool = False,
) -> List[str]:
  command = [
    'fzf',
    '--layout',
    layout,
  ]

  if header:
    command.extend(['--header', header])

  if no_sort:
    command.append('--no-sort')

  if multi:
    command.append('--multi')

  if ansi:
    command.append('--ansi')

  return command


def select_prompt(
  choices: Sequence[str],
  header: str = None,
  no_sort: bool = True,
  layout: str = "reverse",
  multi: bool = False,
  ansi: bool = False,
) -> str:
  command = create_fzf_select_prompt_command(
    header=header,
    no_sort=no_sort,
    layout=layout,
    multi=multi,
    ansi=ansi,
  )

  result: subprocess.CompletedProcess = procs.run(
    command,
    universal_newlines=True,
    stderr=sys.stderr,
    input="\n".join(choices),
  )

  if result.returncode == 130:
    raise KeyboardInterrupt

  result.check_returncode()
  return result.stdout.strip()


def select_prompt_and_return_indexes(
  choices: Sequence[str],
  header: str = None,
  multi: bool = False,
  ansi: bool = False,
) -> List[int]:
  selections = select_prompt(
    choices,
    header=header,
    no_sort=True,
    layout="reverse",
    multi=multi,
    ansi=ansi,
  ).splitlines(keepends=False)

  choices_without_colors = [strip_color_codes(choice) for choice in choices]

  return [choices_without_colors.index(item) for item in selections]


def select_prompt_old(
  choices: Sequence[str],
  message: str = None,
  bottom_message: str = None,
  max_width: int = None,
) -> str:
  command = ['select_prompt']

  if message:
    command.extend(['--message', message])

  if bottom_message:
    command.extend(['--bottom-message', message])

  if max_width:
    command.extend(['--max-width', str(max_width)])

  command.extend(choices)

  result: subprocess.CompletedProcess = procs.run(
    command,
    universal_newlines=True,
    stderr=sys.stderr,
  )
  if result.returncode == 130:
    raise KeyboardInterrupt

  result.check_returncode()
  return result.stdout.strip()


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
