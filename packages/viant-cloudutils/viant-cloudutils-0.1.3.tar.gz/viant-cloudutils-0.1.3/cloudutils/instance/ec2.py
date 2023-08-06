#!/usr/bin/env python

import requests
import logging
from cloudutils.instance import Instance

try:
    import boto3
    from botocore.credentials import InstanceMetadataProvider, InstanceMetadataFetcher
    from botocore.config import Config
except ImportError:
    print("not on AWS")  # need to handle this with an exception


class InstanceEC2(Instance):

    AWS_METADATA_HEADERS = {
    }

    AWS_METADATA_URL = "http://169.254.169.254/latest/meta-data"

    AWS_CONFIG = Config(
        retries=dict(
            max_attempts=10
        )
    )

    def __init__(self, **kwargs):
        self.is_aws = True
        self.provider = "aws"
        self.project = None
        self.zone = self.get_zone()
        self.region = self.get_region()
        self.instance_id = self.get_instance_id()

    def load_tags(self, **kwargs):
        self.tags = self.get_tags()
        return self

    def get_instance_id(self, **kwargs):
        instance_id = requests.get("%s/instance-id" % (self.AWS_METADATA_URL)).content
        return instance_id

    def get_zone(self, **kwargs):
        zone = requests.get(
            "%s/placement/availability-zone" % (self.AWS_METADATA_URL)).content
        return zone

    def get_region(self, **kwargs):
        return self.get_zone()[:-1]

    def datacenter(self, **kwargs):
        if "datacenter" in self.tags:
            return self.tags['datacenter']
        else:
            return None

    def get_tags(self, *kwargs):
        tags = {}

        ec2 = boto3.resource('ec2', region_name=self.region, config=self.AWS_CONFIG)
        instance = ec2.Instance(self.instance_id)
        for tag in instance.tags:
            if ":" in tag['Key']:
                True
            elif "," in tag['Value']:
                tags[tag['Key']] = tag['Value'].split(",")
            else:
                tags[tag['Key']] = self.autoconvert(tag['Value'])

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
