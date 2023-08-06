# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from .code import Code, CodeData

__all__ = ["ErrCode", "APIError", "CodeData"]

CodeDefine = (
    ('SUCCESS', '00000000', '返回成功'),
    ('ERR_UNKOWN', '00000001', '未知错误'),
    ('ERR_SYS_ERROR', '00000002', '服务异常'),

    ('ERR_JWT_EMPTY', '10000001', '没有找到JWT信息'),
    ('ERR_JWT_EXPIRED', '10000002', '签名过期'),
    ('ERR_JWT_DECODE', '10000003', 'JWT解码错误'),
    ('ERR_JWT_INVALID', '10000004', 'JWT不合法'),

    ('ERR_COMMON_BAD_PARAM', '90000001', '参数错误'),
    ('ERR_COMMON_BAD_FORMAT', '90000002', '格式错误'),
    ('ERR_COMMON_PERMISSION', '90000003', '权限错误'),
    ('ERR_COMMON_NOT_FOUND', '90000004', '未找到'),
)

ErrCode = Code(CodeDefine + getattr(settings, "API_ERROR_CODES", ()))


class APIError(ValueError):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, errcode=ErrCode.ERR_UNKOWN, status_code=status.HTTP_400_BAD_REQUEST, **kwargs):
        self.code = errcode
        self.kwargs = kwargs
        self.status_code = status_code
        message = self.kwargs.get('message', errcode.message)
        super(APIError, self).__init__(message)

    def get_res_dict(self):
        return self.code.get_res_dict(**self.kwargs)
