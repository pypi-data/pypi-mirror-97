from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from unchained_chat.views import ChatRoomViewSet


router = routers.DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet, basename='chatrooms')

urlpatterns = [
    path('test', TemplateView.as_view(template_name='templates/websocket_test.html')),
    path('', include(router.urls)),
]