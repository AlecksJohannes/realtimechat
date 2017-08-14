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
from django.views.decorators.http import require_http_methods

parsed_json = {}

def index(request):
    users = User.objects.exclude(id = request.GET.get('id'))
    result = json.dumps(list(users.values('username')))
    return HttpResponse(result, content_type='application/json')

def register(request):
    return HttpResponse(user_create(request), content_type='application/json')

@require_http_methods(['POST'])
def login(request):
    return HttpResponse(user_login(request), content_type='application/json')


@require_http_methods(['POST'])
def conversation(request):
    sender = User.objects.get(username = request.POST.get('sender_email'))
    recipient = User.objects.get(username = request.POST.get('recipient_email'))
    conversation_data = get_conversation_or_create_new(sender.id, recipient.id)
    parsed_json['conversation'] = conversation_data
    parsed_json['code'] = 302
    return HttpResponse(json.dumps(parsed_json), content_type='application/json')
