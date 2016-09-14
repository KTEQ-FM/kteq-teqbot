"""
KTEQ-FM TEQBOT CLASS
"""

from slackclient import SlackClient
import os
import api

class TeqBot:
    def __init__(self):
        SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
        self.slack = SlackClient(SLACK_TOKEN)
        self.username = 'TEQ-BOT'
        self.emoji    = ':robot_face:'
        self.channel = None
        self.message = ""

    def set_emoji(self, emojiName):
        'change TeqBot emoji'
        self.emoji = emojiName
    
    def set_channel(self, channel_id):
        'set the channel id for TeqBot'
        self.channel = channel_id

    def set_message(self, message):
        'set the message for TeqBot before sending'
        self.message = message

    def get_channels(self):
        'get the list of channels'
        return api.get_channels(self.slack)

    def get_channel_info(self):
        'return channel info'
        return api.get_channel_info(self.slack, self.channel)

    def print_channel_list(self):
        channels = self.get_channels()
        if channels:
            print("KTEQ-MGMT Channel List:")
            for channel in channels:
                #ch_id = channel['id']
                #self.set_channel(ch_id)
                print("    #" + channel['name'] + " (" + channel['id'] + ")")

    def send_message(self):
        'send a predetermined message to TeqBots current channel'
        api.send_message(self.slack, self.channel, self.message, self.username, self.emoji)
