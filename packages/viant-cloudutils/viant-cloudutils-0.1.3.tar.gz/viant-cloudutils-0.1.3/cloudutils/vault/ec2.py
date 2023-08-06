#!/usr/bin/env python

import sys
import logging
import base64
import json
import requests
import botocore.session
from botocore.awsrequest import create_request_object
from retry import retry
from cloudutils.vault import Vault
import json

log = logging.getLogger(__name__)


class VaultEC2(Vault):

    def __init__(self, vault_server, instance_object,  **kwargs):
        self.vault_server = vault_server
        self.token = None
        self.login(provider='aws', login_payload=self.generate_vault_auth_payload(
            instance_object=instance_object))

    def headers_to_go_style(self, headers, **kwargs):
        retval = {}
        for k, v in headers.iteritems():
            retval[k] = [v]
        return retval

    @retry(tries=3)
    def generate_vault_auth_payload(self, instance_object, **kwargs):
        '''
        Generate request payload for Vault login
        '''
        try:
            session = botocore.session.get_session()
            client = session.create_client('sts')
            endpoint = client._endpoint
            operation_model = client._service_model.operation_model('GetCallerIdentity')
            request_dict = client._convert_to_request_dict({}, operation_model)
            request_dict['headers']['X-Vault-AWS-IAM-Server-ID'] = self.vault_server
            request = endpoint.create_request(request_dict, operation_model)

            headers = json.dumps(self.headers_to_go_style(dict(request.headers)))

            role_with_environment = ["development","staging"]

            if instance_object.tags['environment'] in role_with_environment:
                role = "{service}-{environment}-{region}".format(
                    service=instance_object.tags['service'],
                    environment=instance_object.tags['environment'],
                    region=instance_object.region,
                )
            else:
                role = "{service}-{region}".format(
                    service=instance_object.tags['service'],
                    region=instance_object.region,
                )

            return {
                'role': role,
                'iam_http_request_method': request.method,
                'iam_request_url':         base64.b64encode(request.url),
                'iam_request_body':        base64.b64encode(request.body),
                'iam_request_headers':     base64.b64encode(headers),
            }
        except Exception as e:
            log.error('Failed to generate auth payload! %s: %s' % (type(e).__name__, e))
            raise
