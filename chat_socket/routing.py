from channels.routing import route

from chat.consumers import ws_connect, ws_message, ws_disconnect, ws_add

channel_routing = [
    # route("websocket.connect", ws_add),
    # route("websocket.receive", ws_message),
    # route("websocket.disconnect", ws_disconnect),
    route("websocket.connect", ws_connect, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.receive", ws_message, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.disconnect", ws_disconnect, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
]
