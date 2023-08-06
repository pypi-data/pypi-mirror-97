from rest_framework.serializers import ModelSerializer

from unchained_notification.models import Notification


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
