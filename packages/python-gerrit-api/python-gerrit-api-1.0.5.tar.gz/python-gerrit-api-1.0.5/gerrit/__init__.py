#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import json
from gerrit.utils.requester import Requester
from gerrit.config.config import GerritConfig
from gerrit.projects.projects import GerritProjects
from gerrit.accounts.accounts import GerritAccounts
from gerrit.groups.groups import GerritGroups
from gerrit.plugins.plugins import GerritPlugins
from gerrit.changes.changes import GerritChanges


class GerritClient(object):
    """
    Python wrapper for the Gerrit V3.x REST API.

    """

    GERRIT_AUTH_SUFFIX = "/a"
    default_headers = {"Content-Type": "application/json; charset=UTF-8"}

    def __init__(
        self,
        base_url,
        username,
        password,
        ssl_verify=True,
        cert=None,
        timeout=60,
        max_retries=None,
    ):
        self._base_url = self.strip_trailing_slash(base_url)

        self.requester = Requester(
            username=username,
            password=password,
            ssl_verify=ssl_verify,
            cert=cert,
            timeout=timeout,
            max_retries=max_retries,
        )

    @classmethod
    def strip_trailing_slash(cls, url):
        """
        remove url's trailing slash
        :param url: url
        :return:
        """
        while url.endswith("/"):
            url = url[:-1]
        return url

    def get_endpoint_url(self, endpoint):
        """
        Return the complete url including host and port for a given endpoint.
        :param endpoint: service endpoint as str
        :return: complete url (including host and port) as str
        """
        return "{}{}{}".format(self._base_url, self.GERRIT_AUTH_SUFFIX, endpoint)

    @staticmethod
    def decode_response(response):
        """Strip off Gerrit's magic prefix and decode a response.
        :returns:
            Decoded JSON content as a dict, or raw text if content could not be
            decoded as JSON.
        :raises:
            requests.HTTPError if the response contains an HTTP error status code.
        """
        magic_json_prefix = ")]}'\n"
        content_type = response.headers.get("content-type", "")

        content = response.content.strip()
        if response.encoding:
            content = content.decode(response.encoding)
        if not content:
            return content
        if content_type.split(";")[0] != "application/json":
            return content
        if content.startswith(magic_json_prefix):
            index = len(magic_json_prefix)
            content = content[index:]
        try:
            return json.loads(content)
        except ValueError:
            raise ValueError("Invalid json content: {}".format(content))

    @property
    def config(self):
        """
        Config related REST APIs

        :return:
        """
        return GerritConfig(gerrit=self)

    @property
    def projects(self):
        """
        Project related REST APIs
        :return:
        """
        return GerritProjects(gerrit=self)

    @property
    def changes(self):
        """
        Change related REST APIs

        :return:
        """
        return GerritChanges(gerrit=self)

    @property
    def accounts(self):
        """
        Account related REST APIs

        :return:
        """
        return GerritAccounts(gerrit=self)

    @property
    def groups(self):
        """
        Group related REST APIs

        :return:
        """
        return GerritGroups(gerrit=self)

    @property
    def plugins(self):
        """
        Plugin related REST APIs

        :return:
        """
        return GerritPlugins(gerrit=self)

    @property
    def version(self):
        """
        get the version of the Gerrit server.

        :return:
        """
        return self.config.get_version()

    @property
    def server(self):
        """
        get the information about the Gerrit server configuration.

        :return:
        """
        return self.config.get_server_info()
