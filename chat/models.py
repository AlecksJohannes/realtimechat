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

@python_2_unicode_compatible
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    is_authenticated = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

def user_create(request):
    if request.method == 'POST':
        user = User(username = request.POST.get('username'),
            email = request.POST.get('email'),
            is_authenticated = True,
            is_anonymous = False,
            password = bcrypt.hashpw(request.POST.get('password').encode('utf-8'), bcrypt.gensalt(14)))
        user.save()
        return json.dumps(model_to_dict(user))
    else:
        return JsonResponse({'status':'false','message':'cykablyat', 'code': 404})


def user_login(request):
    if request.method == 'POST':
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        try:
            user = User.objects.get(email = request.POST.get('email'))
            if bcrypt.checkpw(request.POST.get('password').encode('utf-8'), user.password.encode('utf-8')):
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return JsonResponse({'status':'success','message':'cykablyat', 'code': 302, 'token': token })
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
    def __str__(self):
        return "%s" % (self.body)
