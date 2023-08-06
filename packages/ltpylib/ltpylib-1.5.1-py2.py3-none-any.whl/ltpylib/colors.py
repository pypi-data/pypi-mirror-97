#!/usr/bin/env python


class TermColors:
  BLACK = '\033[0;30m'
  BLUE = '\033[0;34m'
  BOLD = '\033[1m'
  CYAN = '\033[0;36m'
  ENDC = '\033[0m'
  GREEN = '\033[0;32m'
  HEADER = '\033[95m'
  LIGHT_BLUE = '\033[1;34m'
  LIGHT_CYAN = '\033[1;36m'
  LIGHT_GREEN = '\033[1;32m'
  LIGHT_PURPLE = '\033[1;35m'
  LIGHT_RED = '\033[1;31m'
  LIGHT_YELLOW = '\033[1;33m'
  PURPLE = '\033[0;35m'
  RED = '\033[0;31m'
  UNDERLINE = '\033[4m'
  WHITE = '\033[0;37m'
  YELLOW = '\033[0;33m'


def black(value: str) -> str:
  return TermColors.BLACK + value + TermColors.ENDC


def blue(value: str) -> str:
  return TermColors.BLUE + value + TermColors.ENDC


def bold(value: str) -> str:
  return TermColors.BOLD + value + TermColors.ENDC


def cyan(value: str) -> str:
  return TermColors.CYAN + value + TermColors.ENDC


def green(value: str) -> str:
  return TermColors.GREEN + value + TermColors.ENDC


def light_blue(value: str) -> str:
  return TermColors.LIGHT_BLUE + value + TermColors.ENDC


def light_cyan(value: str) -> str:
  return TermColors.LIGHT_CYAN + value + TermColors.ENDC


def light_green(value: str) -> str:
  return TermColors.LIGHT_GREEN + value + TermColors.ENDC


def light_purple(value: str) -> str:
  return TermColors.LIGHT_PURPLE + value + TermColors.ENDC


def light_red(value: str) -> str:
  return TermColors.LIGHT_RED + value + TermColors.ENDC


def light_yellow(value: str) -> str:
  return TermColors.LIGHT_YELLOW + value + TermColors.ENDC


def purple(value: str) -> str:
  return TermColors.PURPLE + value + TermColors.ENDC


def red(value: str) -> str:
  return TermColors.RED + value + TermColors.ENDC


def underline(value: str) -> str:
  return TermColors.UNDERLINE + value + TermColors.ENDC


def white(value: str) -> str:
  return TermColors.WHITE + value + TermColors.ENDC


def yellow(value: str) -> str:
  return TermColors.YELLOW + value + TermColors.ENDC
