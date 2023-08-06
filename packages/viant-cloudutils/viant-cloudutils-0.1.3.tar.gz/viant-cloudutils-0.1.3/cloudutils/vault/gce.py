#!/usr/bin/env python

import requests
import logging
import urllib
from cloudutils.vault import Vault

log = logging.getLogger(__name__)


class VaultGCE(Vault):

    GCP_METADATA_HEADERS = {
        "Metadata-Flavor": "Google"
    }

    GCP_METADATA_URL = 'http://169.254.169.254/computeMetadata/v1'

    def __init__(self,  vault_server, instance_object, **kwargs):
        self.vault_server = vault_server
        self.token = None
        self.login(provider='gcp', login_payload=self.generate_vault_auth_payload(
            instance_object=instance_object))

    def generate_vault_auth_payload(self,  instance_object, **kwargs):
        try:
            role = "%s-%s" % (instance_object.tags['service'], instance_object.zone)
            url_params = [
                "audience=%s" % (urllib.quote("http://vault/%s" % (role), safe="")),
                "format=full"
            ]

            jwt = requests.get("%s/instance/service-accounts/default/identity?%s" % (self.GCP_METADATA_URL,
                                                                                     "&".join(url_params)), headers=self.GCP_METADATA_HEADERS).content

            return {"role": role, "jwt": jwt}
        except Exception as e:
            log.error('Failed to generate auth payload! %s: %s' % (type(e).__name__, e))
            raise
