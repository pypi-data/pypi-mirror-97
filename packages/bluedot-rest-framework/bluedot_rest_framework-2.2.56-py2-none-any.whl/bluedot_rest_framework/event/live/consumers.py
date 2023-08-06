import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from bluedot_rest_framework import import_string
from .models import EventLivePPTCurrent

class LiveConsumer(WebsocketConsumer):
    def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.room_group_name = 'live_%s' % self.event_id

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
            'event_id':self.event_id,
            'activeIndex': text_data_json.get('activeIndex', None),
        }
        EventLivePPTCurrent.objects.create(**data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
                {
                    'type': 'event_live_message',
                    **data
                }
            )
    # Receive message from room group

    def event_live_message(self, event):
        self.send(text_data=json.dumps({
            **event
        }))
