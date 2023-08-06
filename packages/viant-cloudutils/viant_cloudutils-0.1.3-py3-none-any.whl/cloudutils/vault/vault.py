#!/usr/bin/env python

from retry import retry
import requests
import logging
import json

logging.getLogger("requests").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


class Vault():

    @retry(tries=3)
    def make_request(self, method, resource, **args):
        '''
        Make a request to Vault
        '''

        def __init__(self, vault_server=None, token=None, **kwargs):
            self.token = token
            self.vault_server = vault_server

        try:
            url = "{0}/v1/{1}".format(self.vault_server, resource)
            headers = {'X-Vault-Token': self.token, 'Content-Type': 'application/json'}
            data = json.loads(requests.request(method, url, headers=headers, **args).content)
            if 'errors' in data and len(data['errors']) > 0:
                raise Exception("%s" % ','.join(data['errors']))
            else:
                return data
        except Exception as e:
            log.error('Failed to make request! %s: %s' % (type(e).__name__, e))
            raise

    def login(self, provider, login_payload, **kwargs):
        '''
        Generates Vault token from login request
        '''
        try:
            login_data = self.make_request('POST', "auth/%s/login" %
                                           (provider), data=json.dumps(login_payload))
            self.token = login_data['auth']['client_token']
        except Exception as e:
            log.error('Failed to get token! %s: %s' % (type(e).__name__, e))
            raise

    def read(self, path, key=None, **kwargs):
        '''
        Return the value of key at path in vault, or entire secret
        '''
        try:
            data = self.make_request('GET', path)['data']
            if key is not None:
                return data[key]
            return data
        except Exception as e:
            log.error('Failed to read secret! %s: %s' % (type(e).__name__, e))
            raise
