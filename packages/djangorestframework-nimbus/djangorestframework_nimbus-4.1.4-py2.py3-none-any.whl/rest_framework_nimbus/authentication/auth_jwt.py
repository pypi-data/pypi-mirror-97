# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication as JWTAuthentication
from ..err_code import ErrCode, APIError


class JSONWebTokenAuthentication(JWTAuthentication):
    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if not jwt_value:
            raise APIError(ErrCode.ERR_JWT_EMPTY, status_code=401)
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise APIError(ErrCode.ERR_JWT_EXPIRED, status_code=401)
        except jwt.DecodeError:
            raise APIError(ErrCode.ERR_JWT_DECODE, status_code=401)
        except jwt.InvalidTokenError:
            raise APIError(ErrCode.ERR_JWT_INVALID, status_code=401)
        try:
            user = self.authenticate_credentials(payload)
        except AuthenticationFailed as e:
            raise APIError(ErrCode.ERR_JWT_INVALID, status_code=401, detail=e.detail)
        return user, jwt_value

