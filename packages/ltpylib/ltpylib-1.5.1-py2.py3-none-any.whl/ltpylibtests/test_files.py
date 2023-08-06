#!/usr/bin/env python
import os
import unittest
from pathlib import Path

from ltpylib import files


class TestFiles(unittest.TestCase):

  def test_read_file_n_lines(self):
    test_file = Path(os.path.dirname(os.path.realpath(__file__))).joinpath("resources/test_files_read_file_n_lines.txt")

    assert files.read_file_n_lines(test_file, 1) == ["line1"]
    assert files.read_file_n_lines(test_file, 2) == ["line1", "line2"]
    assert files.read_file_n_lines(test_file, 3) == ["line1", "line2", "line3"]
    assert files.read_file_n_lines(test_file, 4) == ["line1", "line2", "line3", ""]
    assert files.read_file_n_lines(test_file, 5) == ["line1", "line2", "line3", "", "line5"]
    assert files.read_file_n_lines(test_file, 6) == ["line1", "line2", "line3", "", "line5"]
    assert files.read_file_n_lines(test_file, -1) == ["line1", "line2", "line3", "", "line5"]

  def test_read_json_file(self):
    test_file = Path(os.path.dirname(os.path.realpath(__file__))).joinpath("resources/test_files_read_json_file.json")
    parsed_json = files.read_json_file(test_file)

    assert parsed_json.get("field1") == "value1"
    assert parsed_json.get("field2") == 2


if __name__ == '__main__':
  unittest.main()
