from django.contrib import admin

from unchained_notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
