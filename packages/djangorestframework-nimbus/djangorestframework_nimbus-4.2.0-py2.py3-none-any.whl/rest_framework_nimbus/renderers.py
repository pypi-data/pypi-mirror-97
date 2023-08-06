# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
import six
from django.conf import settings
from rest_framework import status
from rest_framework import renderers
from rest_framework.utils import encoders
from .settings import api_settings

logger = logging.getLogger(__name__)


class JSONRenderer(renderers.JSONRenderer):
    """
    Renderer which serializes to JSON.
    """
    pass


class UTF8JSONRenderer(renderers.JSONRenderer):
    """
    Renderer which serializes to JSON, and does not escape
    Unicode characters.
    """
    media_type = 'application/json'
    format = 'json'
    ensure_ascii = False
    charset = "utf-8"


class JSONPRenderer(renderers.JSONRenderer):
    """
    Renderer which serializes to json,
    wrapping the json output in a callback function.
    """

    media_type = 'application/javascript'
    format = 'jsonp'
    callback_parameter = 'callback'
    default_callback = 'callback'
    charset = 'utf-8'

    def get_callback(self, renderer_context):
        """
        Determine the name of the callback to wrap around the json output.
        """
        request = renderer_context.get('request', None)
        params = request and request.query_params or {}
        return params.get(self.callback_parameter, self.default_callback)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders into jsonp, wrapping the json output in a callback function.

        Clients may set the callback function name using a query parameter
        on the URL, for example: ?callback=exampleCallbackName
        """
        renderer_context = renderer_context or {}
        callback = self.get_callback(renderer_context)
        json = super(JSONPRenderer, self).render(data, accepted_media_type,
                                                 renderer_context)
        return callback.encode(self.charset) + b'(' + json + b');'


class APIRenderer(JSONRenderer):
    api_render_enabled = api_settings.API_RENDER_DATA_ENABLED
    api_render_handler = api_settings.API_RENDER_DATA_HANDLER

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if self.api_render_enabled:
            if self.api_render_handler and callable(self.api_render_handler):
                response = self.api_render_handler(data, accepted_media_type, renderer_context=renderer_context)
            else:
                response = self.get_render_data(data, accepted_media_type, renderer_context=renderer_context)
        else:
            response = data
        return super(APIRenderer, self).render(response, accepted_media_type, renderer_context)

    def get_render_data(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "code": status_code,
            "status": "SUCCESS",
            "errorCode": None,
            "detailMessages": None,
            "responseBody": data
        }
        if not str(status_code).startswith('2'):
            response["status"] = "ERROR"
            response["responseBody"] = None
            try:
                err_code, err_detail = self._get_exception_info(ex=data, default_code=status_code)
                response["errorCode"] = err_code
                response["detailMessages"] = err_detail
            except KeyError:
                logger.error(data)
                response["responseBody"] = data
        return response

    def _get_exception_info(self, ex, default_code=status.HTTP_400_BAD_REQUEST):
        logger.error(ex)
        if isinstance(ex, dict):
            err = ex.get("detail", "")
        elif isinstance(ex, six.string_types):
            err = ex
        if isinstance(err, dict):
            err_code = err.get("code", default_code)
        else:
            err_code = getattr(err, "code", default_code)
        if isinstance(err, dict):
            err_detail = err.get("detail", err)
        else:
            err_detail = getattr(err, "detail", err)
        if not err_detail and settings.DEBUG:
            err_detail = str(ex)
        return err_code, err_detail


