from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    chatroom = None

    async def connect(self):
        from unchained_chat.models import ChatRoom
        chatroom_id = self.scope["url_route"]["kwargs"]["chatroom_id"]

        if chatroom_id == 'test':
            await self.accept()
        else:
            self.chatroom = ChatRoom.objects.get(nom=self.scope["url_route"]["kwargs"]["chatroom_id"])
            self.group_name = 'CHATROOM{}'.format(self.chatroom.nom)

        if self.scope["user"].is_anonymous:
            await self.accept()  # todo await self.close()
            return
        else:
            await self.accept()
            # todo verify if the  user has access to this group

            await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, close_code):
        if self.chatroom:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.close()

    async def receive_json(self, content, **kwargs):
        from unchained_chat.models import Message

        message = content['message']
        username = (self.scope["user"].is_anonymous and 'anonymous') or self.scope["user"].username

        Message.objects.create(
            room=self.chatroom,
            username=username,
            message=message,
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        # message = event['message']

        print(event)

        del event['type']

        await self.send_json(event)
