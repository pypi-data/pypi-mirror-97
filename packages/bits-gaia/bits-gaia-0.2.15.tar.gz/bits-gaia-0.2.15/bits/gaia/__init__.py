# -*- coding: utf-8 -*-
"""Gaia class file."""
import json
import logging
import os
from datetime import datetime

import requests
import yaml
from google.cloud import storage
from google.cloud.secretmanager_v1 import SecretManagerServiceClient

from .auth import Auth

BIGQUERY_IMPORTS_BUCKET = os.environ.get("BIGQUERY_IMPORTS_BUCKET")
CONFIG_BUCKET = os.environ.get("CONFIG_BUCKET")
FIRESTORE_IMPORTS_BUCKET = os.environ.get("FIRESTORE_IMPORTS_BUCKET")


class Gaia:
    """Gaia class."""

    def __init__(self, verbose=False):
        """Initialize a new Gaia class."""
        self.config = None
        self.project = None

        self.auth = Auth(self)
        self.verbose = verbose

    def get_config(self):
        """Return a dictionary of config settings."""
        if self.config:
            return self.config
        blob = storage.Client().bucket(CONFIG_BUCKET).blob("config.yaml")
        yaml_string = blob.download_as_string()
        docs = yaml.load_all(yaml_string, Loader=yaml.Loader)
        self.config = {}
        for doc in docs:
            for key, value in doc.items():
                self.config[key] = value
        return self.config

    def get_people_dict(self):
        """Return a dict of People from the People MySQL DB."""
        pdb = self.auth.people_mysql()
        person_types = pdb.get_table_dict("person_types")
        today = datetime.today().strftime("%Y-%m-%d")
        people = {}
        for person in pdb.get_table("people"):
            person = json.loads(json.dumps(person, default=str))
            key = person["id"]
            first_name = person["first_name"]
            last_name = person["last_name"]
            person["full_name"] = f"{first_name} {last_name}"
            person_type_id = person["person_type_id"]
            person["person_type"] = person_types.get(person_type_id)
            start_date = person["start_date"]
            person["future_hire"] = 1 if start_date > today else 0
            people[key] = person
        return people

    def get_project(self):
        """Return the project ID of the current environment."""
        if "GCP_PROJECT" in os.environ:
            return os.environ["GCP_PROJECT"]
        return requests.get(
            "http://metadata.google.internal/computeMetadata/v1/project/project-id",
            headers={"Metadata-Flavor": "Google"},
        ).text

    def get_secret(self, name):
        """Return the auth data from the request_json."""
        if not self.project:
            self.project = self.get_project()
        client = SecretManagerServiceClient()
        secret_path = client.secret_version_path(self.project, name, "latest")
        request = {"name": secret_path}
        return client.access_secret_version(request=request).payload.data.decode("utf-8")

    def get_settings(self, name):
        """Return the configuration settings for a specific service name."""
        return self.get_config().get(name)

    def save_bigquery_import(self, dataset, table, entries):
        """Save entries to import bucket."""
        bucketname = BIGQUERY_IMPORTS_BUCKET
        print(f"BigQuery Bucket Name: {bucketname}")
        blobname = f"{dataset}/{table}.json"
        print(f"BigQuery Blob Name: {blobname}")
        blobstring = "\n".join([json.dumps(e, default=str) for e in entries])
        blob = storage.Client().bucket(bucketname).blob(blobname)
        blob.upload_from_string(blobstring, content_type="application/json")
        return blob

    def save_firestore_import(self, dataset, table, entries):
        """Save entries to import bucket."""
        bucketname = FIRESTORE_IMPORTS_BUCKET
        print(f"Firestore Bucket Name: {bucketname}")
        timestamp = datetime.isoformat(datetime.now())
        blobname = f"{dataset}/{dataset}_{table}_{timestamp}.json"
        print(f"Firestore Blob Name: {blobname}")
        blobstring = json.dumps(entries, sort_keys=True, default=str)
        blob = storage.Client().bucket(bucketname).blob(blobname)
        blob.upload_from_string(blobstring, content_type="application/json")
        return blob

    def save_import(self, dataset, table, entries, description=None, bigquery=True, firestore=True):
        """Save an import in bigquery and/or firestore."""
        if not description:
            description = f"{dataset}_{table}"
        if firestore:
            try:
                print(f"Saving {description} for Firestore...")
                blob = self.save_firestore_import(dataset, table, entries)
                print(f"Saved {description} to gs://{blob.bucket.name}/{blob.name}.")
            except Exception as error:
                logging.error(f"Failed saving {description} for Firestore: {error}")
        if bigquery:
            try:
                print(f"Saving {description} for BigQuery...")
                blob = self.save_bigquery_import(dataset, table, entries)
                print(f"Saved {description} to gs://{blob.bucket.name}/{blob.name}.")
            except Exception as error:
                logging.error(f"Failed saving {description} for BigQuery: {error}")
