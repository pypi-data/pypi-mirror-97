# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def jwt_response_payload_handler(token, user=None, request=None, role=None, **kwargs):
    """
    自定义jwt认证成功返回数据
    :param token: 返回的jwt
    :param user: 当前登录的用户信息[对象]
    :param request: 当前本次客户端提交过来的数据
    :param role: 角色
    :return:
    """
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    if user.first_name:
        name = user.first_name
    else:
        name = user.username
    return {
        # "authenticated": 'true',
        # 'id': user.id,
        # "role": role,
        # 'name': name,
        'username': user.username,
        # 'email': user.email,
        'token': token,
    }


def jwt_get_secret_key(user_model):
    return user_model.jwt_secret

