# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .models import Conversation
import json
from channels import Group
from .utils import get_conversation_or_create_new
from .utils import error_response


def index(request):
    conversation = get_conversation_or_create_new(1, 2)
    print(conversation.recipient_id_id)
    result = json.dumps(conversation)
    return HttpResponse(result, content_type='application/json')

def conversation(request):
    parsed_json = {}
    if(request.method == "POST"):
        messages = get_conversation_or_create_new(request.POST.get('sender_id'), request.POST.get('recipient_id'))
        parsed_json['messages'] = list(messages)
        parsed_json['code'] = 300
        return HttpResponse(json.dumps(parsed_json), content_type='application/json')
    else:
        response = error_response()
        return HttpResponse(response, content_type='application/json')

@property
def websocket_group(self):
    return Group("conversation-%s" % self.id)

def send_message(self, message, user):
    msg = {'message': message, 'user': user.first}
    self.websocket_group.send( {'text': json.dumps(msg)})


