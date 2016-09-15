"""
KTEQ-FM TEQBOT CLASS
"""

from slackclient import SlackClient
import os
import time
import api
import stream

class TeqBot:
    def __init__(self):
        #print(os.environ.get('SLACK_TOKEN'))
        self.slack = SlackClient( os.environ.get('SLACK_TOKEN') )
        #print(self.slack)
        self.stream = os.environ.get('KTEQ_STREAM_URL')
        self.username = 'TEQ-BOT'
        self.emoji    = ':robot_face:'
        self.channel = None
        self.message = ""
        self.lastSong = ""

    def run(self, debug=False):
        'run TeqBot for a while'
        self.set_last_song( self.get_now_playing() )
        print( "Song:" , self.lastSong )
        while True:

            #Updating Song
            if debug:
                print("Comparing", self.lastSong, "|", self.get_now_playing() )
            newsong = self.compare_songs()
            if newsong:
                if debug:
                    print("New Song")
                self.set_emoji(':musical_note:')
                self.set_message(self.lastSong)
                self.set_channel("nowplaying")
                self.send_message()
                self.set_emoji(':robot_face:')
            else:
                if debug:
                    print("Same Song")

            #Checking Stream Status
            online = self.ping_stream()
            if online:
                if debug:
                    print("Stream is up")
            else:
                if debug:
                    print("!!ALERT!! STREAM IS DOWN!!")
                self.set_emoji(':skull:')
                self.set_message("RED ALERT! STREAM IS DOWN!!")
                self.set_channel("emergency")
                self.send_message()
                self.set_emoji(':robot_face:')
            if debug:
                print("Wait 30 seconds")
            time.sleep(30)


    def set_emoji(self, emojiName):
        'change TeqBot emoji'
        self.emoji = emojiName
    
    def set_channel(self, channel):
        'set the channel id for TeqBot'
        self.channel = api.get_channel_id(self.slack, channel)

    def set_last_song(self, song):
        self.lastSong = song

    def set_message(self, message):
        'set the message for TeqBot before sending'
        self.message = message

    def get_channels(self):
        'get the list of channels'
        return api.get_channels(self.slack)

    def get_channel_info(self):
        'return channel info'
        return api.get_channel_info(self.slack, self.channel)

    def get_now_playing(self):
        'returns current song being played.'
        return stream.ping_stream(self.stream, True)

    def ping_stream(self):
        'returns True if stream is up, False if stream is down'
        return stream.ping_stream(self.stream)

    def compare_songs(self):
        'check if this is a new song'
        check = self.get_now_playing()
        if self.lastSong != check:
            #new song
            self.set_last_song( check )
            return True
        else:
            #same song
            return False

    def print_channel_list(self):
        channels = self.get_channels()
        if channels:
            print("KTEQ-MGMT Channel List:")
            for channel in channels:
                print("    #" + channel['name'] + " (" + channel['id'] + ")")

    def send_message(self):
        'send a predetermined message to TeqBots current channel'
        api.send_message(self.slack, self.channel, self.message, self.username, self.emoji)
        #clear the message afterwards
        self.set_message("")






