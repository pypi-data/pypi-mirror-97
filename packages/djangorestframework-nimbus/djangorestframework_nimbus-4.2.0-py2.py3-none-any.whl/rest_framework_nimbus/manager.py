# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid
from django.utils.translation import ugettext_lazy as _
from django.db.models.deletion import CASCADE
from django.db import models
from .constants import DELETE_CODE


class BaseManager(models.Manager):
    def get_queryset(self):
        queryset = super(BaseManager, self).get_queryset()
        return queryset.filter(del_flag=DELETE_CODE.NORMAL.code)

    def get_all_queryset(self):
        return super(BaseManager, self).get_queryset()


class APIUserManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})
