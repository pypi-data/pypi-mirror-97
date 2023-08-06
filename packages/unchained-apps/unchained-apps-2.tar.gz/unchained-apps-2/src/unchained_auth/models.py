import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from unchained_utils.v0.base_classes import LowerCaseEmailField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise TypeError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        if not password:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractUser):
    objects = UserManager()

    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()]
    )
    email = LowerCaseEmailField(unique=True, null=True, blank=True )
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)

    is_active = models.BooleanField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def save(self, *args, **kwargs):
        if not self.username:
            if self.email:
                self.username = self.email
            elif self.phone:
                self.username = f'user_{self.phone}'
            else:
                self.username = self.id
        super().save()

    def __str__(self):
        return f"{self.email or self.username or self.id}"
