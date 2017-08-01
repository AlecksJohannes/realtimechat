from functools import wraps
from django.db.models import Q
from .models import Conversation, Message
import json

def get_conversation_or_create_new(sender_id, recipient_id):
    try:
        conversation = Conversation.objects.get(
            Q(sender_id = sender_id, recipient_id = recipient_id)
            | Q(sender_id = recipient_id, recipient_id = sender_id))

        messages = Message.objects.filter(Q(conversation_id = conversation.id)).values('body', 'is_read')
        return messages
    except Conversation.DoesNotExist:
        conversation = Conversation(sender_id = sender_id, recipient_id = recipient_id)
        conversation.save()
        return conversation


def error_response():
    response = {}
    response['error'] = 404
    response['errors'] = { 'description': 'Error page not found' }
    return json.dumps(response)
