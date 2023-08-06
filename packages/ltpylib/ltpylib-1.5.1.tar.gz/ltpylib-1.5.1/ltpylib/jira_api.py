#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import re
from typing import Dict, List, Tuple, Union

from jira import JIRA
from requests import Session

from ltpylib import strconverters
from ltpylib.collect import EMPTY_LIST, EMPTY_MAP, to_csv
from ltpylib.jira_api_types import Issue, IssueSearchResult

JIRA_API_SEARCH: str = "/rest/api/2/search"
JIRA_API_SPRINTS: str = "/rest/greenhopper/latest/sprintquery/225?includeFutureSprints=true"
JIRA_API_EPICS: str = "/rest/greenhopper/latest/xboard/plan/backlog/epics"

ISSUE_FIELD_SPRINT_FINAL: str = "sprintFinal"
ISSUE_FIELD_SPRINT_RAW: str = "sprintRaw"


class JiraApi(object):

  def __init__(self, api: JIRA = None, url: str = None, auth: Tuple[str, str] = None):
    if api is not None:
      self.api: JIRA = api
    elif url is not None and auth is not None:
      self.api: JIRA = JIRA(url, auth=auth)
    else:
      raise Exception("Must be initialized with 'api: JIRA' instance or both 'url' and 'auth'")

  def get_session(self) -> Session:
    return self.api._session

  def epics(self, board_id: int) -> dict:
    return self.get_session().get(self.api.client_info() + JIRA_API_EPICS + "?rapidViewId=" + str(board_id)).json()

  def issue(
    self,
    id: str,
    fields: List[str] = None,
    expand: List[str] = None,
    # parse response config
    no_convert: bool = False,
    convert_single_value_arrays: bool = False,
    create_new_result: bool = False,
    skip_fields: List[str] = EMPTY_LIST,
    dict_field_to_inner_field: Dict[str, str] = EMPTY_MAP,
    join_array_fields: List[str] = EMPTY_LIST,
    date_fields: List[str] = EMPTY_LIST
  ) -> Issue:
    return Issue(
      values=JiraApi.parse_api_response_with_names(
        self.api.issue(
          id,
          fields=to_csv(fields),
          expand=JiraApi.expand_with_names(expand),
        ).raw,
        no_convert=no_convert,
        convert_single_value_arrays=convert_single_value_arrays,
        create_new_result=create_new_result,
        skip_fields=skip_fields,
        dict_field_to_inner_field=dict_field_to_inner_field,
        join_array_fields=join_array_fields,
        date_fields=date_fields
      )
    )

  def search_issues(
    self,
    jql: str,
    start_at: int = 0,
    max_results: int = 50,
    validate_query: bool = True,
    fields: List[str] = None,
    expand: List[str] = None,
    json_result: bool = True,
    # parse response config
    no_convert: bool = False,
    convert_single_value_arrays: bool = False,
    create_new_result: bool = False,
    skip_fields: List[str] = EMPTY_LIST,
    dict_field_to_inner_field: Dict[str, str] = EMPTY_MAP,
    join_array_fields: List[str] = EMPTY_LIST,
    date_fields: List[str] = EMPTY_LIST
  ) -> IssueSearchResult:
    return IssueSearchResult(
      values=JiraApi.parse_api_response_with_names(
        self.api.search_issues(
          jql,
          startAt=start_at,
          maxResults=max_results,
          validate_query=validate_query,
          fields=to_csv(fields),
          expand=JiraApi.expand_with_names(expand),
          json_result=json_result,
        ),
        "issues",
        no_convert=no_convert,
        convert_single_value_arrays=convert_single_value_arrays,
        create_new_result=create_new_result,
        skip_fields=skip_fields,
        dict_field_to_inner_field=dict_field_to_inner_field,
        join_array_fields=join_array_fields,
        date_fields=date_fields
      )
    )

  def issue_summaries(
    self,
    issues: List[str],
    markdown: bool = False,
    link: bool = False,
  ) -> List[str]:
    summaries = []

    for issue in issues:
      if issue.count("/") > 0:
        issue_key = issue.split("/")[-1]
      else:
        issue_key = issue

      result = self.issue(issue_key)

      if markdown:
        summary: str = "[%s](https://jira.wlth.fr/browse/%s) `%s`" % (result.key, result.key, result.summary)
      elif link:
        summary: str = "https://jira.wlth.fr/browse/%s %s" % (result.key, result.summary)
      else:
        summary: str = "%s %s" % (result.key, result.summary)

      summaries.append(summary)

    return summaries

  @staticmethod
  def expand_with_names(expand: List[str]) -> str:
    if expand is None:
      expand = []

    expand.append("names")
    return to_csv(expand)

  @staticmethod
  def parse_api_response_with_names(
    result: dict,
    convert_values_field: str = None,
    names_field: str = "names",
    fields_field: str = "fields",
    no_convert: bool = False,
    convert_single_value_arrays: bool = False,
    create_new_result: bool = False,
    skip_fields: List[str] = EMPTY_LIST,
    dict_field_to_inner_field: Dict[str, str] = EMPTY_MAP,
    join_array_fields: List[str] = EMPTY_LIST,
    date_fields: List[str] = EMPTY_LIST
  ) -> dict:
    if not convert_values_field:
      convert_values: List[Dict] = [result]
    else:
      convert_values_temp: Union[dict, List[dict]] = result.get(convert_values_field)
      if isinstance(convert_values_temp, list):
        convert_values: List[Dict] = convert_values_temp
      else:
        convert_values: List[Dict] = [convert_values_temp]

    names: Dict[str, str] = result.get(names_field)
    array_fields: List[str] = []
    convert_array_fields: List[str] = []

    for convert_value in convert_values:
      if create_new_result:
        updated_value: Dict = {}
      else:
        updated_value: Dict = convert_value

      if create_new_result:
        for entry in convert_value.items():
          if entry[0] != fields_field and not entry[0] in skip_fields:
            updated_value[entry[0]] = entry[1]
      elif skip_fields:
        for field in skip_fields:
          if field != fields_field and field in updated_value:
            updated_value.pop(field)

      if create_new_result:
        issue_fields: Dict = convert_value.get(fields_field, {})
      else:
        issue_fields: Dict = convert_value.pop(fields_field, {})

      for entry in issue_fields.items():
        key: str = entry[0]
        val = entry[1]
        if val is None:
          continue
        elif isinstance(val, list) and not val:
          continue
        elif no_convert:
          updated_value[key] = val
          continue

        orig_key: str = key
        if key.startswith("customfield_") and key in names:
          key = strconverters.to_camel_case(names.get(key))

        if key in skip_fields or orig_key in skip_fields:
          continue
        elif key == "sprint":
          sprints: List[str] = val
          val = [re.match(r".*,name=(.*?),.*", sprint).group(1).replace("Money Movement - 2019", "MM - 2019").replace("Money Movement 2019", "MM - 2019") for sprint in sprints]
          if ISSUE_FIELD_SPRINT_RAW not in skip_fields:
            updated_value[ISSUE_FIELD_SPRINT_RAW] = sprints
          if ISSUE_FIELD_SPRINT_FINAL not in skip_fields:
            updated_value[ISSUE_FIELD_SPRINT_FINAL] = val[-1]
        elif key in dict_field_to_inner_field:
          if key not in skip_fields:
            updated_value[key] = val
          inner_field: str = dict_field_to_inner_field.get(key)
          if isinstance(val, dict):
            val = val.get(inner_field)
            key = key + "_" + inner_field
          elif isinstance(val, list):
            val = [elem.get(inner_field) for elem in val]
            key = key + "_" + inner_field

        if isinstance(val, list):
          if key in join_array_fields:
            val = ",".join(val)
          elif convert_single_value_arrays:
            if key not in array_fields:
              array_fields.append(key)
              convert_array_fields.append(key)

            if len(val) > 1:
              if key in convert_array_fields:
                convert_array_fields.remove(key)
        # elif key in date_fields:
        #   val = val.replace("-0400", "").replace("-0500", "").replace("T", " ")

        updated_value[key] = val

    if not no_convert and convert_single_value_arrays and convert_array_fields:
      for field in convert_array_fields:
        for convert_value in convert_values:
          if field in convert_value and convert_value.get(field):
            convert_value[field] = "\n".join(convert_value.get(field))

    return result
