# -*- coding: utf-8 -*-
import os
import re
import uuid
import logging
import hmac
import datetime
import collections
from io import BytesIO
from hashlib import sha1
import django
from django.conf import settings
from django.db import models
from django.db.models import F, Q
from django.db.models import Count, Avg, Sum, Aggregate
from django.dispatch import receiver
from django.db.models import signals
from django.db.models.signals import post_save, post_delete
from django.db.models.signals import class_prepared
from django.forms.models import model_to_dict, fields_for_model, ALL_FIELDS
from django.db.models.fields.files import FieldFile, FileField, ImageField, ImageFieldFile, FileDescriptor
from django.core import validators
from django.utils import timezone
from django.utils import dateformat
from django.utils.timezone import make_aware, make_naive, is_aware, is_naive, now, utc
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.core.validators import URLValidator, ValidationError
from django.urls import reverse

from . import utils


class EncryptedFile(BytesIO):
    def __init__(self, content, password):
        self.size = content.size
        super(EncryptedFile, self).__init__(utils.encrypt_aes(content.file.read(), password))


class EncryptedFileDescriptor(FileDescriptor):
    def __set__(self, instance, value):
        super(EncryptedFileDescriptor, self).__set__(instance, value)


class EncryptedFieldFile(FieldFile):
    crypt_key = None
    crypt_id = None
    crypt_enable = None
    url_name_key = "decrypt_key_url"
    url_name_file = "decrypt_file_url"

    def __init__(self, instance, field, name):
        super(EncryptedFieldFile, self).__init__(instance, field, name)
        self.init_fields()

    def init_fields(self):
        if isinstance(self.field, EncryptedFileField):
            self.crypt_key = getattr(self.instance, self.field.crypt_key_field, None)
            self.crypt_id = getattr(self.instance, self.field.crypt_id_field, None)
            self.crypt_enable = getattr(self.instance, self.field.crypt_enable_field, None)
            self.url_name_key = self.field.url_name_key or self.url_name_key
            self.url_name_file = self.field.url_name_file or self.url_name_file

    def save(self, name, content, save=True):
        if content and self.crypt_key and self.crypt_enable:
            content = EncryptedFile(content, password=self.crypt_key)
        return super(EncryptedFieldFile, self).save(name, content, save=save)
    save.alters_data = True

    @property
    def url(self):
        return super(EncryptedFieldFile, self).url()

    @property
    def decrypt_url(self):
        if self.crypt_id:
            return reverse(self.url_name_file, kwargs={"crypt_id": self.crypt_id})
        else:
            return u""

    @property
    def decrypt_key_url(self):
        if self.crypt_id:
            return reverse(self.url_name_key, kwargs={"crypt_id": self.crypt_id})
        else:
            return u""


class EncryptedFileField(FileField):
    attr_class = EncryptedFieldFile
    descriptor_class = EncryptedFileDescriptor
    crypt_key_field = None
    crypt_id_field = None
    crypt_enable_field = None
    url_name_key = None
    url_name_file = None

    def __init__(self, verbose_name=None, name=None,
                 crypt_key_field=None, crypt_id_field=None,
                 crypt_enable_field=None,
                 url_name_key=None, url_name_file=None,
                 **kwargs):
        self.crypt_key_field = crypt_key_field
        self.crypt_id_field = crypt_id_field
        self.crypt_enable_field = crypt_enable_field
        self.url_name_key = url_name_key
        self.url_name_file = url_name_file
        super(EncryptedFileField, self).__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(EncryptedFileField, self).deconstruct()
        if self.crypt_key_field:
            kwargs['crypt_key_field'] = self.crypt_key_field
        if self.crypt_id_field:
            kwargs['crypt_id_field'] = self.crypt_id_field
        if self.crypt_enable_field:
            kwargs['crypt_enable_field'] = self.crypt_enable_field
        if self.url_name_key:
            kwargs['url_name_key'] = self.url_name_key
        if self.url_name_file:
            kwargs['url_name_file'] = self.url_name_file
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super(EncryptedFileField, self).contribute_to_class(cls, name, **kwargs)


