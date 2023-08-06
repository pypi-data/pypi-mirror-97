from django.contrib import admin

from unchained_chat.models import Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1

    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is not None, so this is an edit
            return list(set(
                [field.name for field in self.model._meta.local_fields] +
                [field.name for field in self.model._meta.local_many_to_many]
            ))  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []

    def has_add_permission(self, request, obj):
        return False

    can_delete = False
