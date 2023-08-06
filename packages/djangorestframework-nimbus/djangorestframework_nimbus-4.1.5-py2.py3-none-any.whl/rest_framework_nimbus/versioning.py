# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import logging
from rest_framework import exceptions
from rest_framework.compat import unicode_http_header
from rest_framework.reverse import _reverse
from rest_framework.settings import api_settings
from rest_framework.templatetags.rest_framework import replace_query_param
from rest_framework.utils.mediatypes import _MediaType
from django.utils.translation import ugettext_lazy as _
from rest_framework.versioning import BaseVersioning

logger = logging.getLogger(__name__)


class HeaderVersioning(BaseVersioning):
    """
    GET /something/ HTTP/1.1
    Host: example.com
    version: v1
    """
    invalid_version_message = _('Invalid version in header.')

    def determine_version(self, request, *args, **kwargs):
        version = self.get_version(request)
        if not self.is_allowed_version(version):
            raise exceptions.NotAcceptable(self.invalid_version_message)
        return version

    def get_version(self, request):
        v = request.META.get("HTTP_{}".format(self.version_param).upper(), None)
        return v or self.default_version
