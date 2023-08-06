#!/usr/bin/env python
import unittest

from ltpylib.common_types import DataWithUnknownProperties, DataWithUnknownPropertiesAsAttributes


class TestDataWithUnknownProperties(unittest.TestCase):

  def test_DataWithUnknownProperties_empty(self):
    val = DataWithUnknownProperties(values={})
    self.assertIsNone(val.unknown_properties)

  def test_DataWithUnknownProperties_none(self):
    val = DataWithUnknownProperties(values=None)
    self.assertIsNone(val.unknown_properties)

  def test_DataWithUnknownProperties_some(self):
    values = {
      "field_num": 3,
      "field_str": "abc",
    }
    val = DataWithUnknownProperties(values=values)
    self.assertDictEqual(val.unknown_properties, values)


class TestDataWithUnknownPropertiesAsAttributes(unittest.TestCase):

  def test_DataWithUnknownPropertiesAsAttributes(self):
    values = {
      "field_num": 3,
      "field_str": "abc",
    }
    val = DataWithUnknownPropertiesAsAttributes(values=values)

    self.assertTrue(val.has_unknown_properties)
    self.assertFalse(hasattr(val, "unknown_properties"))

    self.assertTrue(hasattr(val, "field_num"))
    self.assertEqual(getattr(val, "field_num"), 3)
    self.assertEqual(val.field_num, 3)

    self.assertTrue(hasattr(val, "field_str"))
    self.assertEqual(getattr(val, "field_str"), "abc")
    self.assertEqual(val.field_str, "abc")

  def test_DataWithUnknownPropertiesAsAttributes_none(self):
    val = DataWithUnknownPropertiesAsAttributes(values=None)
    self.assertFalse(val.has_unknown_properties)
    self.assertFalse(hasattr(val, "unknown_properties"))

    val = DataWithUnknownPropertiesAsAttributes(values={})
    self.assertFalse(val.has_unknown_properties)
    self.assertFalse(hasattr(val, "unknown_properties"))


if __name__ == '__main__':
  unittest.main()
