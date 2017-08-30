import json
from channels import Group
from channels.sessions import channel_session
from urllib.parse import parse_qs
import logging

log = logging.getLogger('www')

# Connected to websocket.connect
@channel_session
def ws_connect(message, room_name=None):
    log.info('ws_connect')
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Parse the query string
    params = parse_qs(message.content["query_string"])
    log.info('params %s' % params)
    if b"username" in params:
        # Set the username in the session
        message.channel_session["username"] = params[b"username"][0].decode("utf8")
        # Add the user to the room_name group
        Group("chat-%s" % room_name).add(message.reply_channel)
    else:
        # Close the connection.
        message.reply_channel.send({"close": True})

# Connected to websocket.receive
@channel_session
def ws_message(message, room_name=None):
    log.info('ws_message')
    log.info('room name  message %s' % room_name)
    if room_name:
        Group("chat-%s" % room_name).send({
            "text": json.dumps({
                "text": message["text"],
                "username": message.channel_session["username"] if message.channel_session.get("username") else "Anon",
            }),
        })
    else:
        Group("chat").send({
            "text": "[user] %s" % message.content['text'],
        })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message, room_name=None):
    if room_name:
        Group("chat-%s" % room_name).discard(message.reply_channel)
    else:
        Group("chat").discard(message.reply_channel)

def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("chat").add(message.reply_channel)
