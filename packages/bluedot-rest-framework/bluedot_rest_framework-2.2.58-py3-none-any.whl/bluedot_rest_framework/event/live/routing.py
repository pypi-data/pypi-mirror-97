from django.conf.urls import url
from bluedot_rest_framework import import_string


LiveConsumer = import_string('event.live.consumers')


websocket_urlpatterns = [
    url(r'ws/event/live/(?P<event_id>\w+)', LiveConsumer),
]
