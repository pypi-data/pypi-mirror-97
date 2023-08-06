# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import date

__all__ = [
    "__title__",
    "__version__",
    "__description__",
    "__keywords__",
    "__author__",
    "__author_email__",
    "__url__",
    "__platforms__",
    "__license__",
    "__classifiers__",
    "__install_requires__",
    "__zip_safe__",
    "__copyright__",
]

__title__ = "djangorestframework-nimbus"
__version__ = '4.2.0'
__description__ = "djangorestframework-nimbus"
__keywords__ = ["rest_framework_nimbus", "nimbus", "django", "api"]
__author__ = "william"
__author_email__ = "william.ren@live.cn"
__maintainer__ = "william"
__maintainer_email__ = "william.ren@live.cn"
__url__ = "https://github.com/williamren"
__platforms__ = "Any"
__license__ = "Apache License 2.0"
__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Internet :: WWW/HTTP",
    "Environment :: Web Environment",
    "Framework :: Django",
    "Framework :: Django :: 1.10",
    "Framework :: Django :: 1.11",
    "Framework :: Django :: 2.0",
    "Framework :: Django :: 3.0",
]
__install_requires__ = [
    "Django",
    "djangorestframework",
    "djangorestframework-jwt",
    "pycrypto",
    "rncryptor",
    "python-dateutil",
    "coreapi",
    "nimbus_utils",
]
__zip_safe__ = False
__copyright__ = "Copyright 2001-{0} {1}".format(date.today().year, __author__)

