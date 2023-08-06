import requests
from django.conf import settings
from rest_framework import status
from ..models import WeChatUserOpenid
from rest_framework.views import APIView
from wechatpy.replies import ArticlesReply
from wechatpy import parse_message, create_reply, utils
from django.shortcuts import HttpResponse
from bluedot_rest_framework.analysis.monitor.models import AnalysisMonitor
from ..handle import WeChatUserSet
from .models import WeChatResponseMaterial, WeChatResponseEvent


class Response(APIView):
    permission_classes = ()
    reply_text = '感谢关注'

    def get(self, request, *args, **kwargs):
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echo_str = request.GET.get('echostr')
        token = settings.BLUEDOT_REST_FRAMEWORK['wechat']['offiaccount']['TOKEN']
        utils.check_signature(token, signature, timestamp, nonce)
        return HttpResponse(echo_str)

    def post(self, request, *args, **kwargs):
        msg = parse_message(request.body)
        msg_dict = msg.__dict__['_data']
        data = {
            '_type': '微信响应日志',
            'user_openid': msg_dict['FromUserName'],
            'wechat_user_name': msg_dict['ToUserName'],
            'wechat_appid': settings.BLUEDOT_REST_FRAMEWORK['wechat']['offiaccount']['APPID'],
            'wechat_name': '',
            'wechat_event_key': '',
            'wechat_event_msg': '',
            'wechat_event_type': msg_dict['MsgType']
        }
        if 'EventKey' in msg_dict:
            data['wechat_event_key'] = msg_dict['Event']
        if 'Content' in msg_dict:
            data['wechat_event_msg'] = msg_dict['Content']
        elif msg_dict['MsgType'] == 'event':
            data['wechat_event_msg'] = msg_dict['EventKey']

        AnalysisMonitor.objects.create(**data)

        default_subscribe_text_queryset = WeChatResponseEvent.objects.filter(
            event_type=0).first()
        if default_subscribe_text_queryset:
            queryset = WeChatResponseMaterial.objects.get(
                pk=default_subscribe_text_queryset.material_id)
            self.reply_text = queryset.content

        if msg.type == 'text':
            queryset = WeChatResponseEvent.objects.filter(
                text=msg_dict['Content']).first()
            if queryset:
                if queryset.remark == 'article':
                    queryset = WeChatResponseMaterial.objects.get(
                        pk=queryset.material_id)
                    reply = ArticlesReply(message=msg)
                    reply.add_article({
                        'title': queryset.remark,
                        'description': queryset.remark,
                        'image': queryset.title,
                        'url': queryset.content
                    })
                    response = HttpResponse(
                        reply.render(), content_type="application/xml")
                    return response
                else:
                    queryset = WeChatResponseMaterial.objects.get(
                        pk=queryset.material_id)
                    self.reply_text = queryset.content
            else:
                self.perform_text(msg_dict)

        elif msg.type == 'event':
            openid = msg_dict['FromUserName']
            if msg_dict['Event'] == 'unsubscribe':
                open_queryset = WeChatUserOpenid.objects.filter(
                    openid=openid).first()
                open_queryset.subscribe = 0
                open_queryset.save()

            elif msg_dict['Event'] == 'SCAN' or msg_dict['Event'] == 'subscribe_scan' or msg_dict['Event'] == 'CLICK':
                queryset = WeChatResponseEvent.objects.filter(
                    event_key=msg_dict['EventKey']).first()
                if queryset:
                    queryset = WeChatResponseMaterial.objects.get(
                        pk=queryset.material_id)
                    self.reply_text = queryset.content
                else:
                    self.perform_event(msg_dict)

            if msg_dict['Event'] in ['subscribe', 'subscribe_scan']:
                openid = openid = msg_dict['FromUserName']
                open_queryset = WeChatUserOpenid.objects.filter(
                    openid=openid).first()
                open_queryset.subscribe = 1
                open_queryset.save()

        reply = create_reply(self.reply_text, msg)
        response = HttpResponse(
            reply.render(), content_type="application/xml")
        return response

    def perform_event(self, msg_dict):
        pass

    def perform_text(self, msg_dict):
        pass
