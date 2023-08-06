import os
import time
import requests


class Client:
    """
    A client for interacting with the Formant Cloud. There are methods for:
    - Ingesting telemetry datapoints for device(s)
    - Query telemetry datapoints
    Requires service account credentials (environment variables):
    - FORMANT_EMAIL
    - FORMANT_PASSWORD
    """

    def __init__(
        self,
        admin_api="https://api.formant.io/v1/admin",
        ingest_api="https://api.formant.io/v1/ingest",
        query_api="https://api.formant.io/v1/queries",
    ):
        self._admin_api = admin_api
        self._ingest_api = ingest_api
        self._query_api = query_api

        self._email = os.getenv("FORMANT_EMAIL")
        self._password = os.getenv("FORMANT_PASSWORD")
        if self._email is None:
            raise ValueError("Missing FORMANT_EMAIL environment variable")
        if self._password is None:
            raise ValueError("Missing FORMANT_PASSWORD environment variable")

        self._headers = {
            "Content-Type": "application/json",
            "App-ID": "formant/python-cloud-sdk",
        }
        self._token = None
        self._token_expiry = 0

    def ingest(self, params):
        """Administrator credentials required.
        Example ingestion params:
        {
            deviceId: "ced176ab-f223-4466-b958-ff8d35261529",
            name: "engine_temp",
            type: "numeric",
            tags: {"location":"sf"},
            points: [...],
        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/batch" % self._ingest_api, headers=headers, json=params
            )
            response.raise_for_status()

        self._authenticate_request(call)

    def query(self, params):
        """Example query params (only start and end time are required):
        {
            start: "2021-01-01T01:00:00.000Z",
            end: "2021-01-01T02:00:00.000Z",
            deviceIds: ["99e8ee37-0a27-4a11-bba2-521facabefa3"],
            names: ["engine_temp"],
            types: ["numeric"],
            tags: {"location":["sf","la"]},
            notNames: ["speed"],
        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/queries" % self._query_api, headers=headers, json=params
            )
            response.raise_for_status()
            return response.json()

        return self._authenticate_request(call)

    def query_devices(self, params):
        """Example params to filter on (all optional)
        {
            name: "model00.001",
            tags: {"location":["sf", "la"]},
        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/devices/query" % self._admin_api, headers=headers, json=params
            )
            response.raise_for_status()
            return response.json()

        return self._authenticate_request(call)

    def _authenticate(self):
        payload = {
            "email": self._email,
            "password": self._password,
            "expirationSeconds": 3600,
        }
        response = requests.post(
            "%s/auth/access-token" % self._admin_api,
            headers=self._headers,
            json=payload,
        )
        response.raise_for_status()
        result = response.json()
        if "token" not in result:
            raise ValueError("Authentication failed")
        self._token_expiry = int(time.time()) + 3530
        self._token = result["token"]

    def _authenticate_request(self, call):
        if self._token is None or self._token_expiry < int(time.time()):
            self._authenticate()
        try:
            return call(self._token)
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 401:
                self._authenticate()
                return call(self._token)
            else:
                raise error
