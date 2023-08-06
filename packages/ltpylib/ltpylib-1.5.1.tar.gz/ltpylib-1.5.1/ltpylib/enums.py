#!/usr/bin/env python
from enum import Enum


class EnumAutoName(str, Enum):

  def _generate_next_value_(name, start, count, last_values):
    return name
