# SeaWave/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat_service.routing import websocket_urlpatterns  # Correct import

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeaWave.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    }
)
