# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import six

if six.PY3:
    from urllib.parse import (
        urlparse, urlunparse, urljoin, urldefrag,
        urlsplit, urlunsplit, parse_qs,
        parse_qsl, unquote
    )
else:
    from urlparse import (
        urlparse, urlunparse, urljoin, urldefrag,
        urlsplit, urlunsplit, parse_qs,
        parse_qsl, unquote
    )


__all__ = [
    "urlparse", "urlunparse", "urljoin", "urldefrag",
    "urlsplit", "urlunsplit", "parse_qs",
    "parse_qsl", "unquote",
]
