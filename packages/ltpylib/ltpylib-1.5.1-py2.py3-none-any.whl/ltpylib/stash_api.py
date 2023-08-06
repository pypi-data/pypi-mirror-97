#!/usr/bin/env python
from typing import List, Tuple, Union

import stashy
from requests import Response
from stashy import repos
from stashy.pullrequests import PullRequest, PullRequests
from stashy.repos import Repos

from ltpylib import colors, dates, requests_helper
from ltpylib.inputs import select_prompt_and_return_indexes
from ltpylib.stash_types import (
  Branch,
  Branches,
  Builds,
  PullRequestActivities,
  PullRequestMergeability,
  PullRequestMergeStatus,
  PullRequestParticipantStatus,
  PullRequestRole,
  PullRequestState,
  PullRequestStatus,
  PullRequestStatuses,
  Repository,
  SearchResults,
)
from ltpylib.strings import str_list_max_length

STASH_URL: str = "https://stash.wlth.fr"
BRANCH_PR_META_KEY: str = "com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata"


class StashApi(object):

  def __init__(self, stash: stashy.Stash):
    self.stash: stashy.Stash = stash

  def ask_user_to_select_their_prs(
    self,
    role: PullRequestRole = None,
    state: PullRequestState = PullRequestState.OPEN,
    participant_status: List[PullRequestParticipantStatus] = None,
  ) -> Union[None, List[PullRequestStatus]]:
    my_prs = self.my_pull_requests(
      state=state,
      role=role,
      participant_status=participant_status,
    )

    if not my_prs.values:
      return None

    prs = sorted(my_prs.values, key=pr_sort)
    pr_links: List[str] = []

    branch_max_length = str_list_max_length([pr.fromRef.displayId for pr in prs])
    repo_max_length = str_list_max_length([pr.fromRef.repository.name for pr in prs])

    for pr in prs:
      pr_links.append(
        "  ".join([
          colors.green(dates.from_millis(pr.createdDate).isoformat()),
          colors.red(pr.fromRef.repository.name.ljust(repo_max_length)),
          colors.blue(pr.fromRef.displayId.ljust(branch_max_length)),
          pr.title,
        ])
      )

    selections = select_prompt_and_return_indexes(
      pr_links,
      header="Select PRs to open",
      multi=True,
      ansi=True,
    )

    return [prs[index] for index in selections]

  def builds_for_commit(self, commit: str, limit: int = 1000) -> Builds:
    api_url = '%s/rest/build-status/latest/commits/%s?limit=%s' % (
      self.stash._client._base_url,
      commit,
      str(limit),
    )
    kw = requests_helper.add_json_headers()
    result: Builds = Builds(requests_helper.parse_raw_response(self.stash._client._session.get(api_url, **kw)))

    return result

  def create_pull_request(
    self,
    project: str,
    repo: str,
    from_ref: str,
    to_ref: str,
    title: str,
    description: str,
    reviewers: List[str],
  ) -> PullRequestStatus:
    prs: PullRequests = self.stash.projects[project].repos[repo].pull_requests
    response: dict = prs.create(
      title=title,
      fromRef=from_ref,
      toRef=to_ref,
      description=description,
      reviewers=reviewers,
    )

    return PullRequestStatus(response)

  def delete_pull_request_source_branch(
    self,
    project: str,
    repo: str,
    pr_id: int,
  ) -> Response:
    api_url = '%s/rest/pull-request-cleanup/latest/projects/%s/repos/%s/pull-requests/%s' % (
      self.stash._client._base_url,
      project,
      repo,
      str(pr_id),
    )
    kw = requests_helper.add_json_headers()
    response = self.stash._client._session.post(
      api_url,
      json={
        "deleteSourceRef": True,
        "retargetDependents": True,
      },
      **kw,
    )
    return response

  def merge_pull_request(
    self,
    project: str,
    repo: str,
    pr_id: int,
    delete_source_branch: bool = True,
    commit_message: str = "",
    version: int = None,
  ) -> PullRequestMergeStatus:
    pr: PullRequest = self.stash.projects[project].repos[repo].pull_requests[str(pr_id)]
    if version is None:
      pr_info = self.pull_request(project, repo, pr_id, include_merge_info=False)
      version = pr_info.version

    result: PullRequestMergeStatus = PullRequestMergeStatus(
      requests_helper.parse_raw_response(pr._client.post(pr.url("/merge"), data=dict(message=commit_message, version=version)))
    )
    if delete_source_branch and result.state == "MERGED":
      delete_source_branch_response = self.delete_pull_request_source_branch(project, repo, pr_id)
      result.sourceBranchDeleted = delete_source_branch_response.status_code == 200 or delete_source_branch_response.status_code == 204

    return result

  def my_pull_requests(
    self,
    role: PullRequestRole = None,
    state: PullRequestState = PullRequestState.OPEN,
    participant_status: List[PullRequestParticipantStatus] = None,
    start: int = 0,
    limit: int = 100,
    with_attributes: bool = True,
    order: str = None,
  ) -> PullRequestStatuses:

    if isinstance(role, str):
      role = PullRequestRole.from_string(role, allow_unknown=True)

    if isinstance(state, str):
      state = PullRequestState.from_string(state, allow_unknown=True, unknown_as_none=True)

    if isinstance(participant_status, str):
      participant_status = [PullRequestParticipantStatus.from_string(val) for val in participant_status.split(",")] if participant_status and participant_status != "_" else None

    api_params = {
      "start": str(start),
      "limit": str(limit),
      "withAttributes": str(with_attributes).lower(),
    }

    if state:
      api_params["state"] = state.name

    if role:
      api_params["role"] = role.name

    if participant_status:
      api_params["participantStatus"] = ",".join([val.name for val in participant_status])

    if order:
      api_params["order"] = order

    api_url = '%s/rest/api/latest/dashboard/pull-requests?%s' % (
      self.stash._client._base_url,
      "&".join((k + "=" + v) for (k, v) in api_params.items()),
    )
    kw = requests_helper.add_json_headers()
    return PullRequestStatuses(values=requests_helper.parse_raw_response(self.stash._client._session.get(api_url, **kw)))

  def pull_request(
    self,
    project: str,
    repo: str,
    pr_id: int,
    include_merge_info: bool = True,
    include_builds: bool = False,
  ) -> PullRequestStatus:
    pr: PullRequest = self.stash.projects[project].repos[repo].pull_requests[str(pr_id)]
    result: PullRequestStatus = PullRequestStatus(pr.get())
    if include_merge_info and result.open:
      merge_info = self.pull_request_merge_info(project, repo, pr_id)
      result.mergeInfo = merge_info

    if include_builds and result.fromRef and result.fromRef.latestCommit:
      builds = self.builds_for_commit(result.fromRef.latestCommit)
      result.builds = builds

    return result

  def pull_request_activities(
    self,
    project: str,
    repo: str,
    pr_id: int,
  ) -> PullRequestActivities:
    pr: PullRequest = self.stash.projects[project].repos[repo].pull_requests[str(pr_id)]
    result: PullRequestActivities = PullRequestActivities(requests_helper.parse_raw_response(pr._client.get(pr.url() + "/activities")))

    return result

  def pull_request_merge_info(
    self,
    project: str,
    repo: str,
    pr_id: int,
  ) -> PullRequestMergeability:
    pr: PullRequest = self.stash.projects[project].repos[repo].pull_requests[str(pr_id)]
    return PullRequestMergeability(pr.merge_info())

  def pull_requests(
    self,
    project: str,
    repo: str,
    state: Union[PullRequestState, str] = PullRequestState.OPEN,
    author: str = None,
    order: str = None,
    target_branch: str = None,
    direction: str = 'INCOMING',
  ) -> List[PullRequestStatus]:

    if isinstance(state, str):
      state = PullRequestState.from_string(state, allow_unknown=False)

    prs: PullRequests = self.stash.projects[project].repos[repo].pull_requests
    return [PullRequestStatus(pr) for pr in prs.all(
      direction=direction,
      at=target_branch,
      state=(state.name if state else None),
      order=order,
      author=author,
    )]

  def repo(self, project: str, repo: str) -> Repository:
    return Repository(self.stash.projects[project].repos[repo].get())

  def repo_branches(self, project: str, repo: str, limit: int = None, details: bool = True) -> Branches:
    if isinstance(limit, str):
      limit = int(limit)
    elif limit is None:
      limit = 1000

    if isinstance(details, str):
      details = details.lower() == "true" or details.lower() == "yes"

    repo: repos.Repository = self.stash.projects[project].repos[repo]

    limit_above_max = limit > 1000 or limit <= -1
    if details and limit_above_max:
      branches = Branches(values={
        "limit": limit,
        "start": 0,
        "values": [],
      })
      branches.isLastPage = True

      for branch in repo.branches(details=details):
        branches.values.append(Branch(values=branch))
        if 0 <= limit <= len(branches.values):
          branches.isLastPage = False
          break

      branches.size = len(branches.values)
      return branches

    details_str = "true" if details else "false"
    if limit <= -1:
      limit = 999999

    return Branches(values=requests_helper.parse_raw_response(self.stash._client.get(repo.url('/branches?limit=%s&details=%s' % (limit, details_str)))))

  def repo_branches_with_pr_in_states(self, project: str, repo: str, states: List[PullRequestState], limit: int = None) -> Branches:
    if isinstance(limit, str):
      limit = int(limit)

    if isinstance(states, str):
      states = [PullRequestState.from_string(state) for state in states.split(",")]
    else:
      states = [PullRequestState.from_string(state) for state in states]

    branches = self.repo_branches(project, repo, limit=limit, details=True)

    merged_branches: Branches = Branches(values={
      "isLastPage": branches.isLastPage,
      "limit": branches.limit,
      "start": branches.start,
    })
    merged_branches.values = []

    for branch in branches.values:
      if branch.metadata is None or BRANCH_PR_META_KEY not in branch.metadata:
        continue

      branch_pr_meta = branch.metadata.get(BRANCH_PR_META_KEY)

      if "pullRequest" not in branch_pr_meta:
        has_prs_with_state = False
        for state in states:
          if state.name.lower() in branch_pr_meta and branch_pr_meta.get(state.name.lower()) > 0:
            has_prs_with_state = True
            break

        if has_prs_with_state:
          merged_branches.values.append(branch)

        continue

      pr_meta_raw: dict = branch_pr_meta.pop("pullRequest")
      pr_meta = PullRequestStatus(values=pr_meta_raw)
      branch_pr_meta["pullRequest"] = pr_meta
      if pr_meta.state in states:
        merged_branches.values.append(branch)

    merged_branches.size = len(merged_branches.values)
    return merged_branches

  def repo_merged_branches(self, project: str, repo: str, limit: int = None) -> Branches:
    return self.repo_branches_with_pr_in_states(project, repo, [PullRequestState.MERGED], limit=limit)

  def repos_for_project(self, project: str) -> List[Repository]:
    project_repos: Repos = self.stash.projects[project].repos
    return [Repository(repo) for repo in project_repos.list()]

  def search(self, query: str, limit: int = 25) -> SearchResults:
    api_json = {
      "entities": {
        "code": {}
      },
      "limits": {
        "primary": limit
      },
      "query": query,
    }
    kw = requests_helper.add_json_headers()
    return SearchResults(requests_helper.parse_raw_response(self.stash._client._session.post(
      '%s/rest/search/latest/search' % self.stash._client._base_url,
      json=api_json,
      **kw,
    )))


def create_stash_api(url: str, creds: Tuple[str, str] = None, token: str = None) -> StashApi:
  if token:
    return StashApi(stashy.client.Stash(url, token=token))

  return StashApi(stashy.client.Stash(url, username=creds[0], password=creds[1]))


def pr_sort(pr: PullRequestStatus) -> str:
  return "%s %s" % (
    pr.fromRef.repository.name,
    pr.fromRef.displayId.lower(),
  )
