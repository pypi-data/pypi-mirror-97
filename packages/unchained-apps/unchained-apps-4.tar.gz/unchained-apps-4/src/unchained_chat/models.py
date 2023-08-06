import uuid

from django.contrib.auth import get_user_model
from django.db import models
from unchained_utils.v0 import unBaseModel
from unchained_utils.v0.base_classes import LooseManyToManyField, generate_short_code


def generate_chatroom_code():
    return generate_short_code('R', 8)

class ChatRoom(unBaseModel):
    id = models.CharField(max_length=20, primary_key=True, default=generate_chatroom_code, editable=False)
    name = models.CharField(max_length=30, unique=True)
    users = LooseManyToManyField(get_user_model())
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    @property
    def last_message(self):
        try:
            message = self.messages.order_by('-timestamp')[0]
            return {"username": message.username, "message": message.message, "timestamp": message.timestamp}
        except:
            return {"username": "", "message": "Nouvelle conversation", "timestamp": self.timestamp}

    class Meta:
        ordering = ('-timestamp',)

    @property
    def get_messages(self):
        return self.messages.order_by('-timestamp')[:20]

    def save(self, *args, **kwargs):
        force_update = False

        if self.id:
            force_update = True

        super(ChatRoom, self).save(force_update=force_update)

    def __str__(self):
        return "%s (%s)" % (self.name, self.id)


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    username = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)

    def save(self, *args, **kwargs):
        super(Message, self).save()
