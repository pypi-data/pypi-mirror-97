# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import sys
import logging
import json
from functools import wraps


def filterd(data, includes=None, excludes=[]):
    if includes and excludes:
        return {k: v for (k, v) in data.items() if (k in includes and k not in excludes)}
    elif includes:
        return {k: v for (k, v) in data.items() if (k in includes)}
    elif excludes:
        return {k: v for (k, v) in data.items() if (k not in excludes)}
    else:
        return data

