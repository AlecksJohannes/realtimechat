# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .models import Conversation, User, user_create
import json
from channels import Group
from .utils import get_conversation_or_create_new
from .utils import error_response
from django.forms.models import model_to_dict

parsed_json = {}
def index(request):
    users = User.objects.all()
    result = json.dumps(list(users.values('id', 'first_name', 'last_name')))
    return HttpResponse(result, content_type='application/json')

def register(request):
    return HttpResponse(user_create(request), content_type='application/json')

def conversation(request):
    if(request.method == "GET"):
        messages = get_conversation_or_create_new(request.POST.get('sender_id'), request.POST.get('recipient_id'))
        parsed_json['messages'] = list(messages)
        parsed_json['code'] = 300
        return HttpResponse(json.dumps(parsed_json), content_type='application/json')
    else:
        return HttpResponse(error_response(), content_type='application/json')

@property
def websocket_group(self):
    return Group("conversation-%s" % self.id)

def send_message(self, message, user):
    msg = {'message': message, 'user': user.first}
    self.websocket_group.send( {'text': json.dumps(msg)})


