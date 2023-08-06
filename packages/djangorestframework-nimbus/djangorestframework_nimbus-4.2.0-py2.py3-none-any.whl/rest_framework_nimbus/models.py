# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid
from django.utils.translation import ugettext_lazy as _
from django.db.models.deletion import CASCADE
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from .constants import DELETE_CODE
from .manager import BaseManager, APIUserManager


class BaseModel(models.Model):
    id = models.BigAutoField('主键ID', primary_key=True, help_text="主键ID")
    del_flag = models.BooleanField('删除状态', choices=DELETE_CODE.get_list(), default=DELETE_CODE.NORMAL.code, null=False,
                                   db_index=True, help_text="是否删除:0-正常；1-已删除")
    create_by = models.CharField('创建者', max_length=128, help_text="创建者")
    update_by = models.CharField('更新者', max_length=128, help_text="更新者")
    create_date = models.DateTimeField('创建时间', auto_now_add=True, db_index=True, editable=False)
    update_date = models.DateTimeField('修改时间', auto_now=True, db_index=True, editable=False)

    objects = BaseManager()

    class Meta:
        abstract = True


class APIUser(models.Model):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = APIUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_username()

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)



