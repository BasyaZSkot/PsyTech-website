import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chat
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.chat_group_name = f'chat_{self.chat_name}'
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name,
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )   

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        # if text_data_json["type"] == "read_status":
        #     message_id = text_data_json["id"]
        #     await self.mark_message_as_read(message_id)
        # else:
        await self.handle_new_message(text_data_json)
    
    # async def mark_message_as_read(self, message_id):
    #     try:
    #         message = await sync_to_async(Message.objects.get)(id=message_id)
    #         message.read_status = True
    #         await sync_to_async(message.save)()
    #         await self.send(json.dumps({
    #             "type": "read_status",
    #             "message": message.id,
    #             "user_id": message.sender.id  # Ensure message.sender is properly accessed
    #         }))
    #     except Message.DoesNotExist:
    #         await self.send(json.dumps({
    #             "type": "error",
    #             "message": "Message not found"
    #         }))
    
    async def handle_new_message(self, text_data_json):
        message_content = text_data_json['message']
        chat_name = text_data_json['chat_name']
        username = text_data_json['username']

        try:
            user = await sync_to_async(User.objects.get)(username=username)
            chat = await sync_to_async(Chat.objects.get)(chat_name=chat_name)

            message = await sync_to_async(Message.objects.create)(
                message=message_content, chat=chat, sender=user
            )
            timestamp = [
                message.timestamp.year,
                message.timestamp.month, 
                message.timestamp.day, 
                message.timestamp.hour, 
                message.timestamp.minute
            ]

            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'id': message.id,
                    'timestamp': timestamp,
                    'user_id': user.id,
                    'read_status': message.read_status,
                    'username': username
                }
            )
        except User.DoesNotExist:
            await self.send(json.dumps({
                "type": "error",
                "message": "User not found"
            }))
        except Chat.DoesNotExist:
            await self.send(json.dumps({
                "type": "error",
                "message": "Chat not found"
            }))
    
    async def chat_message(self, event):
        # if event["type"] == "read_status":
        #     await self.send(text_data=json.dumps({
        #         "type": "read_status",
        #         "message": event["message"],
        #         "user_id": event["user_id"]
        #     }))
        # else:
            await self.send(text_data=json.dumps({
                'type': 'chat',
                'message': event["message"],
                'id': event["id"],
                'timestamp': event["timestamp"],
                'user_id': event["user_id"],
                'read_status': event["read_status"],
                'username': event["username"]
            }))
