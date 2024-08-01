import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = f"chat_{self.scope['url_route']['kwargs']['chat_name']}"
        await self.channel_layer.group_add(self.chat_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json
    
    async def send_message(self, event):
        data = event['message']
        await self.create_message(data=data)
        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data):
        get_chat_by_name = Chat.objects.get(chat_name=data['chat_name'])
        if not Message.objects.filter(message=data['message']).exists():
            new_message = Message(chat=get_chat_by_name, sender=data['sender'], message=data['message'])
            new_message.save()