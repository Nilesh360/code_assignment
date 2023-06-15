# chat/consumers.py
import json
from django.core.cache import cache
from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import HttpResponse


class ChatConsumer(AsyncWebsocketConsumer):
    connected_users = dict()
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        if self.room_name not in self.connected_users.keys():
            self.connected_users[self.room_name]=1
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

        elif self.connected_users[self.room_name]<2:
            self.connected_users[self.room_name]=self.connected_users[self.room_name]+1
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": 'Connection Establish'})
            await self.accept()
        else:
            await self.disconnect(close_code=1006)


    async def disconnect(self, close_code):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        if close_code == 1000:
            if self.room_name in self.connected_users.keys():
                del self.connected_users[self.room_name]
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": 'Connection Terminated'})
            print("Connection closed by client")

        elif close_code == 1001:
            if self.room_name in self.connected_users.keys():
                del self.connected_users[self.room_name]
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": 'Connection Terminated'})
            print("Client is going away")

        else:
            print("Connection Terminated abnormally ")


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))