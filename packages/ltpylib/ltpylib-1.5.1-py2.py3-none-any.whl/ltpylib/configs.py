#!/usr/bin/env python

import glob
import io
import os
from collections import OrderedDict
from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path
from typing import Union

HOSTS_CONFIG: Union[ConfigParser, None] = None


def get_host(key: str, use_key_as_default: bool = True) -> str:
  hosts = get_or_create_hosts_config()

  if use_key_as_default:
    try:
      return hosts.get('DEFAULT', key)
    except NoOptionError:
      return key
    except NoSectionError:
      return key
  else:
    return hosts.get('DEFAULT', key)


def get_or_create_hosts_config() -> ConfigParser:
  global HOSTS_CONFIG
  if HOSTS_CONFIG is None:
    hosts_dir = os.path.abspath('%s/config/hosts' % os.getenv('DOTFILES', '%s/.dotfiles' % os.getenv('HOME')))
    HOSTS_CONFIG = ConfigParser()
    host_files = glob.glob(hosts_dir + '/*.properties')
    host_files.extend(glob.glob(hosts_dir + '/*/*.properties'))
    for hosts_file in host_files:
      HOSTS_CONFIG = read_properties(hosts_file, config=HOSTS_CONFIG)

  return HOSTS_CONFIG


def sort_config_parser_keys(config: ConfigParser) -> ConfigParser:
  if config._defaults:
    config._defaults = OrderedDict(sorted(config._defaults.items(), key=lambda t: t[0]))

  for section in config._sections:
    config._sections[section] = OrderedDict(sorted(config._sections[section].items(), key=lambda t: t[0]))

  config._sections = OrderedDict(sorted(config._sections.items(), key=lambda t: t[0]))
  return config


def config_parser_to_string(config: ConfigParser, sort_keys: bool = False):
  if sort_keys:
    config = sort_config_parser_keys(config)

  sio = io.StringIO()
  config.write(sio)
  return sio.getvalue()


def read_properties(
  file: Union[str, Path],
  use_mock_default_section: bool = True,
  config: ConfigParser = None,
  allow_missing_file: bool = False,
) -> ConfigParser:
  if isinstance(file, str):
    file = Path(file)

  if config is None:
    config = ConfigParser(allow_no_value=True)
    config.optionxform = str

  if not file.is_file():
    if not allow_missing_file:
      raise ValueError("File does not exist: %s" % file)
    return config

  if use_mock_default_section:
    with open(file.as_posix(), 'r') as configfile:
      config.read_string('[DEFAULT]\n' + configfile.read())
  else:
    config.read(file.as_posix())

  return config


def write_properties(config: ConfigParser, file: Union[str, Path], sort_keys: bool = False):
  if sort_keys:
    config = sort_config_parser_keys(config)

  if isinstance(file, str):
    file = Path(file)

  with open(file.as_posix(), 'w') as configfile:
    config.write(configfile)


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
