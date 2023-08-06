# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import re
import uuid
from dateutil import parser
from datetime import datetime
import logging
import hashlib
from .encrypt import encryptor
from .encrypt import aescryptor
from .encoding import smart_bytes, smart_str

logger = logging.getLogger(__name__)


def md5(data=""):
    data = smart_bytes(data)
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


def generate_uid():
    return uuid.uuid4().hex


def str2bool(v=None):
    if v is None:
        return False
    elif isinstance(v, bool):
        return v
    return v.lower() in ("yes", "true", "t", "1")


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


def to_bytes(s):
    if isinstance(s, bytes):
        return s
    if isinstance(s, str):
        return s.encode('utf-8')


def to_str(s):
    if isinstance(s, bytes):
        return s.decode('utf-8')
    if isinstance(s, str):
        return s
