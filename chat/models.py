# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.six import python_2_unicode_compatible
from django.db import models
from django.forms.models import model_to_dict
from django.http import JsonResponse
import bcrypt
import json

@python_2_unicode_compatible
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

def user_create(request):
    if request.method == 'POST':
        user = User(first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email'),
            password = bcrypt.hashpw(request.POST.get('password').encode('utf-8'), bcrypt.gensalt(14)))
        user.save()
        return json.dumps(model_to_dict(user))
    else:
        return JsonResponse({'status':'false','message':'cykablyat', 'code': 404})


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
