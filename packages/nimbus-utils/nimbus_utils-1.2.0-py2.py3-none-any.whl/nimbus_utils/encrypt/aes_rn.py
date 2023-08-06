# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import base64
import rncryptor
import logging
from nimbus_utils.encoding import smart_str

__all__ = ["aescryptor", "rncryptor", "RNCryptor"]

logger = logging.getLogger("encrypt")


class RNCryptor(rncryptor.RNCryptor):
    """
    加密解密
    MODE: CBC
    PADDING: PKCS#7
    SALT: 8
    """
    def encrypt(self, data, password):
        try:
            endata = super(RNCryptor, self).encrypt(data=data, password=password)
        except rncryptor.RNCryptorError as e:
            logger.error(e)
            endata = ""
        return endata

    def decrypt(self, data, password):
        try:
            dedata = super(RNCryptor, self).decrypt(data=data, password=password)
        except rncryptor.DecryptionError as e:
            logger.error(e)
            dedata = ""
        return dedata


aescryptor = RNCryptor()


if __name__ == '__main__':
    raw_key = "e070903a51a43d3ebd7abf1993ae6f4cc65f50c8"
    resource_key = "8a3dffd927abfa15e95c88a26ec3b64f8994ef9f"
    base64_data = "AwHC6zn3e-1NsGBNMXF1tlh76MUKcQs7oZTBpsacdVyZ5KsM7DfckV3PRh48gg-MwWpPa0Q4l_liZB0Wz6p33hN7lZTeV8OdfjyppAhxN7ND7F4FTkyC_Z6IdtBrfHHFLS_56HTUTtblTYTV58RwDF_4"

    print("raw_key   :", raw_key)
    print("encrypt_data:", base64_data)
    base64_data = smart_str(base64_data)
    encrypt_data = base64.urlsafe_b64decode(base64_data)
    crypt_key = aescryptor.decrypt(data=encrypt_data, password=resource_key)
    print("decrypt_key :", crypt_key)

