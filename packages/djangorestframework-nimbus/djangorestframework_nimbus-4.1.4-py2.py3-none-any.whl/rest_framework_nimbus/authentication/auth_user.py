# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import jwt
from ..settings import api_settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import jwt_decode_handler, jwt_get_username_from_payload
from .auth_jwt import JSONWebTokenAuthentication as JWTAuthentication
from ..err_code import ErrCode, APIError


class ExtraJSONWebTokenAuthentication(JWTAuthentication):
    user_model = api_settings.API_USER_MODEL

    def get_model(self):
        if self.user_model is not None:
            return self.user_model
        return get_user_model()

    def authenticate_credentials(self, payload):
        username = jwt_get_username_from_payload(payload)
        if not username:
            msg = _('Invalid payload.')
            raise AuthenticationFailed(msg)
        User = self.get_model()
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise AuthenticationFailed(msg)
        if not user.is_active:
            msg = _('User account is disabled.')
            raise AuthenticationFailed(msg)
        return user

