from django.urls import path

from .consumers import *

websocket_urlpatterns = [
    path('ws/main', SearchConsumer.as_asgi(), name="wsmain"),
    path('ws/chats/<int:id>/', MessageConsumer.as_asgi(), name="wssend")
]
