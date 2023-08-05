#!/usr/bin/env python
#
# Copyright (C) 2020-2021 Ryan Galloway (ryan@rsg.io)
#

__doc__ = """
Contains client class and functions.
"""

import os
import sys
import json
import base64
import hashlib
import requests
import tempfile
import zipfile

import subfork.config as config
from subfork.logger import log


def create_zip_file(template):
    """Creates a zip file for a given site template."""

    template_dir = os.path.dirname(template)

    def zipdir(path, ziph):
        os.chdir(path)
        for root, _, files in os.walk('.'):
            for f in files:
                ziph.write(os.path.join(root, f))

    log.debug('template dir {}'.format(os.path.abspath(template_dir)))
    tempdir = tempfile.mkdtemp()
    template_zip = os.path.join(tempdir, 'template.zip')
    log.debug('upload file: {}'.format(template_zip))
    zipf = zipfile.ZipFile(template_zip, 'w', zipfile.ZIP_DEFLATED)
    zipdir(template_dir, zipf)
    zipf.close()
    log.debug('done')

    return template_zip


def minify_js(source):
    """Javascript minimization."""
    from slimit import minify
    return minify(source, mangle=True, mangle_toplevel=True)


def read_template(template_file):
    """Reads site template file."""
    import yaml

    if not os.path.exists(template_file):
        return

    with open(template_file) as stream:
        data = yaml.safe_load(stream)

    return data


class SubforkClient(object):
    """Subfork client connection class."""

    def __init__(self, host, access_key, secret_key):
        self.base_url = 'http://{0}'.format(host)
        self.api_url = '{}/api'.format(self.base_url)
        self.__auth = (access_key, hashlib.sha256(
            '{accesskey}:{secretkey}'.format(
                accesskey=access_key,
                secretkey=secret_key).encode('utf-8')
            ).hexdigest())

    def __post_request(self, url, data={}, file_data=None):
        """POST a request to subfork api endpoints."""
        log.debug(url)

        if file_data:
            resp = requests.post(url, auth=self.__auth,
                data=data, files={
                    'json': (None, json.dumps(data)),
                    'file': ('template.zip', file_data)
                }
            )
        else:
            resp = requests.post(url, auth=self.__auth,
                json=data, data=data
            )

        return resp

    def deploy(self, template_file):
        """Deploy a site template."""

        if not os.path.exists(template_file):
            log.error('file not found: {}'.format(template_file))
            return

        log.info('template: {}'.format(template_file))
        template_data = read_template(template_file)

        domain = template_data.get('domain')
        if not domain:
            raise Exception('domain must be defined')
        name = template_data.get('name')
        if not name:
            raise Exception('name must have a value')
        template_zip = create_zip_file(template_file)
        if not os.path.exists(template_zip):
            raise Exception('file not found: {}'.format(template_zip))

        log.info('preparing site data for deployment')
        fp = open(template_zip, 'rb')
        file_data = fp.read()
        fp.close()
        log.debug('done')

        data = {'domain': domain, 'name': name}
        url = '{}/deploy'.format(self.api_url)
        resp = self.__post_request(url, data, file_data=file_data)

        if resp.ok:
            log.info(resp.content.decode())
        else:
            log.error({
                403: 'unauthorized',
                404: 'not found',
                500: 'server error'
            }.get(resp.status_code, 'error {}'.format(resp.status_code)))

        log.debug('done')
