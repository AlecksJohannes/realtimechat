from channels import route
from .consumers import ws_connect, ws_receive, chat_join, chat_send

websocket_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_receive),
]

custom_routing = [
    route("chat.receive", chat_join, command="^join$"),
    route("chat.receive", chat_send, command="^send$"),
]
