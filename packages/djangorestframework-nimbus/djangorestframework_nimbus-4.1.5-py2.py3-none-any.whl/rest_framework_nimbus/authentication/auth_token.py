# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import base64
import binascii
import hashlib
import urllib
import logging

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from django.utils.timezone import datetime, timedelta, now, is_aware, is_naive
from django.http import QueryDict
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import BaseAuthentication, SessionAuthentication as RestSessionAuthentication

from .. import utils
from ..exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


class SessionAuthentication(RestSessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class TokenSignAuthentication(BaseAuthentication):
    expiry_minutes = 5
    auth_params = [
        "token", "username", "platform", "deviceid", "timestamp", "sign",
    ]
    sign_params = [
        "method", "scheme", "uri", "username", "platform", "deviceid", "token", "timestamp", "version",
    ]
    sign_prefix = u"SDCP"
    token_param = "token"
    sign_param = "sign"
    timestamp_param = "timestamp"

    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    def authenticate(self, request):
        token = utils.get_header(request, self.token_param, "")
        kwargs = {key: utils.get_header(request, key, "") for key in self.auth_params}
        kwargs[self.token_param] = token
        version = request.version
        func = getattr(self, "authenticate_{}".format(version), None)
        if func and callable(func):
            return func(request=request, version=version, **kwargs)
        raise AuthenticationFailed(_('Authentication Failed'))

    def authenticate_token(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return: (user, token, key) tuple
        """
        raise NotImplementedError(".authenticate_token() must be overridden.")

    def authenticate_sign(self, request, key="", **kwargs):
        sign = kwargs.get(self.sign_param, None)
        if not (sign and key):
            raise AuthenticationFailed(_('Invalid sign.'))
        method = request.method
        scheme = request.scheme
        uri = request.path
        # absolute_uri = request.build_absolute_uri()
        kwargs[self.token_param] = key
        newsign = self.get_sign(request, method=method.lower(), scheme=scheme, uri=uri, path=uri, **kwargs)
        if not newsign or newsign != sign:
            raise AuthenticationFailed(_('Invalid sign.'))

    def authenticate_timestamp(self, **kwargs):
        timestamp = kwargs.get(self.timestamp_param, None)
        if not timestamp:
            raise AuthenticationFailed(_('Invalid timestamp.'))
        dt = utils.to_datetime(timestamp)
        if not dt:
            raise AuthenticationFailed(_('Invalid timestamp.'))
        n = now()
        delta = n - dt if n > dt else dt - n
        if delta > timedelta(minutes=self.expiry_minutes):
            raise AuthenticationFailed(_('Invalid timestamp.'))

    def authenticate_v0(self, request, **kwargs):
        key = kwargs.get(self.token_param, "")
        if not key:
            raise AuthenticationFailed(_('Invalid token.'))
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token.'))
        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))
        return (token.user, token)

    def authenticate_v1(self, request, **kwargs):
        user, token, key = self.authenticate_token(request, **kwargs)
        return (user, token)

    def authenticate_v2(self, request, **kwargs):
        user, token, key = self.authenticate_token(request, **kwargs)
        self.authenticate_sign(request, key=key, **kwargs)
        return (user, token)

    def authenticate_v3(self, request, **kwargs):
        user, token, key = self.authenticate_token(request, **kwargs)
        self.authenticate_sign(request, key=key, **kwargs)
        self.authenticate_timestamp(**kwargs)
        return (user, token)

    def get_sign(self, request, **kwargs):
        unsign_value = u"|".join([u"{}".format(kwargs.get(p, "")) for p in self.sign_params])
        unsign = u"{}|{}".format(self.sign_prefix, unsign_value)
        return hashlib.md5(unsign).hexdigest()

    def decrypt_rsa(self, endata, key, cipher_type=1, base64_key=False, base64_data=True, **kwargs):
        return utils.decrypt_rsa(endata, private_key=key,
                                 cipher_type=cipher_type,
                                 base64_key=base64_key,
                                 base64_data=base64_data,
                                 **kwargs)

    def encrypt_rsa(self, data, key, cipher_type=1, base64_key=False, base64_data=True, **kwargs):
        return utils.encrypt_rsa(data, public_key=key,
                                 cipher_type=cipher_type,
                                 base64_key=base64_key,
                                 base64_data=base64_data,
                                 **kwargs)
