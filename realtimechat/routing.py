from channels import include


# The channel routing defines what channels get handled by what consumers,
channel_routing = [
    include("chat.routing.websocket_routing", path=r'^/conversation/(?P<id>\w+)$'),
    include("chat.routing.custom_routing"),
]
