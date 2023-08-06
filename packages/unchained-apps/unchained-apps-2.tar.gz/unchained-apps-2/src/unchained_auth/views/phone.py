import firebase_admin
from firebase_admin import auth
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


from django.conf import settings
from unchained_auth.serializers import GoogleUIDSerializer

try:
    firebase_credentials = firebase_admin.credentials.Certificate(
        settings.GOOGLE_APPLICATION_CREDENTIALS
    )
    firebase_admin.initialize_app(firebase_credentials)
except (FileNotFoundError,TypeError, ValueError):
    pass


class PhoneLogin(generics.CreateAPIView):
    serializer_class = GoogleUIDSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        assert serializer.is_valid(), "Invalid token"

        uid = serializer.validated_data['uid']
        firebase_user = auth.get_user(uid)

        self.request.user.phone = firebase_user.phone_number
        self.request.user.user.save()
        token, _ = Token.objects.get_or_create(user=self.request.user)
        return Response({
                    'token': token.key,
        }, status=status.HTTP_200_OK)
