#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi

from gerrit.utils.models import BaseModel


class Dashboard(BaseModel):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        self.attributes = [
            "id",
            "ref",
            "path",
            "description",
            "url",
            "is_default",
            "title",
            "sections",
            "defining_project",
            "foreach",
            "project",
            "gerrit",
        ]

    def delete(self):
        """
        Deletes a project dashboard.

        :return:
        """
        endpoint = "/projects/%s/dashboards/%s" % (self.project, self.id)
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))


class Dashboards(object):
    def __init__(self, project, gerrit):
        self.project = project
        self.gerrit = gerrit

    def list(self):
        """
        List custom dashboards for a project.

        :return:
        """
        endpoint = "/projects/%s/dashboards/" % self.project
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Dashboard.parse_list(result, project=self.project, gerrit=self.gerrit)

    def create(self, id_, input_):
        """
        Creates a project dashboard, if a project dashboard with the given dashboard ID doesn't exist yet.

        .. code-block:: python

            input_ = {
                "id": "master:closed",
                "commit_message": "Define the default dashboard"
            }
            new_dashboard = project.dashboards.create('master:closed', input_)


        :param id_: the dashboard id
        :param input_: the DashboardInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#dashboard-input
        :return:
        """
        endpoint = "/projects/%s/dashboards/%s" % (self.project, id_)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return Dashboard.parse(result, project=self.project, gerrit=self.gerrit)

    def get(self, id_):
        """
        Retrieves a project dashboard. The dashboard can be defined on that project or be inherited from a parent project.

        :param id_: the dashboard id
        :return:
        """
        endpoint = "/projects/%s/dashboards/%s" % (self.project, id_)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Dashboard.parse(result, project=self.project, gerrit=self.gerrit)

    def delete(self, id_):
        """
        Deletes a project dashboard.

        :param id_: the dashboard id
        :return:
        """
        endpoint = "/projects/%s/dashboards/%s" % (self.project, id_)
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
