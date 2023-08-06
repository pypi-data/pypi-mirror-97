# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import logging
import json
from functools import wraps
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException as RESTAPIException
from rest_framework import status


class APIException(RESTAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_code = 'error'

    def __init__(self, detail=None, code=None):
        self.detail = detail or self.default_detail
        self.code = code or self.code


class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Incorrect authentication credentials.'

    def __init__(self, detail=None, code=None):
        super(AuthenticationFailed, self).__init__(detail, code)


