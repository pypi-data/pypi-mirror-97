#!/usr/bin/env python

import requests
import logging
from cloudutils.instance import Instance


class InstanceGCE(Instance):

    GCP_METADATA_HEADERS = {
        "Metadata-Flavor": "Google"
    }

    GCP_METADATA_URL = 'http://169.254.169.254/computeMetadata/v1'

    FILTER_TAGS = ['', 'block-project-ssh-keys', 'sshKeys']

    def __init__(self, **kwargs):
        self.is_gce = True
        self.provider = "gcp"
        self.project = self.get_project()
        self.region = self.get_region()
        self.zone = self.get_zone()

    def load_tags(self, **kwargs):
        self.tags = self.get_tags()
        return self

    def get_project(self, **kwargs):
        return requests.get("%s/project/project-id" % (self.GCP_METADATA_URL),
                            headers=self.GCP_METADATA_HEADERS).content

    def get_zone(self, **kwargs):
        zone = requests.get("%s/instance/zone" % (self.GCP_METADATA_URL),
                            headers=self.GCP_METADATA_HEADERS).content.split("/")[3]

        return zone

    def get_region(self, **kwargs):
        return self.get_zone()[:-2]

    def datacenter(self, **kwargs):
        if "datacenter" in self.tags:
            return self.tags['datacenter']
        else:
            return None

    def get_tags(self, **kwargs):
        tags = {}

        instance_tags = requests.get("%s/instance/attributes/" % (self.GCP_METADATA_URL),
                                     headers=self.GCP_METADATA_HEADERS).content.split("\n")
        for tag in instance_tags:
            if tag not in self.FILTER_TAGS:
                value = requests.get("%s/instance/attributes/%s" %
                                     (self.GCP_METADATA_URL, tag), headers=self.GCP_METADATA_HEADERS).content
                if "," in value:
                    tags[tag] = value.split(",")
                else:
                    tags[tag] = self.autoconvert(value)

        return tags

    def boolify(self, s, **kwargs):
        if s == 'True':
            return True
        if s == 'False':
            return False
        raise ValueError("not bool")

    def autoconvert(self, s, **kwargs):
        for fn in (self.boolify, int, float):
            try:
                return fn(s)
            except ValueError:
                pass
        return s
