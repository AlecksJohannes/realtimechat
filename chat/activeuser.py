from rest_framework.views import APIView
import jwt

from django.contrib.auth import get_user_model
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from django.forms.models import model_to_dict
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)
from models import User
from rest_framework_jwt.settings import api_settings
from django.http import JsonResponse
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

class ActivateUser(APIView):
    def get(self, request, *args, **kwargs):
        token = JSONWebTokenAuthentication().get_jwt_value(request)
        print(token)
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = User.objects.get(id=payload.get('user_id'))
        return JsonResponse({'code': 302, 'current_user': user.username})


class JSONWebTokenAuthentication(ActivateUser):
    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            return None

        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]
