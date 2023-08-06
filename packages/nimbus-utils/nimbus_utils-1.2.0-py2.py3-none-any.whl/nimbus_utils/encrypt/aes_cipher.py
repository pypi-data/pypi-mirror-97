# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import base64
import string
import logging
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from nimbus_utils.encoding import smart_bytes, smart_str
from nimbus_utils.crypto import get_random_string

__all__ = ["cryptor", "AESCipherCryptor"]

logger = logging.getLogger("encrypt")


class AESCipherCryptor(object):
    """
    AES/ECB/PKCS7Padding 加密解密
    MODE: ECB
    PADDING: PKCS#7
    SALT: NONE
    """
    random_strings = string.ascii_letters + string.digits

    @classmethod
    def generate_key(cls, size=16):
        return get_random_string(size, cls.random_strings)

    def _get_aes(self, key, mode=AES.MODE_ECB, **kwargs):
        """
        初始化AES,ECB模式的实例
        :param key:
        :param mode:
        :param kwargs:
        :return:
        """
        return AES.new(smart_bytes(key), mode, **kwargs)

    def encrypt(self, data, key, mode=AES.MODE_ECB, **kwargs):
        """
        加密函数
        :param data:
        :param key:
        :param mode:
        :param kwargs:
        :return:
        """
        try:
            aes = self._get_aes(key, mode=mode, **kwargs)
            res = aes.encrypt(smart_bytes(self.pkcs7_padding(data)))
            endata = smart_str(base64.urlsafe_b64encode(res))
        except Exception as e:
            logger.error(e)
            endata = ""
        return endata

    def decrypt(self, data, key, mode=AES.MODE_ECB, **kwargs):
        """
        解密函数
        :param data:
        :param key:
        :param mode:
        :param kwargs:
        :return:
        """
        try:
            aes = self._get_aes(key, mode=mode, **kwargs)
            res = base64.urlsafe_b64decode(smart_bytes(data))
            msg = aes.decrypt(res).decode("utf8")
            dedata = smart_str(self.pkcs7_unpadding(smart_bytes(msg)))
        except Exception as e:
            logger.error(e)
            dedata = ""
        return dedata

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    @staticmethod
    def pkcs7_unpadding(padded_data):
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data)
        try:
            uppadded_data = data + unpadder.finalize()
        except ValueError:
            raise Exception('无效的加密信息!')
        else:
            return uppadded_data


cryptor = AESCipherCryptor()


if __name__ == '__main__':
    key = "WyfFvacE0fWyb1A277vgo2UIIMvTs8mX"
    print(key)
    data = "0990e3dac6448c6c583bd74992cc8a42"
    encrypt_text = cryptor.encrypt(data, key)
    print('encrypt_text:', encrypt_text)
    decrypt_text = cryptor.decrypt(encrypt_text, key)
    print('decrypt_text:', decrypt_text)
