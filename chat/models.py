# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.six import python_2_unicode_compatible
from django.db import models
from django.forms.models import model_to_dict
from django.http import JsonResponse
from chat import utils
import bcrypt
import json
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import UserManager

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
@python_2_unicode_compatible
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    is_authenticated = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
    objects = UserManager()

    def __str__(self):
        return "%s" % (self.username)

def user_create(request):
    if request.method == 'POST':
        user = User(username = request.POST.get('username'),
            password = bcrypt.hashpw(request.POST.get('password').encode('utf-8'), bcrypt.gensalt(14)),
            is_active = True,
            is_anonymous = False,
            is_authenticated = True)
        user.save()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return JsonResponse({'status':'success','token': token, 'code': 302, 'id': user.id })
    else:
        return JsonResponse({'status':'false','message':'cykablyat', 'code': 404})


def user_login(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.POST.get('username'))
            if bcrypt.checkpw(request.POST.get('password').encode('utf-8'), user.password.encode('utf-8')):
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return JsonResponse({'status':'success','message':'cykablyat', 'code': 302, 'token': token, 'id': user.id})
            else:
                return JsonResponse({'status':'failure','message':'cykablyat', 'code': 404})
        except User.DoesNotExist:
            return JsonResponse({'status':'failure','message':'User not found', 'code': 404})


class Conversation(models.Model):
    sender = models.ForeignKey(User, related_name='%(class)s_sender')
    recipient= models.ForeignKey(User, related_name='%(class)s_receipient')


@python_2_unicode_compatible
class Message(models.Model):
    body = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    is_read = models.BooleanField(default=False)
    conversation = models.ForeignKey(Conversation)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % (self.body)
