import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from bluedot_rest_framework import import_string


class WechatLoginConsumer(WebsocketConsumer):
    def connect(self):
        self.scene_str = self.scope['url_route']['kwargs']['scene_str']
        self.room_group_name = self.scene_str

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = {
            'token': text_data_json.get('token', None)
        }

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'wechat_login_message',
                **data
            }
        )

    # Receive message from room group

    def wechat_login_message(self, data):
        self.send(text_data=json.dumps({
            **data
        }))
