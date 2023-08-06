#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.accounts.account import GerritAccount


class GerritAccounts(object):
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def search(self, query):
        """
        Queries accounts visible to the caller.

        :param query:
        :return:
        """
        endpoint = "/accounts/?suggest&q=%s" % query
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return GerritAccount.parse_list(result, gerrit=self.gerrit)

    def whoami(self):
        """
        who am i

        :return:
        """
        endpoint = "/accounts/self"
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.get(result.get("username"))

    def get(self, username):
        """
        Returns an account

        :param username:
        :return:
        """
        endpoint = "/accounts/%s/detail" % username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return GerritAccount.parse(result, gerrit=self.gerrit)

    def create(self, username, input_):
        """
        Creates a new account.

        .. code-block:: python

            input_ = {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "ssh_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA0T...YImydZAw==",
                "http_password": "19D9aIn7zePb",
                "groups": [
                  "MyProject-Owners"
                ]
            }
            new_account = gerrit.accounts.create('john.doe', input_)

        :param username: account username
        :param input_: the AccountInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-accounts.html#account-input
        :return:
        """
        endpoint = "/accounts/%s" % username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return GerritAccount.parse(result, gerrit=self.gerrit)
