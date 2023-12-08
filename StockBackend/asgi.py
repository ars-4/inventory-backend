import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# from channels.security import AllowedHostsOriginValidator
from django.urls import path
from core import asgi as core_asgi
from core.urls import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StockBackend.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    # 'websocket': chats_asgi.application,
    'websocket':AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
})
