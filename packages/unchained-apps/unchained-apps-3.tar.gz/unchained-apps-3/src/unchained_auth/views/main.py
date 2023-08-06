from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token as Rest_Token
from unchained_auth.serializers import UserSerializer


class RegisterAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        assert serializer.is_valid(), str(serializer._errors)
        new_user = get_user_model()(
                email=request.data['email']
        )
        new_user.set_password(request.data['password'])
        new_user.save()
        return Response(status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Rest_Token.objects.get(key=response.data['token'])

        return Response({
            'token': token.key
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
