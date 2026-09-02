"""
ASGI application entrypoint.

HTTP traffic is handled by Django; WebSocket traffic is routed through Channels
with JWT query-token authentication middleware.
"""

import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chat.jwt_auth import JwtAuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            JwtAuthMiddlewareStack(
                URLRouter(chat.routing.websocket_urlpatterns)
            )
        ),
    }
)