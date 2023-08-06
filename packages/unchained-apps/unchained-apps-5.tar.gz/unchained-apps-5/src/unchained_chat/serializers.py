from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from unchained_chat.models import Message, ChatRoom


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatRoomSerializer(ModelSerializer):
    messages = MessageSerializer(many=True)
    last_message = serializers.ReadOnlyField()

    class Meta:
        model = ChatRoom
        fields = '__all__'
