# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from enum import Enum
from enum import unique
from .code import Code

# @unique
# class Color(Enum):
#     RED = 1
#     GREEN = 2
#     BLUE = 3

DELETE_CODE = Code((
    ('NORMAL',  0, '正常'),
    ('DELETED', 1, '已经删除'),
))
