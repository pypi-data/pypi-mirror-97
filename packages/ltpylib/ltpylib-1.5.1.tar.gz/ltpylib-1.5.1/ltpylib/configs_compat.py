#!/usr/bin/env python

import glob
import os

try:
  import configparser as cp
except:
  import ConfigParser as cp


def get_host(key, use_key_as_default=True):
  hosts_dir = os.path.abspath('%s/config/hosts' % os.getenv('DOTFILES', '%s/.dotfiles' % os.getenv('HOME')))
  hosts = cp.ConfigParser()
  host_files = glob.glob(hosts_dir + '/*.properties')
  host_files.extend(glob.glob(hosts_dir + '/*/*.properties'))
  for hosts_file in host_files:
    hosts = _py2_read_properties(hosts_file, config=hosts)

  if use_key_as_default:
    try:
      return hosts.get('DEFAULT', key)
    except cp.NoOptionError:
      return key
    except cp.NoSectionError:
      return key
  else:
    return hosts.get('DEFAULT', key)


def _py2_read_properties(file, use_mock_default_section=True, config=None):
  if not os.path.isfile(file):
    raise ValueError("File does not exist: %s" % file)

  if config is None:
    config = cp.ConfigParser(allow_no_value=True)
    config.optionxform = str

  if use_mock_default_section:
    with open(file, 'r') as configfile:
      try:
        config.read_string('[DEFAULT]\n' + configfile.read())
      except:
        import StringIO

        config.readfp(StringIO.StringIO('[DEFAULT]\n' + configfile.read()))
  else:
    config.read(file)

  return config


if __name__ == "__main__":
  import sys

  result = globals()[sys.argv[1]](*sys.argv[2:])
  if result is not None:
    print(result)
