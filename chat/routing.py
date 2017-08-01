from channels import route
from .consumers import ws_connect, ws_receive

websocket_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_receive),
]

custom_routing = [
]
