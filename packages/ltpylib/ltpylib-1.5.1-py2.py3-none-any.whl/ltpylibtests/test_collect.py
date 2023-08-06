#!/usr/bin/env python
import unittest

from ltpylib import collect


class TestCollect(unittest.TestCase):

  def test_to_csv(self):
    assert collect.to_csv(None) is None
    assert collect.to_csv(["a", "b"]) == "a,b"
    assert collect.to_csv(["a", "b"], sep=" | ") == "a | b"


if __name__ == '__main__':
  unittest.main()
