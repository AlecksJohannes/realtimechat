# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .models import Conversation, User, user_create, user_login
import json
from channels import Group
from .utils import get_conversation_or_create_new
from .utils import error_response
from django.forms.models import model_to_dict
from django.db.models import Q

parsed_json = {}
def index(request):
    users = User.objects.filter(Q(email = ))
    result = json.dumps(list(users.values('email')))
    return HttpResponse(result, content_type='application/json')

def register(request):
    return HttpResponse(user_create(request), content_type='application/json')
def login(request):
    return HttpResponse(user_login(request), content_type='application/json')
def conversation(request):
    if(request.method == "GET"):
        sender = User.objects.get(email = request.POST.get('sender_email'))
        recipient = User.objects.get(email = request.POST.get('recipient_email'))
        messages = get_conversation_or_create_new(sender.id, recipient.id)
        parsed_json['messages'] = list(messages)
        parsed_json['code'] = 300
        return HttpResponse(json.dumps(parsed_json), content_type='application/json')
    else:
        return HttpResponse(error_response(404), content_type='application/json')
