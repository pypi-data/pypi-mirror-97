#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
# pylint: disable=C0111
import argparse
import inspect
import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple, Union

import psutil
from ltpylib import files, logs, opts, procs


class ProcessRunner(object):

  def __init__(
    self,
    proc_id: str,
    start_cmd: List[str],
    build_cmds: List[Union[List[str], Tuple[Union[str, List[str]], dict]]] = None,
    force_build_before_start=None,
    log_file: str = None,
    log_multitail_args: List[str] = None,
    pid_file: str = None,
    proc_name_matcher: str = None,
    status_loop_wait_time: int = 30,
    status_loop_sleep_time: int = 1
  ):
    """
    :type force_build_before_start: Callable[[ProcessRunner], bool]
    """
    self.proc_id = proc_id
    self.start_cmd = start_cmd
    self.build_cmds = build_cmds
    self.force_build_before_start = force_build_before_start
    self.log_file = log_file or ('%s/Library/Logs/%s.log' % (os.getenv('HOME'), proc_id))
    self.log_multitail_args = log_multitail_args
    self.pid_file = pid_file
    self.proc_name_matcher = proc_name_matcher
    self.status_loop_wait_time = status_loop_wait_time
    self.status_loop_sleep_time = status_loop_sleep_time

  def get_proc_pid(self) -> Union[int, None]:
    if self.proc_name_matcher:
      matched_procs = procs.get_procs_from_name(self.proc_name_matcher)
      if matched_procs:
        return matched_procs[0][0]

      return None
    elif self.pid_file:
      if not Path(self.pid_file).is_file():
        return None

      pid = int(files.read_file(self.pid_file))
      if psutil.pid_exists(pid):
        return pid

      return None
    else:
      raise Exception('No pid_file or proc_name_matcher specified.')

  def check_proc_running(self):
    return self.get_proc_pid() is not None

  def log(self):
    if self.log_multitail_args and shutil.which('multitail'):
      logs.tail_log_file(self.log_file, *self.log_multitail_args)
    else:
      logs.tail_log_file(self.log_file)

  def build(self):
    if not self.build_cmds:
      raise Exception('No build_cmds specified.')

    for build_cmd_opt in self.build_cmds:
      func_args = {'universal_newlines': True}
      if isinstance(build_cmd_opt, tuple):
        build_cmd = build_cmd_opt[0]
        func_args.update(build_cmd_opt[1])
      else:
        build_cmd = build_cmd_opt

      subprocess.check_call(build_cmd, **func_args)

  def _await_termination(self, pid: int = None):
    if pid is None:
      pid = self.get_proc_pid()

    procs.await_termination(
      pid,
      timeout=self.status_loop_wait_time,
      sleep_time=self.status_loop_sleep_time,
      log_level=logging.INFO,
    )

  def stop(self) -> bool:
    pid = self.get_proc_pid()
    stop_result = False
    if pid is not None:
      stop_result = procs.stop_proc_by_pid(pid)
      if stop_result:
        self._await_termination(pid)

    return stop_result

  def start(self) -> int:
    self.stop()

    if self.force_build_before_start is not None and self.force_build_before_start(self):
      logging.info('Build required before executing start command - building now...')
      self.build()

    log_file_fd = open(self.log_file, 'a')
    pid = subprocess.Popen(
      self.start_cmd,
      stdout=log_file_fd,
      stderr=log_file_fd,
      universal_newlines=True,
    ).pid

    if pid is not None and self.pid_file:
      files.write_file(self.pid_file, str(pid))

    self.status(pid)
    return pid

  def status(self, pid: int = None) -> bool:
    if pid is None:
      pid = self.get_proc_pid()

    if pid is not None:
      proc = psutil.Process(pid)
      if proc.is_running():
        logging.info('%s', procs.proc_debug_string(proc))
        return True

    return False

  def _exec(self, cmd: str):
    return getattr(self, cmd)()

  def _parse_args(self) -> argparse.Namespace:
    arg_parser = opts.create_default_arg_parser()
    choices = []
    skip_methods = ['parse_and_run', 'check_proc_running']
    methods = inspect.getmembers(self, predicate=inspect.ismethod)
    for method in methods:
      if not method[0].startswith('_') and method[0] not in skip_methods:
        choices.append(method[0])
    arg_parser.add_argument('actions', choices=choices, nargs='+')
    return opts.parse_args_and_init_others(arg_parser)

  def parse_and_run(self):
    args = self._parse_args()
    result = None
    for cmd in args.actions:
      result = self._exec(cmd)

    if isinstance(result, bool):
      if not result:
        exit(1)
      else:
        exit(0)
    elif result is not None:
      logging.info('%s', result)
