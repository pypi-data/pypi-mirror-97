# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from django.templatetags.static import static
from .admintools import ProxyModelAdmin


class BaseAdmin(ProxyModelAdmin):

    class Media:
        js = (static('nimbus/js/filter.js'),)
        css = {
            'all': (static('nimbus/css/filter.css'),),
        }
