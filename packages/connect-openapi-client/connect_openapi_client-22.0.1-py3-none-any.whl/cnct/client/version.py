# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect connect-fluent-client.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import pkg_resources


try:
    __version__ = pkg_resources.require('connect-openapi-client')[0].version
except:  # noqa: E722
    __version__ = '0.0.1'


def get_version():
    return __version__
