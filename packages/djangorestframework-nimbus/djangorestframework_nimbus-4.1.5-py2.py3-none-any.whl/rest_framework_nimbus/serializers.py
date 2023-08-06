# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import uuid
import six
import base64
import logging
import collections
from collections import Mapping, OrderedDict
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import MiddlewareNotUsed, PermissionDenied, SuspiciousOperation
from django.conf import settings
from django.utils import timezone
from django.contrib import auth
from django.shortcuts import render
from django.dispatch import receiver
from django.db.models import F, Q
from django.db.models import Count, Avg, Sum, Aggregate
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import resolve_url
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware, make_naive, is_aware, is_naive, now, utc
from django.utils.encoding import smart_str, smart_text
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions, status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.fields import get_error_detail, set_value, empty
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.utils import formatting
from rest_framework import serializers, viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, GenericViewSet, ReadOnlyModelViewSet, ModelViewSet, ViewSetMixin

from . import utils

logger = logging.getLogger(__name__)


class DateTimeFieldWihTZ(serializers.DateTimeField):
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)


class SizeFormatField(serializers.FloatField):
    raw = False
    suffix = 'B'

    def __init__(self, raw=False, suffix='B', **kwargs):
        self.suffix = suffix
        self.raw = raw
        super(SizeFormatField, self).__init__(**kwargs)

    def to_representation(self, value):
        v = super(SizeFormatField, self).to_representation(value)
        if self.raw:
            return "%.1f%s" % (v, self.suffix)
        return utils.sizeof_fmt(v, suffix=self.suffix)


class Base64Field(serializers.CharField):
    default_error_messages = {
        'invalid': _('Not a valid string.'),
        'blank': _('This field may not be blank.'),
        'max_length': _('Ensure this field has no more than {max_length} characters.'),
        'min_length': _('Ensure this field has at least {min_length} characters.'),
        'base64': _('Not a valid base64 string.')
    }

    def __init__(self, **kwargs):
        super(Base64Field, self).__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            data = base64.standard_b64decode(data)
            return super(Base64Field, self).to_internal_value(data)
        except Exception as e:
            logger.error(u"base64 decode: {}".format(e))
            self.fail('base64', input=data)

    def to_representation(self, value):
        try:
            value = super(Base64Field, self).to_representation(value)
            return base64.standard_b64encode(value)
        except Exception as e:
            logger.error(u"base64 encode: {}".format(e))
            return None


class Base64MethodField(serializers.SerializerMethodField):
    methd_filed = None
    default_error_messages = {
        'required': _('This field is required.'),
        'null': _('This field may not be null.'),
        'base64': _('Not a valid base64 string.')
    }

    def to_internal_value(self, data):
        try:
            data = base64.standard_b64decode(data)
            return super(Base64MethodField, self).to_internal_value(data)
        except Exception as e:
            logger.error(u"base64 decode: {}".format(e))
            self.fail('base64', input=data)

    def to_representation(self, value):
        try:
            value = super(Base64MethodField, self).to_representation(value)
            return base64.standard_b64encode(value)
        except Exception as e:
            logger.error(u"base64 encode: {}".format(e))
            return None


class RSABase64Field(serializers.CharField):
    base64_key = False
    base64_data = True
    cipher_type = 1
    default_error_messages = {
        'invalid': _('Not a valid string.'),
        'blank': _('This field may not be blank.'),
        'max_length': _('Ensure this field has no more than {max_length} characters.'),
        'min_length': _('Ensure this field has at least {min_length} characters.'),
        'base64': _('Not a valid base64 string.'),
        'encrypt': _('Not a valid data.'),
        'decrypt': _('Not a valid data.'),
        'signature': _('Not a valid data.'),
        'verify': _('Not a valid data.'),
    }

    def __init__(self, base64_key=False, base64_data=True, cipher_type=1, **kwargs):
        self.base64_key = base64_key
        self.base64_data = base64_data
        self.cipher_type = cipher_type
        super(RSABase64Field, self).__init__(**kwargs)

    def get_decrypt_key(self):
        raise NotImplementedError(".get_decrypt_key() must be overridden.")

    def get_encrypt_key(self):
        raise NotImplementedError(".get_encrypt_key() must be overridden.")

    def get_passphrase(self):
        return None

    def decrypt_rsa(self, data):
        return utils.decrypt_rsa(data, self.get_decrypt_key(),
                                 passphrase=self.get_passphrase(),
                                 cipher_type=self.cipher_type,
                                 base64_key=self.base64_key,
                                 base64_data=self.base64_data,)

    def encrypt_rsa(self, value):
        return utils.encrypt_rsa(value, self.get_encrypt_key(),
                                 passphrase=self.get_passphrase(),
                                 cipher_type=self.cipher_type,
                                 base64_key=self.base64_key,
                                 base64_data=self.base64_data,)

    def to_internal_value(self, data):
        try:
            data = self.decrypt_rsa(data)
            return super(RSABase64Field, self).to_internal_value(data)
        except Exception as e:
            logger.error(u"rsa decrypt: {}".format(e))
            self.fail('decrypt', input=data)

    def to_representation(self, value):
        try:
            value = super(RSABase64Field, self).to_representation(value)
            value = smart_str(value)
            return self.encrypt_rsa(value)
        except Exception as e:
            logger.error(u"rsa encrypt: {}".format(e))
            return None


class RSABase64MethodField(serializers.SerializerMethodField):
    base64_key = False
    base64_data = True
    cipher_type = 1
    default_error_messages = {
        'required': _('This field is required.'),
        'null': _('This field may not be null.'),
        'base64': _('Not a valid base64 string.'),
        'encrypt': _('Not a valid data.'),
        'decrypt': _('Not a valid data.'),
        'signature': _('Not a valid data.'),
        'verify': _('Not a valid data.'),
    }

    def __init__(self, base64_key=False, base64_data=True, cipher_type=1, method_name=None, **kwargs):
        self.base64_key = base64_key
        self.base64_data = base64_data
        self.cipher_type = cipher_type
        super(RSABase64MethodField, self).__init__(method_name, **kwargs)

    def get_decrypt_key(self):
        raise NotImplementedError(".get_decrypt_key() must be overridden.")

    def get_encrypt_key(self):
        raise NotImplementedError(".get_encrypt_key() must be overridden.")

    def get_passphrase(self):
        return None

    def decrypt_rsa(self, data):
        return utils.decrypt_rsa(data, self.get_decrypt_key(),
                                 passphrase=self.get_passphrase(),
                                 cipher_type=self.cipher_type,
                                 base64_key=self.base64_key,
                                 base64_data=self.base64_data,)

    def encrypt_rsa(self, value):
        return utils.encrypt_rsa(value, self.get_encrypt_key(),
                                 passphrase=self.get_passphrase(),
                                 cipher_type=self.cipher_type,
                                 base64_key=self.base64_key,
                                 base64_data=self.base64_data,)

    def to_internal_value(self, data):
        try:
            data = self.decrypt_rsa(data)
            return super(RSABase64MethodField, self).to_internal_value(data)
        except Exception as e:
            logger.error(u"rsa decrypt: {}".format(e))
            self.fail('decrypt', input=data)

    def to_representation(self, value):
        try:
            value = super(RSABase64MethodField, self).to_representation(value)
            value = smart_str(value)
            return self.encrypt_rsa(value)
        except Exception as e:
            logger.error(u"rsa encrypt: {}".format(e))
            return None

