from unchained_auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import Group


admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['__str__', 'username', 'email', 'phone']
    search_fields = ('id', 'username', 'email', 'phone')
    ordering = ('created_at',)
    date_hierarchy = 'created_at'


