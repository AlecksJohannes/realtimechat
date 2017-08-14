from django.db.models import Q
import json
from rest_framework_jwt.settings import api_settings

def get_conversation_or_create_new(sender_id, recipient_id):
    from models import Conversation, Message
    conversation_json = {}
    try:
        conversation = Conversation.objects.get(
            Q(sender_id = sender_id, recipient_id = recipient_id)
            | Q(sender_id = recipient_id, recipient_id = sender_id))

        messages = Message.objects.filter(Q(conversation_id = conversation.id)).values('body', 'is_read', 'user_id').order_by('created_at')
        conversation_json['messages'] = list(messages)
        conversation_json['conversation_id'] = conversation.id
        return conversation_json
    except Conversation.DoesNotExist:
        conversation = Conversation(sender_id = sender_id, recipient_id = recipient_id)
        conversation.save()
        conversation_json['conversation_id'] = conversation.id
        return conversation_json

def error_response(code):
    response = {}
    response['error'] = code
    response['errors'] = { 'description': 'Error page not found' }
    return json.dumps(response)

