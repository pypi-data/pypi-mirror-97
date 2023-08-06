from rest_framework.viewsets import ReadOnlyModelViewSet

from unchained_chat.models import ChatRoom
from unchained_chat.serializers import ChatRoomSerializer


class ChatRoomViewSet(ReadOnlyModelViewSet):
    serializer_class = ChatRoomSerializer

    def get_queryset(self, queryset=None):
        return ChatRoom.objects.filter(users__in=[self.request.user])




