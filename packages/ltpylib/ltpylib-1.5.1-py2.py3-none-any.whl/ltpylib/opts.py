#!/usr/bin/env python
import argparse
import os
from pathlib import Path
from typing import Callable, List, Optional, Sequence

from ltpylib.common_types import TypeWithDictRepr
from ltpylib.opts_actions import APPEND, STORE_TRUE
from ltpylib.output import is_output_to_terminal

TRUE_VALUES = ["true", "1", "t", "yes", "y"]
DEFAULT_POSITIONALS_KEY = "command"


class PositionalsHelpFormatter(argparse.HelpFormatter):

  def __init__(
    self,
    prog,
    indent_increment=2,
    max_help_position=24,
    width=None,
    positionals_key: str = DEFAULT_POSITIONALS_KEY,
  ):
    super().__init__(prog, indent_increment, max_help_position, width)
    self.positionals_key = positionals_key
    self.positionals_action = argparse._StoreAction([], self.positionals_key, nargs="+")

  def add_usage(self, usage, actions, groups, prefix=None):
    from itertools import chain

    super().add_usage(usage, chain(actions, [self.positionals_action]), groups, prefix)

  def add_arguments(self, actions):
    from itertools import chain

    if self._current_section.heading == "positional arguments":
      super().add_arguments(chain(actions, [self.positionals_action]))
    else:
      super().add_arguments(actions)


class ActionPathValidate(argparse.Action):

  def __init__(self, option_strings, dest, type=None, **kwargs):
    if type is not None:
      raise ValueError("type not allowed")

    super(ActionPathValidate, self).__init__(option_strings=option_strings, dest=dest, type=Path, **kwargs)

  def __call__(self, parser, namespace, value: Path, option_string=None):
    setattr(namespace, self.dest, value)

    if value is not None:
      if not value.exists():
        raise ValueError("Supplied Path does not exist: %s" % (value.as_posix()))


class ActionPathsValidate(argparse._AppendAction):

  def __init__(self, option_strings, dest, type=None, **kwargs):
    if type is not None:
      raise ValueError("type not allowed")

    super(ActionPathsValidate, self).__init__(option_strings=option_strings, dest=dest, type=Path, **kwargs)

  def __call__(self, parser, namespace, values: List[Path], option_string=None):
    setattr(namespace, self.dest, values)

    if values:
      for item in values:
        if not item.exists():
          raise ValueError("Supplied Path does not exist: %s" % (item.as_posix()))


class BaseArgs(TypeWithDictRepr):

  def __init__(self, args: argparse.Namespace):
    self._args: argparse.Namespace = args
    self.debug: bool = args.debug
    self.verbose: bool = args.verbose

  def check_for_debug_and_exit(self, exit_code: int = 0, log_args_before_exit: bool = False):
    if self.debug:
      import logging

      if log_args_before_exit:
        log_args(self)

      logging.warning("debug enabled, exiting...")
      exit(exit_code)


class ColorArgs(object):

  def __init__(self, args: argparse.Namespace):
    self.color: bool = args.color if args.color is not None else is_output_to_terminal()

  @staticmethod
  def add_arguments_to_parser(arg_parser: argparse.ArgumentParser, default: bool = None) -> argparse.ArgumentParser:
    arg_parser.add_argument("--color", action=argparse.BooleanOptionalAction, default=default)
    return arg_parser


class IncludeExcludeCmdArgs(object):

  def __init__(self, args: argparse.Namespace):
    self.exclude_commands: List[str] = args.exclude_cmd or []
    self.include_commands: List[str] = args.include_cmd or []

  @staticmethod
  def add_arguments_to_parser(arg_parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    arg_parser.add_argument("--exclude-cmd", action=APPEND)
    arg_parser.add_argument("--include-cmd", action=APPEND)
    return arg_parser


class IncludeExcludeRegexArgs(object):

  def __init__(self, args: argparse.Namespace):
    self.exclude_regex: List[str] = args.exclude_regex or []
    self.include_regex: List[str] = args.include_regex or []

  @staticmethod
  def add_arguments_to_parser(arg_parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    arg_parser.add_argument("--exclude-regex", action=APPEND)
    arg_parser.add_argument("--include-regex", action=APPEND)
    return arg_parser


class LoggingArgs(object):

  def __init__(self, args: argparse.Namespace):
    self.log_format: str = args.log_format
    self.log_level: str = args.log_level
    self.quiet: bool = args.quiet

  @staticmethod
  def add_arguments_to_parser(arg_parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    arg_parser.add_argument("--log-format")
    arg_parser.add_argument("--log-level")
    arg_parser.add_argument("--quiet", action=STORE_TRUE)
    return arg_parser


class PagerArgs(object):

  def __init__(self, args: argparse.Namespace):
    self.no_pager: bool = args.no_pager
    self.pager: str = args.pager
    self.use_pager: bool = args.use_pager

  def should_use_pager(self, default: bool = True) -> bool:
    if self.use_pager:
      return True

    if self.no_pager:
      return False

    return default

  @staticmethod
  def add_arguments_to_parser(arg_parser: argparse.ArgumentParser, default_pager: str = None) -> argparse.ArgumentParser:
    arg_parser.add_argument("--no-pager", action=STORE_TRUE)
    arg_parser.add_argument("--pager", default=default_pager if default_pager else os.getenv("PAGER", "less"))
    arg_parser.add_argument("--use-pager", action=STORE_TRUE)
    return arg_parser


class RegexCasingArgs(object):

  def __init__(self, args: argparse.Namespace):
    self.ignore_case: bool = args.ignore_case
    self.use_case: bool = args.use_case

  @staticmethod
  def add_arguments_to_parser(arg_parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    arg_parser.add_argument("--ignore-case", "-i", action=STORE_TRUE)
    arg_parser.add_argument("--use-case", action=STORE_TRUE)
    return arg_parser

  def should_ignore_case(self, regex_pattern: str) -> bool:
    if self.use_case:
      return False

    if self.ignore_case:
      return True

    return regex_pattern is not None and regex_pattern.islower()


def add_default_arguments_to_parser(arg_parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
  arg_parser.add_argument("-v", "--verbose", action=STORE_TRUE)
  arg_parser.add_argument("--debug", action=STORE_TRUE)
  return arg_parser


def check_debug_mode() -> bool:
  return os.getenv("debug_mode", "false").lower() in TRUE_VALUES


def check_verbose() -> bool:
  return os.getenv("verbose", "false").lower() in TRUE_VALUES


def create_default_arg_parser() -> argparse.ArgumentParser:
  arg_parser = argparse.ArgumentParser()
  return add_default_arguments_to_parser(arg_parser)


def create_default_with_positionals_arg_parser(positionals_key: str = DEFAULT_POSITIONALS_KEY) -> argparse.ArgumentParser:
  import functools

  arg_parser = argparse.ArgumentParser(formatter_class=functools.partial(PositionalsHelpFormatter, positionals_key=positionals_key))
  return add_default_arguments_to_parser(arg_parser)


def parse_args(arg_parser: argparse.ArgumentParser, argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
  import argcomplete

  argcomplete.autocomplete(arg_parser)
  args = arg_parser.parse_args(args=argv)
  return args


def parse_args_and_init_others(arg_parser: argparse.ArgumentParser, argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
  from ltpylib.logs import init_logging

  args = parse_args(arg_parser, argv=argv)
  init_logging(args=args)
  return args


def parse_args_with_positionals_and_init_others(
  arg_parser: argparse.ArgumentParser,
  positionals_key: str = None,
  argv: Optional[Sequence[str]] = None,
  positionals_type: Callable = None,
) -> argparse.Namespace:
  import argcomplete
  import functools
  from ltpylib.logs import init_logging

  argcomplete.autocomplete(arg_parser)
  args, positionals = arg_parser.parse_known_intermixed_args(args=argv)

  if positionals_key is None:
    if isinstance(arg_parser.formatter_class, PositionalsHelpFormatter):
      help_formatter: PositionalsHelpFormatter = arg_parser.formatter_class
      positionals_key = help_formatter.positionals_key
    elif isinstance(arg_parser.formatter_class, functools.partial):
      help_formatter: functools.partial = arg_parser.formatter_class
      positionals_key = help_formatter.keywords.get("positionals_key")
    else:
      positionals_key = DEFAULT_POSITIONALS_KEY

  if positionals_type is not None:
    positionals = [positionals_type(arg) for arg in positionals]

  args.__setattr__(positionals_key, positionals)
  init_logging(args=args)
  return args


def does_stdin_have_data() -> bool:
  import sys
  import select

  if select.select([sys.stdin], [], [], 0.0)[0]:
    return True
  elif sys.stdin.isatty():
    return True
  else:
    return False


def check_command(cmd: str) -> bool:
  import shutil

  return shutil.which(cmd) is not None


def log_args(args: BaseArgs, include_raw_args: bool = True, only_keys: List[str] = None, skip_keys: List[str] = None):
  import logging
  from ltpylib.logs import log_sep

  logging.info("ARGS")
  log_sep(debug_only=False)

  log_format = "%-" + str(len(max(args.__dict__.keys(), key=len))) + "s -> %s"

  for item in sorted(args.__dict__.items()):
    if item[0] == "_args" and not include_raw_args:
      continue
    elif only_keys and not item[0] in only_keys:
      continue
    elif skip_keys and item[0] in skip_keys:
      continue

    logging.info(log_format, item[0], item[1])
