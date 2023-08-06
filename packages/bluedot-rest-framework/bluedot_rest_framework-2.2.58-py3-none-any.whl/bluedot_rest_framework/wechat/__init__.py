
import base64
import json
from redis import Redis
from Crypto.Cipher import AES
from django.conf import settings
from wechatpy.oauth import WeChatOAuth
from wechatpy.client import WeChatClient
from wechatpy.session.redisstorage import RedisStorage
from bluedot_rest_framework import import_string

redis_client = Redis.from_url(
    settings.BLUEDOT_REST_FRAMEWORK['wechat']['redis_client'])
session_interface = RedisStorage(
    redis_client,
    prefix='wechatpy'
)


def App(appid):
    Config = import_string('config.models')
    queryset = Config.objects.get(config_type=1)
    return WeChatClient(
        appid,
        queryset.value[appid]['SECRET'],
        session=session_interface
    )


MiniProgram = WeChatClient(
    settings.BLUEDOT_REST_FRAMEWORK['wechat']['miniprogram']['APPID'],
    settings.BLUEDOT_REST_FRAMEWORK['wechat']['miniprogram']['SECRET'],
    session=session_interface
)

OfficialAccount = WeChatClient(
    settings.BLUEDOT_REST_FRAMEWORK['wechat']['offiaccount']['APPID'],
    settings.BLUEDOT_REST_FRAMEWORK['wechat']['offiaccount']['SECRET'],
    session=session_interface
)


def official_account_oauth(redirect_uri, scope='snsapi_base', state=''):
    return WeChatOAuth(
        settings.BLUEDOT_REST_FRAMEWORK['wechat']['offiaccount']['APPID'],
        settings.BLUEDOT_REST_FRAMEWORK['wechat']['offiaccount']['SECRET'],
        redirect_uri,
        scope,
        state
    )


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
