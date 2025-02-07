import os

import requests


API_URL = os.environ["JUPYTERHUB_API_URL"]
JUPYTERHUB_API_TOKEN = os.environ["JUPYTERHUB_API_TOKEN"]


class HubClient:
    def __init__(self, token=None):
        self.token = token or JUPYTERHUB_API_TOKEN

    def _headers(self):
        return {"Authorization": f"token {self.token}"}

    def get_users(self):
        r = requests.get(API_URL + "/users", headers=self._headers())
        r.raise_for_status()
        users = r.json()
        return users

    def get_user(self, user):
        params = {"include_stopped_servers": True}
        r = requests.get(
            API_URL + f"/users/{user}", params=params, headers=self._headers()
        )
        r.raise_for_status()
        user = r.json()
        return user

    def get_server(self, username, servername):
        user = self.get_user(username)
        for name, server in user["servers"].items():
            if name == servername:
                return server

    def create_server(self, username, servername, edit=True, params=None):
        server = self.get_server(username, servername)
        if server:
            if edit:
                self.delete_server(username, server["name"])
            else:
                raise ValueError(f"Server: {servername} already exists")
        url = f"/users/{username}/servers/{servername}"
        params = params or {}
        data = {"jhub_app": True, **params}
        r = requests.post(API_URL + url, headers=self._headers(), json=data)
        r.raise_for_status()
        return r.status_code

    def delete_server(self, username, server_name):
        url = f"/users/{username}/servers/{server_name}"
        params = {"remove": True}
        r = requests.delete(API_URL + url, headers=self._headers(), json=params)
        r.raise_for_status()
        return r.status_code
