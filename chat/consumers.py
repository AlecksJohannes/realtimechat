from channels.auth import channel_session_user_from_http
import json
from channels import Channel


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({'accept': True})
    message.channel_session['conversations'] = []


def ws_receive(message):
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel('chat.receive').send(playload)

def chat_join(message):
    conversation = get_conversation_or_error(1, message.user)
    conversation.websocket_group.add(message.reply_channel)
    message.channel_session['conversations'] = list(set(message.channel_session['conversations']).union([conversation.id]))
    message.reply_channel.send({
        'text': json.dumps({
            'join': str(conversation.id),
        }),
    })

def chat_send(message):
    conversation = get_conversation_or_error(message['conversation'], message.user)
    conversation.send_message(message['message'], message.user)
