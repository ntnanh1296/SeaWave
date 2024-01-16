# chat_service/routing.py

from django.urls import re_path
from channels.layers import DEFAULT_CHANNEL_LAYER

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
