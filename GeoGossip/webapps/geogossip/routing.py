from channels.routing import route
from geogossip.consumer import connect, receive, disconnect


channel_routing = [
    route("websocket.connect", connect),
    route("websocket.receive", receive),
    route("websocket.disconnect", disconnect),
]
