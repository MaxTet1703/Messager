from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Value, Q
from channels.db import database_sync_to_async
from django.db.models.functions import Concat

from .models import Users


class SearchConsumer(AsyncJsonWebsocketConsumer):

    async def websocket_connect(self, message):
        await self.accept()

    async def websocket_receive(self, message):
        full_name = message["text"].split()
        users = await self.get_users(full_name)
        await self.send_json(users)

    async def websocket_disconnect(self, message):
        await self.close()

    @database_sync_to_async
    def get_users(self, full_name):
        if len(full_name) == 2:
            return Users.objects.filter(
                Q(first_name__trigram_similar=full_name[0]) & Q(last_name__trigram_similar=full_name[1]))
        else:
            return Users.objects.filter(Q(first_name__trigram_similar=full_name[0]))
