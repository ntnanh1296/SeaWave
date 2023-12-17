# SeaWave/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat_service.routing import websocket_urlpatterns  # Import your WebSocket routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeaWave.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        websocket_urlpatterns
    ),
})
