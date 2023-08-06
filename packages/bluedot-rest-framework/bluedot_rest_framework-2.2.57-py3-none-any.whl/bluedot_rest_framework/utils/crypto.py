import re
import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from django.conf import settings


class AESEncrypt(object):
    iv = settings.BLUEDOT_REST_FRAMEWORK['utils']['AES']['iv']
    key = settings.BLUEDOT_REST_FRAMEWORK['utils']['AES']['key']

    def __init__(self):
        self.model = AES.MODE_CBC

    def add_to_16_cn(self, text):
        pad = 16 - len(text.encode('utf-8')) % 16
        text = text + pad * chr(pad)
        return text.encode('utf-8')

    def encrypt(self, text):
        text = self.add_to_16_cn(text)
        cryptos = AES.new(self.key.encode('utf-8'),
                          AES.MODE_CBC, self.iv.encode('utf-8'))
        cipher_text = cryptos.encrypt(text)
        return base64.b64encode(cipher_text).decode('utf-8')  # base编码

    def decrypt(self, text):
        cryptos = AES.new(self.key.encode('utf-8'),
                          AES.MODE_CBC, self.iv.encode('utf-8'))
        text = base64.b64decode(text)  # base64解码
        plain_text = cryptos.decrypt(text)

        # 去除解码后的非法字符
        result = re.compile(
            '[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', plain_text.decode('utf-8'))
        return result


AESEncrypt = AESEncrypt()
