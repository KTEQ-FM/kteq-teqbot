import os
from slackclient import SlackClient

def get_channels(client):
    "List All Channels"
    channels_call = client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    else:
        return None

def get_channel_id(client, channel):
    "Get Specific Channel ID"
    channels = get_channels(client)
    for c in channels:
        if c['name'] == channel:
            return c['id']
    return None

def get_channel_info(client, channel_id):
    "Get Channel Info"
    channel_info = client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None

def send_message(client, channel_id, message, username="TEQ-BOT", emoji=":robot_face:"):
    "Send a message to a specific channel"
    client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username=username,
        icon_emoji=emoji
    )