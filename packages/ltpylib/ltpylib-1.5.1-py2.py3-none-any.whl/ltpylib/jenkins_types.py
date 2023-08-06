#!/usr/bin/env python
import time
from typing import List

from ltpylib.common_types import DataWithUnknownPropertiesAsAttributes


class JenkinsBuild(DataWithUnknownPropertiesAsAttributes):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self._class: str = values.pop("_class", None)
    self.building: bool = values.pop("building", None)
    self.description: str = values.pop("description", None)
    self.displayName: str = values.pop("displayName", None)
    self.duration: int = values.pop("duration", None)
    self.estimatedDuration: int = values.pop("estimatedDuration", None)
    self.executor: str = values.pop("executor", None)
    self.id: str = values.pop("id", None)
    self.number: int = values.pop("number", None)
    self.queueId: int = values.pop("queueId", None)
    self.result: str = values.pop("result", None)
    self.timestamp: int = values.pop("timestamp", None)
    self.url: str = values.pop("url", None)

    self.timeRunning: int = None
    if self.timestamp is not None:
      self.timeRunning = (int(time.time() * 1000) - self.timestamp)

    self.estimatedTimeRemaining: int = None
    if self.duration is not None and self.duration > 0 and self.estimatedDuration is not None and self.estimatedDuration > 0:
      self.estimatedTimeRemaining: int = self.estimatedDuration - self.duration
    elif self.estimatedDuration is not None and self.estimatedDuration > 0 and self.timeRunning is not None:
      self.estimatedTimeRemaining: int = self.estimatedDuration - self.timeRunning

    DataWithUnknownPropertiesAsAttributes.__init__(self, values)


class JenkinsInstance(DataWithUnknownPropertiesAsAttributes):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self._class: str = values.pop("_class", None)
    self.jobs: List[JenkinsJob] = list(map(JenkinsJob, values.pop("jobs", []))) if "jobs" in values else None

    DataWithUnknownPropertiesAsAttributes.__init__(self, values)


class JenkinsJob(DataWithUnknownPropertiesAsAttributes):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self._class: str = values.pop("_class", None)
    self.jobs: List[JenkinsJob] = list(map(JenkinsJob, values.pop("jobs", []))) if "jobs" in values else None
    self.name: str = values.pop("name", None)
    self.url: str = values.pop("url", None)

    DataWithUnknownPropertiesAsAttributes.__init__(self, values)


class JenkinsJobStats(DataWithUnknownPropertiesAsAttributes):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.avg_duration_millis: float = values.pop("avg_duration_millis", None)
    self.name: str = values.pop("name", None)
    self.total: int = values.pop("total", None)

    DataWithUnknownPropertiesAsAttributes.__init__(self, values)
