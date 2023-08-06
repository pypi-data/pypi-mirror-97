#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import os

if 'COMAP_SMART_HOME_USERNAME' in os.environ and 'COMAP_SMART_HOME_PASSWORD' in os.environ:
    _USERNAME = os.environ['COMAP_SMART_HOME_USERNAME']
    _PASSWORD = os.environ['COMAP_SMART_HOME_PASSWORD']
else:
    print('No COMAP Smart Home credentials available.\nPlease add your credentials to your environment. ')

_AUTHENTICATION_URL = 'https://authentication.comapsmarthome.com/auth/realms/smarthome-prod/protocol/openid-connect/token'


class ClientAuth(object):
    def __init__(self, username=_USERNAME, password=_PASSWORD):
        self.username = username
        self.password = password
        self._token = None
        self._refresh_token = None
        self._token_expiration = None
        self._refresh_token_expiration = None
        self.authentication_url = _AUTHENTICATION_URL
        self._get_new_token()

    @property
    def token(self):
        if time.time() > self._token_expiration:
            if time.time() > self._refresh_token_expiration:
                self._get_new_token()
            else:
                self._refresh_current_token()
        return self._token

    def _get_new_token(self):
        data = {"grant_type": "password", "client_id": "smarthome-webapp", "password": self.password, "username": self.username}

        r = requests.post(url=self.authentication_url, data=data)
        r.raise_for_status()
        data = r.json()
        self._token = data["access_token"]
        self._token_expiration = time.time() + data["expires_in"]
        self._refresh_token = data["refresh_token"]
        self._refresh_token_expiration = time.time() + data["refresh_expires_in"]

    def _refresh_current_token(self):
        if self._token:
            data = {"grant_type": "refresh_token", "client_id": "smarthome-webapp", "refresh_token": self._refresh_token}

            r = requests.post(url=self.authentication_url, data=data)
            r.raise_for_status()
            data = r.json()
            self._token = data["access_token"]
            self._token_expiration = time.time() + data["expires_in"]
            self._refresh_token = data["refresh_token"]
            self._refresh_token_expiration = time.time() + data["refresh_expires_in"]


if __name__ == '__main__':
    auth = ClientAuth()
