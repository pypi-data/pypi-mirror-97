# -*- coding: utf-8 -*-

"""
Copyright 2018 Axibase Corporation or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

https://www.axibase.com/atsd/axibase-apache-2.0.pdf

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
"""
import logging, requests, sys
from requests.compat import urljoin
from . import _jsonutil
from .exceptions import ServerException
import datetime

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Client(object):
    """
    low level request wrapper
    sets method, path, payload
    returns response data
        or True if request is successful without content
    """

    def __init__(self, base_url,
                 username=None, password=None,
                 ssl_verify=False, timeout=None):
        """
        :param base_url: ATSD url
        :param username: login
        :param password:
        :param ssl_verify: verify ssl certificate
        :param timeout: request timeout
        """
        logging.debug('Connecting to ATSD at %s as %s user.' % (base_url, username))
        self.context = urljoin(base_url, 'api/')
        session = requests.Session()
        if ssl_verify is False or ssl_verify == 'False':
            session.verify = False
        if username is not None and password is not None:
            session.auth = (username, password)
        self.session = session
        self.timeout = int(timeout) if timeout is not None else None
        self.client_version = sys.modules[_jsonutil.__package__].__version__
        self.python_version = sys.version_info[:3]

    def _request(self, method, path, params=None, json=None, data=None, portal=False, portal_file=None):
        request = requests.Request(
            method=method,
            url=urljoin(self.context, path),
            data=data,
            json=_jsonutil.serialize(json),
            params=params,
            headers={
                'user-agent': 'atsd-api-python/{} python/{}.{}.{}'.format(self.client_version, *self.python_version)}
        )
        prepared_request = self.session.prepare_request(request)
        response = self.session.send(prepared_request, timeout=self.timeout, stream=portal)
        if not (200 <= response.status_code < 300):
            raise ServerException(response.status_code, response.text)
        try:
            if portal:
                if not portal_file:
                    portal_name = response.headers.get("Content-Disposition").split("\"")[1]
                    file_name = {"name": portal_name.split(".")[0],
                                 "entity": "" if params["entity"] is None else "_{}".format(params["entity"]),
                                 "date": datetime.datetime.now().strftime("%Y%m%d")}
                    portal_file = "{name}{entity}_{date}.png".format(**file_name)
                image = response.raw.read()
                with open(portal_file, 'wb') as f:
                    f.write(image)
            return response.json()
        except ValueError:
            return response.text

    def post(self, path, data, params=None):
        return self._request('POST', path, params=params, json=data)

    def post_plain_text(self, path, data, params=None):
        return self._request('POST', path, params=params, data=data)

    def patch(self, path, data):
        return self._request('PATCH', path, json=data)

    def get(self, path, params=None, portal=False, portal_file=None):
        return self._request('GET', path, params=params, portal=portal, portal_file=portal_file)

    def put(self, path, data):
        return self._request('PUT', path, json=data)

    def delete(self, path):
        return self._request('DELETE', path)

    def close(self):
        self.session.close()
