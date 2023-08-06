from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.func import orm_bulk_update
from bluedot_rest_framework.utils.jwt_token import jwt_create_token_wechat
from . import App
from .models import WeChatUser, WeChatUserOpenid

User = import_string('user.models')


class WeChatUserSet:
    appid = ''
    openid = ''

    user_data = None  # 用户信息
    wechat_user_queryset = None  # WeChatUser QuerySet

    def __init__(self, appid, user_info=None, openid=None):
        self.appid = appid
        if user_info or openid:
            if user_info:
                self.user_data = {
                    'unionid': user_info.get('unionid', ''),
                    'nick_name': user_info.get('nickname', ''),
                    'avatar_url': user_info.get('headimgurl', ''),
                    'gender': user_info.get('sex', ''),
                    'province': user_info.get('province', ''),
                    'city': user_info.get('city', ''),
                    'country': user_info.get('country', ''),
                    'language': user_info.get('language', ''),
                    
                }
                self.openid = user_info.get('openid', '')
                unionid=self.user_data['unionid']
                if unionid == '':
                    wechat_queryset = WeChatUserOpenid.objects.filter(
                    openid=self.openid).first()
                    if wechat_queryset:
                        wechat_id=wechat_queryset.wechat_id
                        self.wechat_user_queryset=WeChatUser.objects.filter(
                        pk=wechat_id).first()
                else:
                    self.wechat_user_queryset = WeChatUser.objects.filter(
                        unionid=self.user_data['unionid']).first()
                self.handle_user()
            else:
                self.openid = openid
                try:
                    user_info = App(self.appid).user.get(self.openid)
                    self.__init__(appid=self.appid, user_info=user_info)
                    unionid=self.user_data['unionid']
                    if unionid == '':
                        wechat_id = WeChatUserOpenid.objects.filter(
                        openid=self.openid).first().wechat_id
                        self.wechat_user_queryset=WeChatUser.objects.filter(
                        wechat_id=wechat_id).first()

                    else:
                        self.wechat_user_queryset = WeChatUser.objects.filter(
                            unionid=unionid).first()
                    self.handle_user()
                except:
                    wechat_user_openid_queryset = WeChatUserOpenid.objects.filter(
                        openid=openid).first()
                    if wechat_user_openid_queryset:
                        queryset = WeChatUser.objects.filter(
                            pk=wechat_user_openid_queryset.wechat_id).first()
                        if queryset:
                            self.wechat_user_queryset = WeChatUser.objects.filter(
                                unionid=queryset.unionid).first()
                    pass

    def create_user(self):
        subscribe = 0
        try:
            user = App(self.appid).user.get(self.openid)
            subscribe = user['subscribe']
        except:
            pass

        self.wechat_user_queryset = WeChatUser.objects.create(**self.user_data)
        openid_data = {
            'wechat': self.wechat_user_queryset,
            'appid': self.appid,
            'openid': self.openid,
            'subscribe': subscribe
        }
        WeChatUserOpenid.objects.create(**openid_data)

    def update_user(self):
        orm_bulk_update(self.wechat_user_queryset, self.user_data)

    def handle_user(self):
        if self.wechat_user_queryset:
            self.update_user()
        else:
            self.create_user()
 
    def get_token(self):
        token = ''
        if self.wechat_user_queryset:
            token = jwt_create_token_wechat(wechat_id=self.wechat_user_queryset.pk,
                                            unionid=self.wechat_user_queryset.unionid)
        return token
