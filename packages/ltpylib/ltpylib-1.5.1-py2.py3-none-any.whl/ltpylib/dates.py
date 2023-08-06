#!/usr/bin/env python
from datetime import datetime


def from_millis(millis: int) -> datetime:
  return datetime.fromtimestamp(millis / 1000.0)


def parse_iso_date(date_string: str) -> datetime:
  if not date_string:
    return None

  from dateutil import parser

  return parser.isoparse(date_string)


def parse_date(date_string: str, format: str = None) -> datetime:
  from dateutil import parser

  if not format:
    return parser.parse(date_string)
  return datetime.strptime(date_string, format)


def parse_possibly_relative_date(date_string: str) -> datetime:
  import dateparser

  return dateparser.parse(date_string)


def to_yyyymmdd(date: datetime) -> str:
  return date.strftime("%Y%m%d")


def to_yyyymmdd_dashes(date: datetime) -> str:
  return date.strftime("%Y-%m-%d")


def to_json_isoformat(date: datetime) -> str:
  return date.isoformat(sep="T", timespec="milliseconds") + "Z"


def to_json_isoformat_friendly(date: datetime) -> str:
  return date.isoformat(sep=" ", timespec="auto")


def add(
  date: datetime,
  years: int = 0,
  months: int = 0,
  days: int = 0,
  leapdays: int = 0,
  weeks: int = 0,
  hours: int = 0,
  minutes: int = 0,
  seconds: int = 0,
  microseconds: int = 0,
  year: int = None,
  month: int = None,
  day: int = None,
  weekday: int = None,
  yearday: int = None,
  nlyearday: int = None,
  hour: int = None,
  minute: int = None,
  second: int = None,
  microsecond: int = None,
) -> datetime:
  from dateutil.relativedelta import relativedelta

  return date + relativedelta(
    years=years,
    months=months,
    days=days,
    leapdays=leapdays,
    weeks=weeks,
    hours=hours,
    minutes=minutes,
    seconds=seconds,
    microseconds=microseconds,
    year=year,
    month=month,
    day=day,
    weekday=weekday,
    yearday=yearday,
    nlyearday=nlyearday,
    hour=hour,
    minute=minute,
    second=second,
    microsecond=microsecond,
  )


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
