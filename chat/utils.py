from django.db.models import Q
import json
from rest_framework_jwt.settings import api_settings

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

def error_response(code):
    response = {}
    response['error'] = code
    response['errors'] = { 'description': 'Error page not found' }
    return json.dumps(response)
