import base64
import json
import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import Room, Person, Message, File, Origin
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

# rooms = []
online_users = []

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.current_room = None

        self.order_room = "order"
        self.order_group_name = f"chat_{self.order_room}"

        self.product_room = "product"
        self.product_group_name = f"chat_{self.product_room}"

        # token = self.scope["query_string"].decode().split("=")[1]
        # user_token = await database_sync_to_async(Token.objects.get, thread_sensitive=True)(key=token)

        # # path, headers, client, server, method

        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.channel_layer.group_add(self.order_group_name, self.channel_name)
        await self.channel_layer.group_add(self.product_group_name, self.channel_name)
        # self.user = user_token.user

            
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.close()


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = ""
        order = ""
        product = ""
        token = ""

        timestamp = str(datetime.datetime.now()).split(".")[0]
        if "message" in text_data_json:
            message = text_data_json["message"]
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message, "token": "token", "user": "user", "timestamp": timestamp, "room": self.room_name}
            )

        if "token" in text_data_json:
            token = text_data_json["token"]
            # user_token = await database_sync_to_async(Token.objects.get, thread_sensitive=True)(key=token)
            # user = user_token.user.username
            # person = await database_sync_to_async(Person.objects.get, thread_sensitive=True)(user=user_token.user)


        if "order" in text_data_json:
            order = text_data_json["order"]
            await self.channel_layer.group_send(
                self.order_group_name, {"type": "chat.order", "order": order, "token": "token", "user": "user", "timestamp": timestamp, "room": self.room_name, "msg_type": "msg"}
            )
        
        
        if "product" in text_data_json:
            product = text_data_json["product"]
            await self.channel_layer.group_send(
                self.product_group_name, {"type": "chat.product", "product": product, "token": "token", "user": "user", "timestamp": timestamp, "room": self.room_name, "msg_type": "msg"}
            )

        # if "file" in text_data_json:
        #     uploaded_file_data = text_data_json["file"]
        #     file_name = uploaded_file_data["name"]
        #     file_content = uploaded_file_data["content"]
        #     # file_type = uploaded_file_data["type"]
        #     file_content = base64.b64decode(file_content)
        #     # uploaded_file = ContentFile(file_content_bytes, name=file_name)

        #     if file_name.endswith(".jpg") or file_name.endswith(".jpeg"):
        #         content_type = "image/jpeg"
        #     elif file_name.endswith(".png"):
        #         content_type = "image/png"
        #     elif file_name.endswith(".pdf"):
        #         content_type = "application/pdf"
        #     else:
        #         content_type = "application/octet-stream"

        #     uploaded_file = InMemoryUploadedFile(
        #         ContentFile(file_content),
        #         field_name=None,
        #         name=file_name,
        #         content_type=content_type,
        #         size=len(file_content),
        #         charset=None,
        #     )
        #     uploaded_file.seek(0)
        #     file_obj = File.objects.create(
        #         room=room,
        #         user=person,
        #         uploaded_file=uploaded_file
        #     )
        #     file_obj.save()
        #     file_url = f"{self.current_host}{file_obj.uploaded_file.url}"
        #     message = f"{file_url}"


        # if "Welcome to the chat" not in message:
        #     Message.objects.create(
        #         sender=person,
        #         room=room,
        #         content=message
        #     ).save()
    

    async def chat_message(self, event):
        message = event["message"]
        timestamp = str(datetime.datetime.now()).split(".")[0]

        user = 'Anonymous'

        # user_token = await database_sync_to_async(Token.objects.get, thread_sensitive=True)(key=token)
        # user = user_token.user.username
        
        await self.send(text_data=json.dumps({"message": message, "token": "token", "user": user, "timestamp": timestamp, "room": self.room_name}))

    async def chat_order(self, event):
        order = event["order"]
        # token = event["token"]
        timestamp = str(datetime.datetime.now()).split(".")[0]

        # user = 'Anonymous'

        # user_token = await database_sync_to_async(Token.objects.get, thread_sensitive=True)(key=token)

        await self.send(text_data=json.dumps({"order": order, "token": "token", "user": "user", "timestamp": timestamp, "room": self.room_name}))


    async def chat_product(self, event):
        product = event["product"]
        # token = event["token"]
        timestamp = str(datetime.datetime.now()).split(".")[0]

        # user = 'Anonymous'

        # user_token = await database_sync_to_async(Token.objects.get, thread_sensitive=True)(key=token)

        await self.send(text_data=json.dumps({"product": product, "token": "token", "user": "user", "timestamp": timestamp, "room": self.room_name}))

    
    
    