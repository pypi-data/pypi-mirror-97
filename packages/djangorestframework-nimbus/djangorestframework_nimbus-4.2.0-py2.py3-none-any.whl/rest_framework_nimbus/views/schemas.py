# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
from rest_framework.compat import coreapi
from rest_framework.permissions import AllowAny
from django_rest_swagger_docstring.schemas import DocsSchemaGenerator as _DocsSchemaGenerator
from django_rest_swagger_docstring.parsers import YAMLDocstringParser


def insert_into(target, keys, value):
    """
    Nested dictionary insertion.
    """
    for key in keys[:-1]:
        if key not in target:
            target[key] = OrderedDict()
        target = target[key]
    target[keys[-1]] = value


def sort_key(x):
    path, method, view = x
    doc_order = getattr(view, "_doc_order", 1)
    return doc_order


class DocsSchemaGenerator(_DocsSchemaGenerator):

    def has_view_permissions(self, path, method, view):
        return True

    # def get_link(self, path, method, view):
    #     """ Return a `coreapi.Link` instance for the given endpoint. """
    #     fields = []
    #     try:
    #         fields = self.get_path_fields(path, method, view)
    #     except:
    #         pass
    #     try:
    #         fields += self.get_serializer_fields(path, method, view)
    #     except:
    #         pass
    #     try:
    #         fields += self.get_pagination_fields(path, method, view)
    #     except:
    #         pass
    #     try:
    #         fields += self.get_filter_fields(path, method, view)
    #     except:
    #         pass
    #     try:
    #         fields += self.get_docs_fields(path, method, view)
    #     except:
    #         pass
    #
    #     if fields and any([field.location in ('form', 'body') for field in fields]):
    #         encoding = self.get_encoding(path, method, view)
    #     else:
    #         encoding = None
    #
    #     description = self.get_description(path, method, view)
    #     permisions = self.get_permissions_docs(path, method, view)
    #     if permisions is not None:
    #         description = u'{}\nPermisions:\n========\n{}'.format(description, permisions)
    #
    #     if self.url and path.startswith('/'):
    #         path = path[1:]
    #
    #     return coreapi.Link(
    #         url=urlparse.urljoin(self.url, path),
    #         action=method.lower(),
    #         encoding=encoding,
    #         fields=fields,
    #         description=description
    #     )

    def get_docs_fields(self, path, method, view):
        """ Return a `coreapi.Fields array` instance from docstrings """
        method_name = getattr(view, 'action', method.lower())
        method_docstring = getattr(view, method_name, None).__doc__
        docs = str(method_docstring)
        if method_docstring is None:
            docs = view.get_view_description()
        yaml_parser = YAMLDocstringParser(docs)
        parameters = yaml_parser.get_parameters()
        coreapi_fields = []
        for parameter in parameters:
            coreapi_fields.append(coreapi.Field(name=parameter.get('name'),
                                                required=parameter.get('required'),
                                                location=parameter.get('param_type'),
                                                type=parameter.get('data_type')))
        return coreapi_fields

    def get_permissions_docs(self, path, method, view):
        permissions = view.get_permissions()
        permissions_docs = u''
        for permission in permissions:
            if isinstance(permission, AllowAny):
                continue
            if permission.__class__.__doc__ is not None:
                permissions_docs = u'{}- {} - {}\n'.format(permissions_docs, permission.__class__.__name__,
                                                           permission.__class__.__doc__)
            else:
                permissions_docs = u'{}- {}\n'.format(permissions_docs, permission.__class__.__name__)
        if len(permissions_docs) > 0:
            return permissions_docs
        return None

