#!/usr/bin/env python
import logging
import time


def format_seconds(frac_seconds):
  hours, rem = divmod(float(frac_seconds), 3600)
  minutes, seconds = divmod(rem, 60)
  return "{0:0>2}:{1:0>2}:{2:06.3f}".format(int(hours), int(minutes), seconds)


def format_millis(millis):
  return format_seconds(float(millis) / float(1000))


def get_time_elapsed_msg(start_time):
  return format_seconds(time.time() - float(start_time))


def get_time_remaining_formatted_seconds(start_time, count, total):
  frac_seconds = time.time() - float(start_time)
  if float(count) <= 0:
    return "N/A"

  estimated_total = frac_seconds * (float(total) / float(count))
  return format_seconds(estimated_total - frac_seconds)


def get_time_remaining_msg(start_time, count, total):
  frac_seconds = time.time() - float(start_time)
  if float(count) <= 0:
    return "Elapsed: {0: >12} Remaining: {1: >12}".format(format_seconds(frac_seconds), 'N/A')

  estimated_total = frac_seconds * (float(total) / float(count))
  return "Elapsed: {0: >12} Remaining: {1: >12}".format(format_seconds(frac_seconds), format_seconds(estimated_total - frac_seconds))


def sleep_and_log(seconds: int, log_level: int = logging.INFO):
  logging.log(log_level, "Sleeping %s seconds...", seconds)
  time.sleep(seconds)


if __name__ == "__main__":
  import sys

  result = globals()[sys.argv[1]](*sys.argv[2:])
  if result is not None:
    print(result)
