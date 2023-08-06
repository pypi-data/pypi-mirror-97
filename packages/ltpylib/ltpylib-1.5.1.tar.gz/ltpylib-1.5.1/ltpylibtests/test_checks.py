#!/usr/bin/env python
import unittest

from ltpylib import checks


class TestChecks(unittest.TestCase):

  def test_is_empty(self):
    assert checks.is_empty(None)
    assert checks.is_empty([])
    assert checks.is_empty({})

  def test_is_not_empty(self):
    assert checks.is_not_empty("abc")
    assert checks.is_not_empty([1])
    assert checks.is_not_empty(["abc"])
    assert checks.is_not_empty([{}])
    assert checks.is_not_empty([[]])
    assert checks.is_not_empty({"field": "value"})


if __name__ == '__main__':
  unittest.main()
