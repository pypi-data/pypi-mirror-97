# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import base64
import string
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography import exceptions
from cryptography import fernet
from nimbus_utils.encoding import smart_str, smart_bytes
from nimbus_utils.crypto import get_random_string

__all__ = ["fernetcryptor", "FernetCryptoGrapher"]

logger = logging.getLogger("encrypt")


class FernetCryptoGrapher(object):
    """
    Fernet 加密解密
    """
    random_strings = string.ascii_letters + string.digits

    def __init__(self, salt="1234567890"):
        self.salt = salt

    @classmethod
    def generate_salt(cls, size=16):
        return get_random_string(size, cls.random_strings)

    def _get_fernet(self, password):
        return Fernet(base64.urlsafe_b64encode(PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=smart_bytes(self.salt),
            iterations=100000,
            backend=default_backend()
        ).derive(smart_bytes(password))))

    def encrypt(self, data, password):
        try:
            data = smart_bytes(data)
            _en_data = self._get_fernet(password=password).encrypt(data)
            endata = smart_str(base64.urlsafe_b64encode(_en_data))
        except Exception as e:
            logger.error(e)
            endata = ""
        return endata

    def decrypt(self, data, password):
        try:
            data = base64.urlsafe_b64decode(smart_bytes(data))
            _de_data = self._get_fernet(password=password).decrypt(data)
            dedata = smart_str(_de_data)
        except exceptions.InvalidSignature as e:
            logger.error(e)
            dedata = ""
        except fernet.InvalidToken as e:
            logger.error(e)
            dedata = ""
        return dedata


fernetcryptor = FernetCryptoGrapher()


if __name__ == '__main__':
    key = "WyfFvacE0fWyb1A277vgo2UIIMvTs8mX"
    print(key)
    data = "0990e3dac6448c6c583bd74992cc8a42"
    encrypt_text = fernetcryptor.encrypt(data, key)
    print('encrypt_text:', encrypt_text)
    decrypt_text = fernetcryptor.decrypt(encrypt_text, key)
    print('decrypt_text:', decrypt_text)


