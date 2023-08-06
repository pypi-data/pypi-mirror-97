# -*- coding:utf-8 -*-
from django.conf import settings
from django.conf.urls import url, include

from .views.swagger import get_swagger_view

urlpatterns = [
    url(r'^$', get_swagger_view()),
]
