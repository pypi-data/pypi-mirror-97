from django.contrib import admin

from unchained_chat.inlines import MessageInline
from unchained_chat.models import ChatRoom

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    inlines = [MessageInline]
    list_display = ['name']
