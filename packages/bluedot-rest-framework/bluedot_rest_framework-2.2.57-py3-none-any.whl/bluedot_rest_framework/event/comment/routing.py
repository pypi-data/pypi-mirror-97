from django.conf.urls import url
from bluedot_rest_framework import import_string


CommentConsumer = import_string('event.comment.consumers')

websocket_urlpatterns = [
    url(r'ws/event/comment/(?P<schedule_id>\w+)', CommentConsumer),
]
