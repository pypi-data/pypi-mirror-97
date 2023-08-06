#!/usr/bin/env python
import subprocess
import sys
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union


class CalledProcessErrorWithOutput(subprocess.CalledProcessError):

  def __init__(self, returncode, cmd, output=None, stderr=None):
    super(CalledProcessErrorWithOutput, self).__init__(returncode, cmd, output, stderr)

  def __str__(self):
    stdout_and_stderr = ""

    if self.output:
      stdout_and_stderr += "\n\nstdout\n---\n%s" % self.output

    if self.stderr:
      stdout_and_stderr += "\n\nstderr\n---\n%s" % self.stderr

    if self.returncode and self.returncode < 0:
      try:
        import signal

        return "Command '%s' died with %r.%s" % (self.cmd, signal.Signals(-self.returncode), stdout_and_stderr)
      except ValueError:
        return "Command '%s' died with unknown signal %d.%s" % (self.cmd, -self.returncode, stdout_and_stderr)
    else:
      return "Command '%s' returned non-zero exit status %d.%s" % (self.cmd, self.returncode, stdout_and_stderr)


def run(
  *popenargs,
  input: Union[bytes, str, None] = None,
  timeout: Optional[float] = None,
  check: bool = False,
  cwd: Union[str, bytes, Path] = None,
  shell: bool = False,
  **kwargs,
) -> subprocess.CompletedProcess:
  kwargs['universal_newlines'] = True
  if 'stdout' not in kwargs:
    kwargs['stdout'] = subprocess.PIPE
  if 'stderr' not in kwargs:
    kwargs['stderr'] = subprocess.PIPE

  result = subprocess.run(
    *popenargs,
    input=input,
    timeout=timeout,
    check=False,
    cwd=cwd,
    shell=shell,
    **kwargs,
  )

  if check:
    check_returncode_with_output(result)

  return result


def run_with_regular_stdout(
  *popenargs,
  input: Union[bytes, str, None] = None,
  timeout: Optional[float] = None,
  check: bool = False,
  cwd: Union[str, bytes, Path] = None,
  shell: bool = False,
  **kwargs,
) -> subprocess.CompletedProcess:
  return run(
    *popenargs,
    input=input,
    timeout=timeout,
    check=check,
    cwd=cwd,
    shell=shell,
    stdout=sys.stdout,
    stderr=sys.stderr,
    **kwargs,
  )


def run_and_parse_output(
  *popenargs,
  input: Union[bytes, str, None] = None,
  timeout: Optional[float] = None,
  check: bool = False,
  cwd: Union[str, bytes, Path] = None,
  shell: bool = False,
  **kwargs,
) -> Tuple[int, str]:
  kwargs['stdout'] = subprocess.PIPE

  result = run(
    *popenargs,
    input=input,
    timeout=timeout,
    check=check,
    cwd=cwd,
    shell=shell,
    **kwargs,
  )

  return result.returncode, result.stdout


def check_returncode_with_output(result: subprocess.CompletedProcess):
  if result.returncode:
    raise CalledProcessErrorWithOutput(result.returncode, result.args, result.stdout, result.stderr)


def get_procs_from_name(name_matcher: str) -> List[Tuple[int, str]]:
  matched_procs = []
  exit_code, output = run_and_parse_output(['pgrep', '-fl', name_matcher])
  if exit_code > 0:
    return matched_procs

  for line in output.splitlines():
    parts = line.partition(' ')
    matched_procs.append((int(parts[0]), parts[2]))

  return matched_procs


def proc_debug_string(proc) -> str:
  """
  :type proc: psutil.Process
  """
  import collections
  import psutil

  info = collections.OrderedDict()
  info['pid'] = proc.pid
  try:
    info["name"] = proc.name()
    if proc._create_time:
      info['started'] = psutil._pprint_secs(proc._create_time)
  except psutil.ZombieProcess:
    info["status"] = "zombie"
  except psutil.NoSuchProcess:
    info["status"] = "terminated"
  except psutil.AccessDenied:
    pass
  info['cmdline'] = ' '.join(proc.cmdline())
  return "%s.%s(%s)" % (
    proc.__class__.__module__,
    proc.__class__.__name__,
    ", ".join(["%s=%r" % (k, v) for k, v in info.items()]),
  )


def stop_proc_by_name(name_matcher: str) -> bool:
  import psutil

  matched_procs = get_procs_from_name(name_matcher)
  if not matched_procs:
    return False

  if len(matched_procs) > 1:
    raise Exception('Multiple processes found: %s' % matched_procs)

  proc = psutil.Process(matched_procs[0][0])
  proc.terminate()
  return True


def stop_proc_by_pid(pid: Any) -> bool:
  import psutil

  proc = psutil.Process(int(pid))
  if proc.is_running():
    proc.terminate()
  else:
    return False
  return True


def await_termination(pid: int, timeout: int = 30, sleep_time: int = 1, log_level: int = 20):
  """
  :param log_level: default is logging.INFO
  :return: None
  """
  import logging
  import psutil
  from time import sleep

  if pid is None:
    return

  proc = psutil.Process(pid)
  total_time = 0
  while total_time <= timeout:
    if proc.is_running():
      logging.log(log_level, 'STATUS: loop %s seconds - process is still running, please wait...', total_time)
    else:
      break

    total_time += sleep_time
    sleep(sleep_time)

  if proc.is_running():
    logging.error('STATUS: Process still running after %s seconds, sending SIGKILL to terminate...', total_time)
    proc.kill()
    proc.wait(5)
    logging.log(log_level, 'STATUS: Process killed.')
  else:
    logging.log(log_level, 'STATUS: Process successfully shutdown after %s seconds.', total_time)


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
