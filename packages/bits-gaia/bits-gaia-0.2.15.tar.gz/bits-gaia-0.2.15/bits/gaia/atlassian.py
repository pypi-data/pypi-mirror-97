# -*- coding: utf-8 -*-
"""Atlassian class file."""
import requests


class Atlassian:
    """Atlassian class."""

    def __init__(self, username, token, base_url="https://broadinstitute.atlassian.net"):
        """Initialize an Atlassian class instance."""
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (username, token)
        self.session.headers.update({
            "Accept": "application/json",
        })

    def get_group_members(self, group, includeInactiveUsers=False):
        """Return a list of members in a group."""
        url = f"{self.base_url}/rest/api/3/group/member"
        params = {
            "groupname": group,
            "includeInactiveUsers": includeInactiveUsers,
            "maxResults": 1000,
        }
        response = self.session.get(url, params=params).json()
        members = response.get("values", [])
        while not response.get("isLast", False):
            nextPage = response["nextPage"]
            response = self.session.get(nextPage).json()
            members.extend(response.get("values", []))
        return members

    def get_groups(self):
        """Return a list of all Atlassian Groups."""
        url = f"{self.base_url}/rest/api/3/groups/picker"
        params = {
            "maxResults": 1000,
        }
        response = self.session.get(url, params=params).json()
        groups = response["groups"]
        total = response["total"]
        if len(groups) < total:
            print(f"WARNING: {response['header']}")
        return groups

    def get_groups_with_members(self):
        """Return a list of all Atlassian Groups and their members."""
        groups = self.get_groups()
        for group in groups:
            name = group["name"]
            group["members"] = self.get_group_members(name)
        return groups

    def get_users(self):
        """Return a list of all Atlassian Users."""
        url = f"{self.base_url}/rest/api/3/users/search"
        count = 1000
        params = {
            "maxResults": count,
            "startAt": 0,
        }
        users = []
        while True:
            results = self.session.get(url, params=params).json()
            if results:
                users.extend(results)
            if len(results) < count:
                break
            params["startAt"] += count
        return users
