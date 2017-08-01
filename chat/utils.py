from functools import wraps
from django.db.models import Q
from .models import Conversation, Message
import json


def get_conversation_or_create_new(sender_id, recipient_id):
    try:
        conversation = Conversation.objects.get(
            Q(sender_id_id = sender_id, recipient_id_id = recipient_id)
            | Q(sender_id_id = recipient_id, recipient_id_id = sender_id))

        messages = Message.objects.filter(Q(conversation_id = conversation.id))
        return messages
    except Conversation.DoesNotExist:
        conversation = Conversation
        return conversation


def error_response():
    response = {}
    response['error'] = 404
    response['errors'] = { 'description': 'Error page not found' }
    return json.dumps(response)
