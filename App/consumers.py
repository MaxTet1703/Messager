""" Module for serialize """

import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from django.db.models import Q
from channels.db import database_sync_to_async

from .models import Users, Message, Chats


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
                'id': user.pk,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'photo_image': user.profile_image.url,
                'is_yourself': True if user == self.scope['user'] else False,
                'is_friend': True if user.chats.all().intersection(self.scope['user'].chats.all()).exists() else False
            }
            for user in users
        ]
        return users_data


class MessageConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, message):
        self.room_name = f"chat{self.scope['url_route']['kwargs']['id']}"
        await self.channel_layer.group_add(self.room_name, 
                                            self.channel_name)
        await self.accept()
    
    async def websocket_receive(self, message):
        message = message["text"]
        user_id = self.scope["user"].id
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chatroom_message",
                "message": message,
                "user_id": user_id,
                "chat_id": self.scope['url_route']['kwargs']['id']
            }
        )

    async def chatroom_message(self, event):
        await self.add_message(event["message"],
                               self.scope["user"],
                               await self.get_chat(event["chat_id"])
                            )
        await self.send(json.dumps({
            "message": event["message"],
            "user_id": event["user_id"]
             }, ensure_ascii=False)
        )

    @database_sync_to_async
    def get_chat(self, id):
        return Chats.objects.get(pk=id)

    @database_sync_to_async
    def add_message(self, message, user, chat):
        Message.objects.create(user=user, chat=chat, text=message)

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard(self.room_name,
                                             self.channel_name)
