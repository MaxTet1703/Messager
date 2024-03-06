import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Q
from channels.db import database_sync_to_async
from rest_framework.renderers import JSONRenderer

from .models import Users
from .serializers import UsersSerializer


class SearchConsumer(AsyncJsonWebsocketConsumer):

    async def websocket_connect(self, message):
        await self.accept()

    async def websocket_receive(self, message):
        users = await self.get_users(message["text"])

        await self.send(json.dumps(users, ensure_ascii=False))

    async def websocket_disconnect(self, message):
        await self.close()

    @database_sync_to_async
    def get_users(self, full_name):
        users = Users.objects.filter(
            Q(first_name__trigram_similar=full_name) | Q(last_name__trigram_similar=full_name))
        users_data = [
            {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'photo_image': user.profile_image.url
            }
            for user in users
        ]
        return users_data
