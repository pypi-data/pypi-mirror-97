
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from social_core.backends import facebook
from google.oauth2 import id_token, service_account
from google.auth.transport import requests
from unchained_auth.serializers import GoogleUIDSerializer
from django.conf import settings

try:
    credentials = service_account.Credentials.from_service_account_file(settings.GOOGLE_APPLICATION_CREDENTIALS)
    credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
except (TypeError, FileNotFoundError):
    pass


class SocialView(generics.CreateAPIView):
    serializer_class = GoogleUIDSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        User = get_user_model()
        backend = kwargs.get('backend')
        serializer = self.get_serializer(data=request.data)
        assert serializer.is_valid(), "Invalid token"
        token = serializer.validated_data['token']
        user = None
        if backend == 'google':
            idinfo = id_token.verify_oauth2_token(token, requests.Request())
            assert idinfo.get('iss') in ['accounts.google.com', 'https://accounts.google.com'], 'Wrong issuer.'
            email = idinfo['email']
            user, _ = User.objects.get_or_create(email=email)
            user.set_unusable_password()
            user.last_name = idinfo['family_name']
            user.first_name = idinfo['given_name']
            user.save()
        elif backend == 'facebook':
            user = facebook.FacebookOAuth2().do_auth(access_token=token)

        assert user, 'Unauthorized'
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
                'token': token.key
        }, status=status.HTTP_200_OK)


