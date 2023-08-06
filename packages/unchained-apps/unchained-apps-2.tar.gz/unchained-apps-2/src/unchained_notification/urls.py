from django.urls import path, include
from rest_framework import routers

from unchained_notification.views import NoListingFCMDeviceViewSet, NotificationViewSet


router = routers.DefaultRouter()
router.register(r'devices', NoListingFCMDeviceViewSet)
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
]