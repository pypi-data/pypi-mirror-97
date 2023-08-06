# -*- coding: utf-8 -*-
from __future__ import absolute_import

"""
Package Description
"""
import os
import sys
import logging
import json
from functools import wraps
from django.conf import settings
from django.test.signals import setting_changed
from rest_framework.settings import perform_import


DEFAULTS = {
    'DEBUG': False,
    'API_ALLOW_EMPTY': True,

    # 公钥私钥
    'API_PRIVATE_KEY': "",
    'API_SECRECT_KEY': "",

    # 错误捕捉
    'API_CATCH_EXCEPTION_ENABLED': True,
    'API_CATCH_EXCEPTION_HANDLER': None,

    # API 格式
    'API_RENDER_DATA_ENABLED': True,
    'API_RENDER_DATA_HANDLER': None,

    # 分页参数
    'PAGE_QUERY_PARAM': 'page',
    'PAGE_SIZE_QUERY_PARAM': 'page_size',
    'MAX_PAGE_SIZE': 100,

    # 分页返回参数
    'API_PAGE_NAME_TOTAL_DATA': "total",
    'API_PAGE_NAME_TOTAL_PAGE': "total_page",
    'API_PAGE_NAME_PAGE': "page",
    'API_PAGE_NAME_PAGE_SIZE': "page_size",
    'API_PAGE_NAME_DATA': "data",

    # API用户模型
    'API_USER_MODEL': None,
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = [
    'API_CATCH_EXCEPTION_HANDLER',
    'API_RENDER_DATA_HANDLER',
    'API_USER_MODEL',
]


class APISettings(object):
    def __init__(self, defaults=None, import_strings=None):
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'API_CONFIG', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


api_settings = APISettings(DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'API_CONFIG':
        api_settings.reload()


setting_changed.connect(reload_api_settings)
