import sys
from slackclient import SlackClient
import os
from teq import TeqBot

def usage():
    usage = "\n\n"
    usage = usage + "===============\n"
    usage = usage + "KTEQ-FM TEQ-BOT\n"
    usage = usage + "===============\n\n"
    usage = usage + "=======================================\n"
    usage = usage + "By J. Anthony Brackins & Jonathan Dixon\n"
    usage = usage + "=======================================\n\n"
    usage = usage + "Requirements:\n"
    usage = usage + "Python3\n"
    usage = usage + "slackclient python library\n"
    usage = usage + "Slack API Token\n\n"    
    usage = usage + "Usage:\n"
    usage = usage + "python3 teqbot <command>\n\n"
    usage = usage + "Commands:\n\n"
    usage = usage + "\tusage         \t\tPrint Usage statement\n"
    usage = usage + "\tmessage <text>\t\tSend a test message to #boondoggling channel\n"
    return usage + "\n"

def command_handler(args):
    'check what command line argument was handled'
    args[0] = args[0].upper()
    #handle MESSAGE command:
    if args[0] == "USAGE":
        # Print Usage Statement
        print( usage() )
    if args[0] == "MESSAGE":
        if len(args) > 1:
            # Send whatever message you enter as command line args
            msg = " ".join(args[1:])
            print( "Sending \'" + msg + "\' to #boondoggling channel..." )
            print( test_slack_message( msg ) )

#simply prints some channel info, then sends message to #boondoggling
def test_slack_message(message="Hello World!"):
    channels = teq.get_channels()
    if channels:
        for channel in channels:
            #send a message to boondoggling
            if channel['name'] == 'boondoggling':
                teq.set_channel(channel['id'])
                teq.set_message(message)
                teq.send_message()
                return "Message Sent."
    else:
        return "Unable to authenticate."

# get system arguments
teq = TeqBot()
args = sys.argv
if len(args) > 1:
    command_handler( args[1:] )
else:
    print( usage() )

