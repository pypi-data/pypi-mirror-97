import datetime
import logging
import re
import unicodedata

import arrow
import requests
from dateutil import tz

from taxi import __version__ as taxi_version
from taxi.aliases import aliases_database
from taxi.backends import BaseBackend, PushEntryFailed
from taxi.exceptions import TaxiException
from taxi.projects import Activity, Project

logger = logging.getLogger(__name__)


def slugify(value):
    value = str(value)
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


class ClockifyBackend(BaseBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._authenticated = False
        self._session = requests.Session()
        self._session.headers.update({"user-agent": "Taxi {}".format(taxi_version)})
        self._user_info = None
        self.timezone = self.options.get("timezone", "CET")
        self.workspace_id = self.options.get("workspace")

        if tz.gettz(self.timezone) is None:
            raise TaxiException(
                f"Invalid timezone {self.timezone}. Please check your configuration file by running `taxi config` and fix the `timezone` option of the backend."
            )

    def get_api_url(self, url):
        return "https://api.clockify.me/api/v1/{url}".format(url=url.lstrip("/"))

    def clockify_request(self, method, url, **kwargs):
        headers = {"X-Api-Key": self.options["token"]}
        response = self._session.request(
            method=method, url=url, headers=headers, **kwargs
        )

        if response.status_code in {401, 403}:
            raise TaxiException("Login failed, please check your credentials")

        return response

    def get_workspace_id(self):
        if self.workspace_id is None:
            workspaces_response = self.clockify_request(
                "get", self.get_api_url("/workspaces")
            )

            if workspaces_response.status_code != 200:
                raise TaxiException(
                    f"Could not get workspaces list, got error {workspaces_response.status_code}: {workspaces_response.content}."
                )

            workspaces = workspaces_response.json()

            if len(workspaces) > 0:
                raise TaxiException(
                    "You have more than one workspace available. Please add the workspace option to your backend url (eg. `clockify://?token=xxx&workspace=yyy`)."
                )

            self.workspace_id = workspaces[0]["id"]

        return self.workspace_id

    def push_entry(self, date, entry):
        workspace_id = self.get_workspace_id()
        push_url = self.get_api_url(
            "/workspaces/{workspace_id}/time-entries".format(workspace_id=workspace_id)
        )

        if not isinstance(entry.duration, tuple):
            raise PushEntryFailed(
                "Only durations with a start and end time are supported."
            )

        start_datetime = datetime.datetime.combine(date, entry.get_start_time())
        end_datetime = datetime.datetime.combine(date, entry.duration[1])

        start_datetime_str = (
            arrow.get(start_datetime, self.timezone)
            .to("UTC")
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        end_datetime_str = (
            arrow.get(end_datetime, self.timezone)
            .to("UTC")
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        project_id, task_id = aliases_database[entry.alias].mapping

        response = self.clockify_request(
            "post",
            push_url,
            json={
                "start": start_datetime_str,
                "end": end_datetime_str,
                "projectId": project_id,
                "taskId": task_id,
                "description": entry.description,
            },
        )

        if response.status_code != 201:
            raise PushEntryFailed(response.content)

    def get_projects(self):
        workspace_id = self.get_workspace_id()
        projects_url = self.get_api_url(
            "/workspaces/{workspace_id}/projects".format(workspace_id=workspace_id)
        )

        try:
            response = self.clockify_request("get", projects_url)
            projects = response.json()
        except ValueError:
            raise TaxiException(
                "Unexpected response from the server (%s).  Check your "
                "credentials" % response.content
            )

        projects_list = []
        for project in projects:
            p = Project(
                project["id"],
                project["name"],
                Project.STATUS_ACTIVE,
                "",
                project["budgetEstimate"],
            )

            tasks_url = self.get_api_url(
                "/workspaces/{workspace_id}/projects/{project_id}/tasks".format(
                    workspace_id=workspace_id, project_id=project["id"]
                )
            )
            tasks = self.clockify_request("get", tasks_url).json()

            for task in tasks:
                a = Activity(task["id"], task["name"])
                p.add_activity(a)
                p.aliases[slugify(a.name)] = task["id"]

            projects_list.append(p)

        return projects_list
