# -*- coding: utf-8 -*-
"""AWS class file."""
import boto3


class AWS:
    """AWS Class."""

    def __init__(self, access_key_id, secret_access_key):
        """Initialize an AWS class instance."""
        self.params = {
            "aws_access_key_id": access_key_id,
            "aws_secret_access_key": secret_access_key,
        }

    def assume_role(self, role, resource):
        """Return the credentials for an assumed role."""
        client = boto3.client("sts", **self.params)
        assumedRoleObject = client.assume_role(
            RoleArn=role,
            RoleSessionName="AssumeRoleSession1",
        )
        return assumedRoleObject["Credentials"]

    def get_accounts(self, include_alias=True, include_summary=True):
        """Return a list of accounts."""
        role_name = "role/OrganizationAccountAccessRole"
        accounts = []
        for a in self.get_organization_accounts():
            id = a["Id"]
            print(id)
            role = f"arn:aws:iam::{id}:{role_name}"
            credentials = self.assume_role(role, "iam")
            if include_alias:
                a["alias"] = self.get_account_alias(credentials)
            if include_summary:
                a["summary"] = self.get_account_summary(credentials)
            accounts.append(a)
        return accounts

    def get_account_alias(self, credentials):
        """Return the alias for an account from assumed credentials."""
        client = boto3.client(
            "iam",
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
        return client.list_account_aliases().get("AccountAliases", [None])[0]

    def get_account_summary(self, credentials):
        """Return the summary for an account from assumed credentials."""
        iam = boto3.resource(
            "iam",
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
        return iam.AccountSummary().summary_map

    def get_organization_accounts(self):
        """Return a list of organization AWS accounts."""
        client = boto3.client("organizations", **self.params)
        response = client.list_accounts()
        accounts = response.get("Accounts", [])
        next_token = response.get("NextToken")
        while next_token:
            response = client.list_accounts(NextToken=next_token)
            next_token = response.get("NextToken")
            accounts += response.get("Accounts", [])
        return accounts
