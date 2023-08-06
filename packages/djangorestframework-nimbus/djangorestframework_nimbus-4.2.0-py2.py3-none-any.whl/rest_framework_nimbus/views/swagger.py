# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.renderers import BrowsableAPIRenderer, CoreJSONRenderer
from rest_framework.schemas import SchemaGenerator
from rest_framework_swagger import renderers


class DocsSchemaGenerator(SchemaGenerator):

    def has_view_permissions(self, path, method, view):
        return True


def get_schema_view(title=None, url=None, renderer_classes=None):
    """
    Return a schema view.
    """
    generator = DocsSchemaGenerator(title=title, url=url)
    if renderer_classes is None:
        if BrowsableAPIRenderer in api_settings.DEFAULT_RENDERER_CLASSES:
            rclasses = [CoreJSONRenderer, BrowsableAPIRenderer]
        else:
            rclasses = [CoreJSONRenderer]
    else:
        rclasses = renderer_classes

    class SchemaView(APIView):
        authentication_classes = []
        permission_classes = []
        _ignore_model_permissions = True
        exclude_from_schema = True
        renderer_classes = rclasses

        def get(self, request, *args, **kwargs):
            schema = generator.get_schema(request)
            if schema is None:
                raise exceptions.PermissionDenied()
            return Response(schema)

    return SchemaView.as_view()


def get_swagger_view(title=None, url=None):
    """
    Returns schema view which renders Swagger/OpenAPI.
    """

    title = title or getattr(settings, 'SWAGGER_TITLE', None)
    url = url or getattr(settings, 'SWAGGER_URL', None)
    return get_schema_view(
        title=title,
        url=url,
        renderer_classes=[
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]
    )
