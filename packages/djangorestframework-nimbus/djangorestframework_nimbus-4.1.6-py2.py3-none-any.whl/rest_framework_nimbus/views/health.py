# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.http import HttpResponse, JsonResponse
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView
from rest_framework.views import APIView
from rest_framework import status


class HealthCheckerView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("ok", status=status.HTTP_200_OK)
