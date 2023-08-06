# -*- coding: utf-8 -*-
import re
import uuid
from dateutil import parser
from datetime import datetime
import logging
from django.conf import settings
from django.db import models
from django.dispatch import receiver
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
from nimbus_utils.encrypt_rsa import encryptor
from nimbus_utils.encrypt_aes import aescryptor

logger = logging.getLogger(__name__)


def format_exception(status_code, detail, code=None, show_detail=False):
    data = {
        "code": status_code,
        "subcode": code or status_code,
    }
    if settings.DEBUG or show_detail:
        data["msg"] = detail
    return data


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def to_python_boolean(string):
    """Convert a string to boolean.
    """
    string = string.lower()
    if string in ('t', 'true', '1'):
        return True
    if string in ('f', 'false', '0'):
        return False
    raise ValueError("Invalid boolean value: '%s'" % string)


def within_time_range(d1, d2, maxdiff_seconds):
    '''Return true if two datetime.datetime object differs less than the given seconds'''
    delta = d2 - d1 if d2 > d1 else d1 - d2
    # delta.total_seconds() is only available in python 2.7+
    diff = (delta.microseconds + (delta.seconds + delta.days*24*3600) * 1e6) / 1e6
    return diff < maxdiff_seconds


def get_keyword(request, keyword, default=None):
    value = request.GET.get(keyword, default)
    return value or request.POST.get(keyword, default)


def get_header(request, key, default=None):
    key = key.replace("-", "_")
    key = u"HTTP_{}".format(key).upper()
    return request.META.get(key, default)


def get_data(request, key, default=None):
    return request.data.get(key, default)


def to_datetime(timestamp):
    try:
        ts = float(timestamp)
        return datetime.fromtimestamp(ts, timezone.get_current_timezone())
    except Exception as e:
        logger.error(e)
    try:
        return parser.parse(timestamp)
    except Exception as e:
        logger.error(e)
    return None


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


def generate_keys_string(bits=1024, format='PEM', passphrase=None, pkcs=1, base64_key=False):
    return encryptor.generate_keys_string(bits=bits,
                                          format=format,
                                          passphrase=passphrase,
                                          pkcs=pkcs,
                                          base64_key=base64_key)


def encrypt_rsa_big(message, public_key, sep='\n', passphrase=None, cipher_type=1, base64_key=False, base64_data=True):
    return encryptor.encrypt_big(message, public_key=public_key,
                                 sep=sep,
                                 passphrase=passphrase,
                                 cipher_type=cipher_type,
                                 base64_key=base64_key,
                                 base64_data=base64_data)


def decrypt_rsa_big(message, private_key, sep=None, passphrase=None, cipher_type=1, base64_key=False, base64_data=True):
    return encryptor.decrypt_big(message, private_key=private_key,
                                 sep=sep,
                                 passphrase=passphrase,
                                 cipher_type=cipher_type,
                                 base64_key=base64_key,
                                 base64_data=base64_data)


def encrypt_rsa(message, public_key, passphrase=None, cipher_type=1, base64_key=False, base64_data=True):
    return encryptor.encrypt(message, public_key=public_key,
                             passphrase=passphrase,
                             cipher_type=cipher_type,
                             base64_key=base64_key,
                             base64_data=base64_data)


def decrypt_rsa(message, private_key, passphrase=None, cipher_type=1, base64_key=False, base64_data=True):
    return encryptor.decrypt(message, private_key=private_key,
                             passphrase=passphrase,
                             cipher_type=cipher_type,
                             base64_key=base64_key,
                             base64_data=base64_data)


def sign(message, private_key, passphrase=None, signature_type=1, base64_key=False, base64_signature=True):
    return encryptor.sign(message, private_key=private_key,
                          passphrase=passphrase,
                          signature_type=signature_type,
                          base64_key=base64_key,
                          base64_signature=base64_signature)


def verify(message, signature, public_key, passphrase=None, signature_type=1, base64_key=False, base64_signature=True):
    return encryptor.verify(message, signature, public_key=public_key,
                            passphrase=passphrase,
                            signature_type=signature_type,
                            base64_key=base64_key,
                            base64_signature=base64_signature)


def encrypt_aes(data, password):
    return aescryptor.encrypt(data=data, password=password)


def decrypt_aes(data, password):
    return aescryptor.decrypt(data=data, password=password)

