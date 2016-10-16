"""
KTEQ-FM TEQBOT CLASS
"""

from slackclient import SlackClient
import os
import time
import api
import stream
import tunein
import shlex
import subprocess

NOW_PLAYING   = '00000001'
STREAM_STATUS = '00000010'
OPTION_3 = '00000100'
OPTION_4 = '00001000'
OPTION_5 = '00010000'
OPTION_6 = '00100000'
OPTION_7 = '01000000'
OPTION_8 = '10000000'


ROBOT_EMOJI = ':robot_face:'
SKULL_EMOJI = ':skull:'
MUSIC_EMOJI = ':musical_note:'

class TeqBot:
    def __init__(self):
        self.slack = SlackClient( os.environ.get('SLACK_TOKEN') )
        self.stream = os.environ.get('STREAM_URL')
        self.python = os.environ.get('PYTHONPATH')
        self.tuneinStationID  = os.environ.get('TUNEIN_STATION_ID')
        self.tuneinPartnerID  = os.environ.get('TUNEIN_PARTNER_ID')
        self.tuneinPartnerKey = os.environ.get('TUNEIN_PARTNER_KEY')
        self.username = 'TEQ-BOT'
        self.emoji    = ROBOT_EMOJI
        self.channel = None
        self.message = ""
        self.lastSong = ""

    def scheduler(self, event='11111111', frequency=60):
        # reset some flags
        clock = 0
        self.set_last_played("None")
        self.set_stat_file("Running")
        self.get_last_played()
        while True:
            if clock % frequency == 0:
                nowPlaying = int( "{0:b}".format( int( event, 2) & int(NOW_PLAYING, 2) ) )
                if nowPlaying:
                    print("Handling NowPlaying Status...")
                    self.spawn_task(self.python + " teqbot task --nowplaying")
                streamStatus = int(  "{0:b}".format( int( event, 2) & int(STREAM_STATUS, 2) ) )
                if streamStatus:
                    print("Handling Stream Status...")
                    self.spawn_task(self.python + " teqbot task --status")
                clock = 0
            clock = clock + 1
            #print("Sleep for", abs(clock - frequency) + 1, "Seconds...")
            time.sleep(1)
            if self.check_stat_file("Done"):
                self.delete_stat_file()
                break
        print("Finished Scheduler")

    def run(self, debug=False):
        'run TeqBot for a while'
        self.set_last_song( self.get_now_playing() )
        print( "Song:" , self.lastSong )
        while True:

            #Updating Song
            self.task_now_playing()

            #Checking Stream Status
            self.task_stream_status()

            if debug:
                print("Wait 30 seconds")
            time.sleep(30)


    def spawn_task(self, command):
        'Spawn a new task'
        # can be made way more complex to handle more stuff
        args = shlex.split(command)
        p = subprocess.Popen(args)

    def task_now_playing(self):
        #Updating Song
        self.get_last_played()
        print("Comparing", self.lastSong, "|", self.get_now_playing() )
        newsong = self.check_last_played()
        if newsong:
            print("New Song")
            self.teq_message(self.lastSong, "nowplaying", MUSIC_EMOJI)
            #post metadata to TuneIn
            self.teq_tunein(self.lastSong)
        else:
            print("Same Song")

    def task_stream_status(self):
        online, msg = self.ping_stream()
        if online:
            # Only do something if the stream HAD been down
            # If this is the case, then let everyone know
            # We are back online
            if self.check_stat_file("Stream Down"):
                self.set_stat_file("Running")
                msg = "The Stream is Back Online!"
                print(msg)
                self.teq_message(msg, "emergency", ROBOT_EMOJI )
            else:
                print("Stream is Online")

        else:
            print(msg)
            self.teq_message(msg, "emergency", SKULL_EMOJI )
            self.set_stat_file("Stream Down")

    def task_update_repo(self):
        print("Update Repository")

    def teq_message(self, message, channel, emoji):
        'set emoji and prepare a message, send'
        self.set_emoji(emoji)
        self.set_message(message)
        self.set_channel(channel)
        self.send_message()
        self.set_message(ROBOT_EMOJI)

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
        ping, message = stream.ping_stream(self.stream)
        return message

    def ping_stream(self):
        'returns True if stream is up, False if stream is down'
        ping, message = stream.ping_stream(self.stream)
        return ping, message

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


    def set_last_played(self, song):
        f = open('.teq.song', 'w')
        f.write(song)

    def get_last_played(self):
        if os.path.exists('.teq.song'):
            f = open('.teq.song', 'r')
            self.lastSong = f.read()
        else:
            self.lastSong = ""

    def check_last_played(self):
        if os.path.exists('.teq.song'):
            f = open('.teq.song', 'r')
            check = self.get_now_playing()
            song = f.read()
            if song == "None":
                self.set_last_song( check )
                self.set_last_played( check )
                return True

            elif check != song:
                # New Song
                self.set_last_song( check )
                self.set_last_played( check )
                return True

            else:
                return False
        else:
            return False

    def set_stat_file(self, status):
        f = open('.teq.stat', 'w')
        f.write(status)

    def check_stat_file(self, check):
        if os.path.exists('.teq.stat'):
            f = open('.teq.stat', 'r')
            stat = f.read()
            return check == stat
        else:
            return False

    def delete_stat_file(self):
        if os.path.exists('.teq.stat'):
            os.remove('.teq.stat')

    def tunein(self, metadata):
        #post metadata to TuneIn afterformatting
        tunein.post( self.tuneinStationID, self.tuneinPartnerID, self.tuneinPartnerKey metadata)





