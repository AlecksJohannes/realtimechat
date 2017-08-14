import json
from channels import Channel, Group
from channels.auth import channel_session_user_from_http, channel_session_user
from models import Message
@channel_session_user
def ws_connect(message, id):
    print("HAHAHA")
    print(id)
    print(message.user)
    message.reply_channel.send({'accept': True})
    message.channel_session['conversations'] = []
    Group('conversation-%s' % id).add(message.reply_channel)

def ws_receive(message, id):
    data = json.loads(message['text'])
    Group('conversation-%s' % id).send({
        'text': message['text'],
    })

    message = Message( conversation_id = id , body = data['text'], user_id = data['sender_id'])
    message.save()

