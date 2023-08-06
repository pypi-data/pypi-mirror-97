#!/usr/bin/env python
import os
import unittest
from pathlib import Path

from ltpylib import strings
from ltpylibtests import testing_utils


class TestStrings(unittest.TestCase):

  def test_to_snake_case(self):
    test_file = Path(os.path.dirname(os.path.realpath(__file__))).joinpath("resources/test_to_snake_case.yaml")
    config = testing_utils.load_yaml_test_config_file(test_file)

    assert len(config.test_cases) > 0

    for test_case in config.test_cases:
      if not test_case:
        continue

      self.assertEqual(strings.to_snake_case(test_case.input), test_case.expected)


if __name__ == '__main__':
  unittest.main()
