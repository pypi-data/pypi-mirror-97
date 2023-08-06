from django.urls import path, re_path
from django.conf import settings

urlpatterns = []

if settings.UNCHAINED_AUTH.get('PWD'):
    from unchained_auth.views.main import LoginView, LogoutView

    urlpatterns.extend([
        path('login/', LoginView.as_view(), name='un_login'),
        path('logout/', LogoutView.as_view(), name='un_logout'),
    ])

if settings.UNCHAINED_AUTH.get('PWD_REGISTER'):
    from unchained_auth.views.main import RegisterAPIView

    urlpatterns.extend([
        path('register/', RegisterAPIView.as_view(), name='un_register')
    ])

if settings.UNCHAINED_AUTH.get('PHONE'):
    from unchained_auth.views.phone import PhoneLogin

    urlpatterns.extend([
        path('phone/verify/', PhoneLogin.as_view(), name='un_phone_verify')
    ])

if settings.UNCHAINED_AUTH.get('SOCIAL'):
    from unchained_auth.views.social import SocialView

    urlpatterns.extend([
        re_path(r'social/(?P<backend>[^/]+)/auth/',
                SocialView.as_view(), name='un_social_auth')
    ])

if settings.UNCHAINED_AUTH.get('PWD_RESET'):
    pass
