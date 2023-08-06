from fcm_django.api.rest_framework import DeviceViewSetMixin, FCMDeviceSerializer
from fcm_django.models import FCMDevice
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from unchained_notification.models import Notification
from unchained_notification.serializers import NotificationSerializer


class NotificationViewSet(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NoListingFCMDeviceViewSet(DeviceViewSetMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = FCMDevice.objects.filter(active=True)
    serializer_class = FCMDeviceSerializer


