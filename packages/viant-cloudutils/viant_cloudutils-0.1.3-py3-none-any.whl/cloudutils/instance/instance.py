#!/usr/bin/env python

import requests
import logging


class Instance:

    @staticmethod
    def get_cloud_provider(**kwargs):
        provider = ""
        if requests.get("http://169.254.169.254/").content.split("\n")[1] == "computeMetadata/":
            provider = "gcp"
        else:
            provider = "aws"
        return provider
