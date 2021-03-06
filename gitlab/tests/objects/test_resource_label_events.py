"""
GitLab API: https://docs.gitlab.com/ee/api/resource_label_events.html
"""

import pytest
import responses

from gitlab.v4.objects import (
    GroupEpicResourceLabelEvent,
    ProjectIssueResourceLabelEvent,
    ProjectMergeRequestResourceLabelEvent,
)


@pytest.fixture()
def resp_group_epic_request_label_events():
    epic_content = {"id": 1}
    events_content = {"id": 1, "resource_type": "Epic"}
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/epics",
            json=[epic_content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/epics/1/resource_label_events",
            json=[events_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_merge_request_label_events():
    mr_content = {"iid": 1}
    events_content = {"id": 1, "resource_type": "MergeRequest"}
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests",
            json=[mr_content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1/resource_label_events",
            json=[events_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_project_issue_label_events():
    issue_content = {"iid": 1}
    events_content = {"id": 1, "resource_type": "Issue"}
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/issues",
            json=[issue_content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/issues/1/resource_label_events",
            json=[events_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_project_issue_label_events(project, resp_project_issue_label_events):
    issue = project.issues.list()[0]
    label_events = issue.resourcelabelevents.list()
    assert isinstance(label_events, list)
    label_event = label_events[0]
    assert isinstance(label_event, ProjectIssueResourceLabelEvent)
    assert label_event.resource_type == "Issue"


def test_merge_request_label_events(project, resp_merge_request_label_events):
    mr = project.mergerequests.list()[0]
    label_events = mr.resourcelabelevents.list()
    assert isinstance(label_events, list)
    label_event = label_events[0]
    assert isinstance(label_event, ProjectMergeRequestResourceLabelEvent)
    assert label_event.resource_type == "MergeRequest"


def test_group_epic_request_label_events(group, resp_group_epic_request_label_events):
    epic = group.epics.list()[0]
    label_events = epic.resourcelabelevents.list()
    assert isinstance(label_events, list)
    label_event = label_events[0]
    assert isinstance(label_event, GroupEpicResourceLabelEvent)
    assert label_event.resource_type == "Epic"
