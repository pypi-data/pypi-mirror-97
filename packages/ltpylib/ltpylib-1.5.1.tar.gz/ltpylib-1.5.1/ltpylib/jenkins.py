#!/usr/bin/env python
import re
from typing import List, Tuple

import requests
from requests import Session

from ltpylib import requests_helper
from ltpylib.jenkins_types import JenkinsBuild, JenkinsInstance

JENKINS_JOB_URL_REGEX: str = r'^(https?):\/\/([^\/:]+)(:[0-9]+)?(?:\/)(?:job|blue\/organizations\/jenkins)\/(([^\/]+)(?:\/(?:job|detail)\/([^\/]+))?)\/([0-9]+)\/' \
                             r'(?:pipeline\/?|display\/redirect)?$'


class JenkinsApi(object):

  def __init__(self, base_url: str, creds: Tuple[str, str]):
    if base_url.endswith("/"):
      self.base_url: str = base_url[:-1]
    else:
      self.base_url: str = base_url

    self.creds: Tuple[str, str] = creds
    self.session: Session = requests.Session()

    self.session.verify = True
    if creds is not None:
      self.session.auth = creds

    self.session.cookies = self.session.head(self.url("")).cookies
    self.session.headers.update({'Content-Type': 'application/json', 'Accept': 'application/json'})

  def url(self, resource_path: str):
    if not resource_path.startswith("/"):
      resource_path = "/" + resource_path
    return self.base_url + resource_path

  def build(self, job: str, build: int) -> JenkinsBuild:
    response = self.session.get(self.url("job/%s/%s/api/json?tree=*" % (job, str(build))))
    return JenkinsBuild(requests_helper.parse_raw_response(response))

  def all_builds(self, job: str, tree: str = "building,description,displayName,duration,estimatedDuration,executor,id,number,queueId,result,timestamp,url") -> List[JenkinsBuild]:
    response = self.session.get(self.url("job/%s/api/json?tree=%s" % (
      job,
      "allBuilds[%s]" % tree,
    )))
    return [JenkinsBuild(values=v) for v in requests_helper.parse_raw_response(response).get("allBuilds")]

  def instance_info(self, tree: str = "*") -> JenkinsInstance:
    response = self.session.get(self.url("api/json?tree=%s" % tree))
    return JenkinsInstance(requests_helper.parse_raw_response(response))

  def instance_info_all_jobs(self) -> JenkinsInstance:
    return self.instance_info(tree="jobs[name,jobs[name]]")


def parse_job_url(url: str) -> Tuple[str, int]:
  match = re.match(JENKINS_JOB_URL_REGEX, url)
  job_name = match.group(5)
  if match.group(6) and match.group(5) != match.group(6):
    job_name = job_name + "/job/" + match.group(6)

  job_num = int(match.group(7))

  return job_name, job_num
