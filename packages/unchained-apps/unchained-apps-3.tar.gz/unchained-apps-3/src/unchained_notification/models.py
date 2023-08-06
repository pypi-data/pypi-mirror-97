from django.contrib.auth import get_user_model
from django.db import models
from fcm_django.models import FCMDevice
from unchained_utils.v0.base_classes import LooseForeignKey, unBaseModel


class Notification(unBaseModel):
    user = LooseForeignKey(get_user_model(), blank=True)
    text = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    payload = models.TextField(null=True, blank=True)

    def send_notification(self):
        if self.user.exists():
            devices = FCMDevice.objects.filter(user_id__in=list(self.user.values_list('id', flat=True)),
                                               active=True)
        else:
            devices = FCMDevice.objects.filter(active=True)
        devices.send_message(title=self.title, body=self.text, sound=True,
                             data={"category": self.type, 'payload': self.payload},
                             extra_kwargs={
                                 "actions": [
                                     {
                                         "title": "Accept",
                                         "action": "accept",
                                         "icon": "icons/heart.png"
                                     },
                                     {
                                         "title": "Ignore",
                                         "action": "ignore",
                                         "icon": "icons/cross.png"
                                     }
                                 ]})

    def __str__(self):
        return f"{self.id}"
