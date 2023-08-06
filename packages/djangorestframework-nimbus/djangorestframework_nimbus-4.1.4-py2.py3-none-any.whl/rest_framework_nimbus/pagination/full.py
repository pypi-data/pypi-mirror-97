# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param
from ..settings import api_settings
from .base import BaseAPIPageNumberPagination


class APIPageNumberPagination(BaseAPIPageNumberPagination):
    api_name_total_data = api_settings.API_PAGE_NAME_TOTAL_DATA
    api_name_total_page = api_settings.API_PAGE_NAME_TOTAL_PAGE
    api_name_page = api_settings.API_PAGE_NAME_PAGE
    api_name_page_size = api_settings.API_PAGE_NAME_PAGE_SIZE
    api_name_data = api_settings.API_PAGE_NAME_DATA

    def get_paginated_response(self, data):
        total_data = self.page.paginator.count
        page_size = self.page.paginator.per_page
        page = self.page.number
        # page_size = self.request.params.page_size
        total_page = (total_data + page_size - 1) // page_size
        res = {
            self.api_name_page_size: page_size,
            self.api_name_data: data,
            self.api_name_page: page,
            self.api_name_total_page: total_page,
            self.api_name_total_data: total_data
        }
        return Response(res)

