# -*- coding: utf-8 -*-
import re
import uuid
import logging
import collections
import operator
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models import F, Q
from django.db.models import Count, Avg, Sum, Aggregate
from django.db.models.signals import post_save, post_delete
from django.db.models.signals import class_prepared
from django.forms.models import model_to_dict, fields_for_model, ALL_FIELDS
from django.shortcuts import resolve_url
from django.core import validators
from django.utils import timezone
from django.utils import dateformat
from django.utils.timezone import make_aware, make_naive, is_aware, is_naive, now, utc
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import filters

logger = logging.getLogger(__name__)


class UserFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user and request.user.is_authenticated:
            return queryset.filter(user=request.user)
        else:
            return queryset.none()


class UsersFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user and request.user.is_authenticated:
            return queryset.filter(users=request.user)
        else:
            return queryset.none()


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user and request.user.is_authenticated:
            return queryset.filter(owner=request.user)
        else:
            return queryset.none()

