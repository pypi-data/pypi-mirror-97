#!/usr/bin/env python
import argparse
from enum import auto
from typing import Dict, List

from ltpylib import opts_actions
from ltpylib.common_types import DataWithUnknownProperties, TypeWithDictRepr
from ltpylib.enums import EnumAutoName


class DisplayIdAndId(object):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.displayId: str = values.pop("displayId", None)
    self.id: str = values.pop("id", None)


class PaginatedValues(object):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.isLastPage: int = values.pop("isLastPage", None)
    self.limit: int = values.pop("limit", None)
    self.size: int = values.pop("size", None)
    self.start: int = values.pop("start", None)


class PullRequestParticipantStatus(EnumAutoName):
  APPROVED = auto()
  NEEDS_WORK = auto()
  UNAPPROVED = auto()

  @staticmethod
  def from_string(val: str, allow_unknown: bool = False):
    try:
      return PullRequestParticipantStatus[val.upper()] if val else None
    except KeyError as e:
      if allow_unknown:
        return None

      raise e


class PullRequestRole(EnumAutoName):
  AUTHOR = auto()
  PARTICIPANT = auto()
  REVIEWER = auto()

  @staticmethod
  def from_string(val: str, allow_unknown: bool = False):
    try:
      return PullRequestRole[val.upper()] if val else None
    except KeyError as e:
      if allow_unknown:
        return None

      raise e


class PullRequestState(EnumAutoName):
  DECLINED = auto()
  MERGED = auto()
  OPEN = auto()
  UNKNOWN = auto()

  @staticmethod
  def from_string(state: str, allow_unknown: bool = True, unknown_as_none: bool = False):
    try:
      return PullRequestState[state.upper()] if state else None
    except KeyError as e:
      if allow_unknown:
        return None if unknown_as_none else PullRequestState.UNKNOWN

      raise e


class ApplicationProperties(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.buildDate: str = values.pop("buildDate", None)
    self.buildNumber: str = values.pop("buildNumber", None)
    self.displayName: str = values.pop("displayName", None)
    self.version: str = values.pop("version", None)

    DataWithUnknownProperties.__init__(self, values)


class Branch(DataWithUnknownProperties, DisplayIdAndId):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    DisplayIdAndId.__init__(self, values)

    self.isDefault: bool = values.pop("isDefault", None)
    self.latestChangeset: str = values.pop("latestChangeset", None)
    self.latestCommit: str = values.pop("latestCommit", None)
    self.type: str = values.pop("type", None)
    self.metadata: Dict[str, dict] = values.pop("metadata", None)

    DataWithUnknownProperties.__init__(self, values)


class Branches(DataWithUnknownProperties, PaginatedValues):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    PaginatedValues.__init__(self, values)

    self.values: List[Branch] = list(map(Branch, values.pop("values", []))) if "values" in values else None

    DataWithUnknownProperties.__init__(self, values)


class Build(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.dateAdded: int = values.pop("dateAdded", None)
    self.description: str = values.pop("description", None)
    self.key: str = values.pop("key", None)
    self.name: str = values.pop("name", None)
    self.state: str = values.pop("state", None)
    self.url: str = values.pop("url", None)

    DataWithUnknownProperties.__init__(self, values)


class Builds(DataWithUnknownProperties, PaginatedValues):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    PaginatedValues.__init__(self, values)

    self.values: List[Build] = list(map(Build, values.pop("values", []))) if "values" in values else None

    DataWithUnknownProperties.__init__(self, values)


class Comment(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.id: int = values.pop("id", None)
    self.text: str = values.pop("text", None)
    self.version: int = values.pop("version", None)

    DataWithUnknownProperties.__init__(self, values)


class Commit(DataWithUnknownProperties, DisplayIdAndId):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    DisplayIdAndId.__init__(self, values)

    DataWithUnknownProperties.__init__(self, values)


class Link(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.href: str = values.pop("href", None)
    self.name: str = values.pop("name", None)

    DataWithUnknownProperties.__init__(self, values)


class Links(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.clone: List[Link] = list(map(Link, values.pop("clone", []))) if "clone" in values else None
    self.self: List[Link] = list(map(Link, values.pop("self", []))) if "self" in values else None

    DataWithUnknownProperties.__init__(self, values)


class Project(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.description: str = values.pop("description", None)
    self.id: int = values.pop("id", None)
    self.key: str = values.pop("key", None)
    self.links: Links = Links(values=values.pop("links")) if "links" in values else None
    self.name: str = values.pop("name", None)
    self.owner: User = User(values=values.pop("owner")) if "owner" in values else None
    self.public: bool = values.pop("public", None)
    self.type: str = values.pop("type", None)

    DataWithUnknownProperties.__init__(self, values)


class PullRequestActivities(DataWithUnknownProperties, PaginatedValues):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    PaginatedValues.__init__(self, values)

    self.values: List[PullRequestActivity] = list(map(PullRequestActivity, values.pop("values", []))) if "values" in values else None

    DataWithUnknownProperties.__init__(self, values)


class PullRequestActivity(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.action: str = values.pop("action", None)
    self.commentAction: str = values.pop("commentAction", None)
    self.createdDate: int = values.pop("createdDate", None)
    self.id: int = values.pop("id", None)
    self.user: User = User(values=values.pop("user")) if "user" in values else None

    DataWithUnknownProperties.__init__(self, values)


class PullRequestMergeability(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.canMerge: bool = values.pop("canMerge", None)
    self.conflicted: bool = values.pop("conflicted", None)
    self.outcome: str = values.pop("outcome", None)
    self.vetoes: List[PullRequestVeto] = list(map(PullRequestVeto, values.pop("vetoes", []))) if "vetoes" in values else None

    DataWithUnknownProperties.__init__(self, values)


class PullRequestParticipant(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.approved: bool = values.pop("approved", None)
    self.lastReviewedCommit: str = values.pop("lastReviewedCommit", None)
    self.role: str = values.pop("role", None)
    self.status: str = values.pop("status", None)
    self.user: User = User(values=values.pop("user")) if "user" in values else None

    DataWithUnknownProperties.__init__(self, values)


class PullRequestProperties(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.commentCount: int = values.pop("commentCount", None)
    self.mergeCommit: Commit = Commit(values=values.pop("mergeCommit")) if "mergeCommit" in values else None
    self.openTaskCount: int = values.pop("openTaskCount", None)
    self.resolvedTaskCount: int = values.pop("resolvedTaskCount", None)

    DataWithUnknownProperties.__init__(self, values)


class PullRequestRef(DataWithUnknownProperties, DisplayIdAndId):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    DisplayIdAndId.__init__(self, values)

    self.latestCommit: str = values.pop("latestCommit", None)
    self.repository: Repository = Repository(values=values.pop("repository")) if "repository" in values else None

    DataWithUnknownProperties.__init__(self, values)


class PullRequestStatus(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.author: PullRequestParticipant = PullRequestParticipant(values=values.pop("author")) if "author" in values else None
    self.closed: bool = values.pop("closed", None)
    self.createdDate: int = values.pop("createdDate", None)
    self.description: str = values.pop("description", None)
    self.fromRef: PullRequestRef = PullRequestRef(values=values.pop("fromRef")) if "fromRef" in values else None
    self.id: int = values.pop("id", None)
    self.links: Links = Links(values=values.pop("links")) if "links" in values else None
    self.locked: bool = values.pop("locked", None)
    self.open: bool = values.pop("open", None)
    self.outstandingTaskCount: int = values.pop("outstandingTaskCount", None)
    self.participants: List[PullRequestParticipant] = list(map(PullRequestParticipant, values.pop("participants", []))) if "participants" in values else None
    self.properties: PullRequestProperties = PullRequestProperties(values=values.pop("properties")) if "properties" in values else None
    self.reviewers: List[PullRequestParticipant] = list(map(PullRequestParticipant, values.pop("reviewers", []))) if "reviewers" in values else None
    self.state: PullRequestState = PullRequestState.from_string(values.pop("state")) if "state" in values else None
    self.title: str = values.pop("title", None)
    self.toRef: PullRequestRef = PullRequestRef(values=values.pop("toRef")) if "toRef" in values else None
    self.updatedDate: int = values.pop("updatedDate", None)
    self.version: int = values.pop("version", None)

    self.url: str = self.links.self[0].href if (self.links and self.links.self) else None

    self.builds: Builds = None
    self.mergeInfo: PullRequestMergeability = None

    DataWithUnknownProperties.__init__(self, values)


class PullRequestStatuses(DataWithUnknownProperties, PaginatedValues):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    PaginatedValues.__init__(self, values)

    self.nextPageStart: int = values.pop("nextPageStart", None)
    self.values: List[PullRequestStatus] = list(map(PullRequestStatus, values.pop("values", []))) if "values" in values else None

    DataWithUnknownProperties.__init__(self, values)


class PullRequestMergeStatus(PullRequestStatus):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.sourceBranchDeleted: bool = None

    PullRequestStatus.__init__(self, values)


class PullRequestVeto(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.detailedMessage: str = values.pop("detailedMessage", None)
    self.summaryMessage: str = values.pop("summaryMessage", None)

    DataWithUnknownProperties.__init__(self, values)


class Repository(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.forkable: bool = values.pop("forkable", None)
    self.id: int = values.pop("id", None)
    self.links: Links = Links(values=values.pop("links")) if "links" in values else None
    self.name: str = values.pop("name", None)
    self.origin: Repository = Repository(values=values.pop("origin")) if "origin" in values else None
    self.project: Project = Project(values=values.pop("project")) if "project" in values else None
    self.public: bool = values.pop("public", None)
    self.scmId: str = values.pop("scmId", None)
    self.slug: str = values.pop("slug", None)
    self.state: str = values.pop("state", None)
    self.statusMessage: str = values.pop("statusMessage", None)

    DataWithUnknownProperties.__init__(self, values)


class SearchGroupResult(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.category: str = values.pop("category", None)
    self.count: int = values.pop("count", None)
    self.isLastPage: int = values.pop("isLastPage", None)
    self.nextStart: int = values.pop("nextStart", None)
    self.start: int = values.pop("start", None)
    self.values: List[SearchResult] = list(map(SearchResult, values.pop("values", []))) if "values" in values else None

    DataWithUnknownProperties.__init__(self, values)


class SearchResult(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.file: str = values.pop("file", None)
    self.hitContexts: List[List[SearchResultHit]] = list(map(lambda vals: list(map(SearchResultHit, vals)), values.pop("hitContexts", []))) if "hitContexts" in values else None
    self.hitCount: int = values.pop("hitCount", None)
    self.pathMatches: List[SearchResultPathMatch] = list(map(SearchResultPathMatch, values.pop("pathMatches", []))) if "pathMatches" in values else None
    self.repository: Repository = Repository(values=values.pop("repository")) if "repository" in values else None

    DataWithUnknownProperties.__init__(self, values)


class SearchResultHit(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.line: int = values.pop("line", None)
    self.text: str = values.pop("text", None)

    DataWithUnknownProperties.__init__(self, values)


class SearchResultPathMatch(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.match: bool = values.pop("match", None)
    self.text: str = values.pop("text", None)

    DataWithUnknownProperties.__init__(self, values)


class SearchResultQuery(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.substituted: bool = values.pop("substituted", None)

    DataWithUnknownProperties.__init__(self, values)


class SearchResultScope(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.type: str = values.pop("type", None)

    DataWithUnknownProperties.__init__(self, values)


class SearchResults(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.code: SearchGroupResult = SearchGroupResult(values=values.pop("code")) if "code" in values else None
    self.query: SearchResultQuery = SearchResultQuery(values=values.pop("query")) if "query" in values else None
    self.scope: SearchResultScope = SearchResultScope(values=values.pop("scope")) if "scope" in values else None

    DataWithUnknownProperties.__init__(self, values)


class Tag(DataWithUnknownProperties, DisplayIdAndId):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    DisplayIdAndId.__init__(self, values)

    self.hash: str = values.pop("hash", None)
    self.latestChangeset: str = values.pop("latestChangeset", None)
    self.latestCommit: str = values.pop("latestCommit", None)

    DataWithUnknownProperties.__init__(self, values)


class User(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    values = values if values is not None else {}

    self.active: bool = values.pop("active", None)
    self.deletable: bool = values.pop("deletable", None)
    self.displayName: str = values.pop("displayName", None)
    self.emailAddress: str = values.pop("emailAddress", None)
    self.id: int = values.pop("id", None)
    self.lastAuthenticationTimestamp: int = values.pop("lastAuthenticationTimestamp", None)
    self.links: Links = Links(values=values.pop("links")) if "links" in values else None
    self.mutableDetails: bool = values.pop("mutableDetails", None)
    self.mutableGroups: bool = values.pop("mutableGroups", None)
    self.name: str = values.pop("name", None)
    self.slug: str = values.pop("slug", None)
    self.type: str = values.pop("type", None)

    DataWithUnknownProperties.__init__(self, values)


class ScriptArgPullRequest(TypeWithDictRepr):
  url_regex: str = r"https://([^/]+)/(projects|users)/([^/]+)/repos/([^/]+)/pull-requests/([^/]+)"

  def __init__(
    self,
    url: str = None,
    project: str = None,
    repo: str = None,
    pr_id: int = None,
  ):
    self.url: str = url
    self.project: str = project
    self.repo: str = repo
    self.pr_id: int = pr_id

    self.project_type: str = ""

    if self.url:
      import re

      matches: List[List[str]] = re.findall(ScriptArgPullRequest.url_regex, self.url)
      if not matches:
        raise ValueError("Could not extract arguments from URL: %s" % self.url)

      matched = matches[0]
      self.pr_id: int = int(matched[4])
      self.project: str = matched[2]
      self.project_type: str = matched[1]
      self.repo: str = matched[3]

      if self.project_type == "users" and not self.project.startswith("~"):
        self.project = "~" + self.project

    else:
      if self.pr_id and self.project and self.repo:

        if self.project.startswith("~"):
          self.project_type = "users"
        else:
          self.project_type = "projects"

        self.url = ("https://stash.wlth.fr/projects/%s/repos/%s/pull-requests/%s/overview" % (self.project, self.repo, self.pr_id))
      else:
        raise ValueError("Either the URL (via --url) or project/repo/id (via --project/--repo/--id) arguments must be specified.")


class ScriptArgsPullRequestSelections(object):

  def __init__(self, args: argparse.Namespace):
    self.participant_status: List[PullRequestParticipantStatus] = args.participant_status
    self.role: PullRequestRole = args.role
    self.state: PullRequestState = args.state
    self.state_all: bool = args.state_all

    if self.state_all:
      self.state = None

  @staticmethod
  def add_arguments_to_parser(arg_parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    arg_parser.add_argument("--participant-status", type=PullRequestParticipantStatus, choices=list(PullRequestParticipantStatus), nargs="*")
    arg_parser.add_argument("--role", type=PullRequestRole, choices=list(PullRequestRole))
    arg_parser.add_argument("--state", type=PullRequestState, choices=list(PullRequestState), default=PullRequestState.OPEN)
    arg_parser.add_argument("--state-all", action=opts_actions.STORE_TRUE)
    return arg_parser
