import time
import random
import string
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from bluedot_rest_framework.utils.jwt_token import jwt_get_wechatid_handler, jwt_get_userid_handler
from bluedot_rest_framework import import_string
from . import App, WXBizDataCrypt, official_account_oauth
from .handle import WeChatUserSet
from .models import WeChatUser
from .serializers import WeChatUserSerializer

User = import_string('user.models')
UserSerializer = import_string('user.serializers')


class JSSdk(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        referer = request.META['HTTP_REFERER']
        appid = request.query_params.get('appid', '')

        ticket = App(appid).jsapi.get_jsapi_ticket()
        nonceStr = ''.join(random.sample(
            string.ascii_letters + string.digits, 8))
        timestamp = str(int(time.time()))
        signature = App(appid).jsapi.get_jsapi_signature(
            nonceStr, ticket, timestamp, referer)
        return Response({
            'appId': appid,
            'timestamp': timestamp,
            'nonceStr': nonceStr,
            'signature': signature,
        })


class Auth(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        appid = request.query_params.get('appid', None)
        code = request.query_params.get('code', None)
        session_info = App(appid).wxa.code_to_session(code)
        if 'unionid' in session_info:
            session_info['token'] = WeChatUserSet(
                appid=appid, openid=session_info['openid']).get_token()
        return Response(session_info)

    def post(self, request, *args, **kwargs):
        auth_data = request.data['data']
        appid = request.data['appid']
        auth_user = WXBizDataCrypt(
            appid, auth_data['session_key']
        ).decrypt(auth_data['encryptedData'], auth_data['iv'])
        user_info = {
            'openid': auth_user['openId'],
            'unionid': auth_user['unionId'],
            'nickname': auth_user['nickName'],
            'headimgurl': auth_user['avatarUrl'],
            'sex': auth_user['gender'],
            'language': auth_user['language'],
            'city': auth_user['city'],
            'province': auth_user['province'],
            'country': auth_user['country'],
        }
        token = WeChatUserSet(appid=appid, user_info=user_info).get_token()
        return Response({'token': token})


class OAuth(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        appid = request.query_params.get('appid', None)
        code = request.query_params.get('code', None)
        referer_uri = request.META['HTTP_REFERER']
        if code and appid:
            wechat_oauth = official_account_oauth(
                referer_uri, 'snsapi_userinfo')
            wechat_oauth.fetch_access_token(code)
            user_info = wechat_oauth.get_user_info()
            token = WeChatUserSet(appid=appid, user_info=user_info).get_token()
            return Response({'token': token, 'user_info': user_info})
        else:
            wechat_oauth = official_account_oauth(
                referer_uri, 'snsapi_userinfo')
            url = wechat_oauth.authorize_url
            return HttpResponseRedirect(url)


class OAuthDev(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        redirect_uri = "https://" + request.get_host() + request.get_full_path()
        code = request.query_params.get('code', None)
        referer_uri = request.query_params.get('referer_uri', None)
        if code:
            link_type = '?'
            if "?" in referer_uri:
                link_type = '&'
            uri = referer_uri + link_type + 'code=' + code
            return HttpResponseRedirect(uri)

        else:
            referer_uri = parse.quote(request.META['HTTP_REFERER'])
            link_type = '?'
            if "?" in referer_uri:
                link_type = '&'
            wechat_oauth = official_account_oauth(
                redirect_uri + link_type + 'referer_uri=' + referer_uri, 'snsapi_userinfo')
            url = wechat_oauth.authorize_url
            return HttpResponseRedirect(url)


class Current(APIView):

    def get(self, request, *args, **kwargs):
        wechat_id = jwt_get_wechatid_handler(request.auth)
        if wechat_id:
            queryset = WeChatUser.objects.get(pk=wechat_id)
            data = WeChatUserSerializer(queryset).data
            return Response(data)
        else:
            userid = jwt_get_userid_handler(request.auth)
            queryset = User.objects.get(pk=userid)
            data = UserSerializer(queryset).data
            return Response(data)


class Menu(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token', None)
        if token == 'e3340768d695c1591f352456ad51ab1c':
            OfficialAccount.menu.create({
                "button": [
                    {
                        "name": "关于我们",
                        "sub_button": [
                            {
                                "type": "miniprogram",
                                "name": "最新资讯",
                                "url": "http://cpa-global-wechat.bluewebonline.com/html/white_paper?source=menu",
                                "appid": "wx4c41efd924f3ef12",
                                "pagepath": "pages/index/index"
                            },
                            {
                                "type": "view",
                                "name": "资料中心",
                                "url": "http://cpa-global-wechat.bluewebonline.com/html/white_paper?source=menu",
                            },
                            {
                                "type": "view",
                                "name": "产品及解决方案",
                                "url": "http://cpa-global-wechat.bluewebonline.com/html/product?source=menu"
                            },
                        ]
                    },
                    {
                        "type": "view",
                        "name": "活动中心",
                        "url": "http://cpa-global-wechat.bluewebonline.com/html/home?source=menu"
                    },
                    {
                        "type": "view",
                        "name": "联系我们",
                        "url": "http://cpa-global-wechat.bluewebonline.com/html/contact_us?source=menu"
                    },
                ],
            })
        return Response()
