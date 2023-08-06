# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator as DjangoPaginator
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import remove_query_param, replace_query_param
from ..settings import api_settings


class APIPaginator(DjangoPaginator):
    allow_empty = getattr(api_settings, "API_ALLOW_EMPTY", True)

    def validate_number(self, number):
        """
        Validates the given 1-based page number.
        """
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            elif self.allow_empty:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return number


class BaseAPIPageNumberPagination(PageNumberPagination):
    django_paginator_class = APIPaginator

    # Client can control the page using this query parameter.
    page_query_param = api_settings.PAGE_QUERY_PARAM

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = api_settings.PAGE_SIZE_QUERY_PARAM

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = api_settings.MAX_PAGE_SIZE

    #display_page_controls = True

    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'count': self.page.paginator.count,
                # 'next': self.get_next_link(),
                # 'previous': self.get_previous_link(),
                # 'html': self.to_html(),
                # 'context': self.get_html_context(),
                'version': self.request.version,
            },
            'results': data
        })

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        # if page_number == 1:
        #     return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)
