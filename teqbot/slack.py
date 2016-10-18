"""
KTEQ-FM SLACK API CALLS
"""

"""KTEQ-FM SLACK API CALLS.

This module contains the TeqBot class, the main component of the kteq-teqbot 
project. Several methods in this class serve as wrappers for API calls and 
other scripts in this repository. This abstraction was implemented so that 
all of the complicated logic could be separated from this module, 
allowing most of the TeqBot module to handle scheduling tasks.

Example:

        $ python slack.py "<YOUR_SLACK_WEB_API_TOKEN>"

Ordinarily, the teqbot.py module will not be run via command line. Instead, 
the module will be loaded in, allowing for an instance of the TeqBot class 
to be created. This class can run a scheduler for performing various tasks 
related to a provided IceCast music station. Current tasks involve updating 
metadata from a music stream to slack and TuneIn, as well as sending stream 
status updates to slack with diagnosis messages when the stream is not 
operating properly.

Attributes:
    STANDARD_FREQUENCY (int): default frequency in seconds for scheduler
    NOW_PLAYING (str): bitstring corresponding to now playing task
    STREAM_STATUS (str): bitstring corresponding to stream status task
    OPTION_3 (str): bitstring corresponding to placeholder task 3
    OPTION_4 (str): bitstring corresponding to placeholder task 4
    OPTION_5 (str): bitstring corresponding to placeholder task 5
    OPTION_6 (str): bitstring corresponding to placeholder task 6
    OPTION_7 (str): bitstring corresponding to placeholder task 7
    OPTION_8 (str): bitstring corresponding to placeholder task 8
    ROBOT_EMOJI (str): robot face emoji
    SKULL_EMOJI (str): skull emoji
    MUSIC_EMOJI (str): musical note emoji
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * Create the update task for automatically updating scheduler
    * Create other additional tasks as they are needed

.. _TeqBot GitHub Repository:
   https://github.com/kteq-fm/kteq-teqbot

.. _KTEQ-FM Website:
   http://www.kteq.org/

"""

import os
import sys
from slackclient import SlackClient

def get_channels(client):
    """Return a full list of channels, with all accompanying info

    Args:
        client (slackclient._client.SlackClient): SlackClient object 
            created by an API token.

    Returns:
        list: list of public slack channels, or None if fails

    Example:

        >>> import slack
        >>> from slackclient import SlackClient
        >>> token = <YOUR_SLACK_WEB_API_TOKEN>
        >>> client = SlackClient(token)
        >>> msg = slack.get_channels(client)
        >>> for i in range (0, len(msg)):
        ...   msg[i]['name']
        ... 
        <'The result is a printing of all channels for slack team'>
    """
    channels_call = client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    else:
        return None

def get_channel_id(client, channel):
    """Get A specific channel's ID, if you know its name

    Args:
        client (slackclient._client.SlackClient): SlackClient object 
            created by an API token
        channel (str): name of slack channel

    Returns:
        str: Specified channel's ID, or None if fails

    Example:

        >>> import slack
        >>> from slackclient import SlackClient
        >>> token = <YOUR_SLACK_WEB_API_TOKEN>
        >>> client = SlackClient(token)
        >>> msg = slack.get_channel_id(client, "general")
        >>> msg
        '<GENERAL_CHANNEL_ID>'
    """
    channels = get_channels(client)
    for channel in channels:
        if channel['name'] == channel:
            return channel['id']
    return None

def get_channel_name(client, channel_id):
    """Get A specific channel's name, if you have its ID.

    Args:
        client (slackclient._client.SlackClient): SlackClient object 
            created by an API token
        channel_id (str): Slack Channel ID unique to specific slack channel

    Returns:          
        str: Specified channel's name, none if fails

    Example:

        >>> import slack
        >>> from slackclient import SlackClient
        >>> token = <YOUR_SLACK_WEB_API_TOKEN>
        >>> client = SlackClient(token)
        >>> cid = slack.get_channel_id(client, "general")
        >>> msg = slack.get_channel_name(client, cid)
        >>> msg
        'general'
    """
    "Get Specific Channel Name"
    channels = get_channels(client)
    for channel in channels:
        if channel['id'] == channel_id:
            return channel['name']
    return None

def get_channel_info(client, channel_id):
    """Get A specific channel's information.

    Args:
        client (slackclient._client.SlackClient): SlackClient object 
            created by an API token
        channel_id (str): Slack Channel ID unique to specific slack channel

    Returns:
        str: Specified channel's information, None if fails

    Example:

        >>> import slack
        >>> from slackclient import SlackClient
        >>> token = <YOUR_SLACK_WEB_API_TOKEN>
        >>> client = SlackClient(token)
        >>> cid = slack.get_channel_id(client, "general")
        >>> msg = slack.get_channel_info(client, cid)
        >>> msg['purpose']['value']
        '<general channel's purpose displayed here...>'
    """
    channel_info = client.api_call("channels.info", channel=channel_id)
    if channel_info['ok']:
        return channel_info['channel']
    return None

def send_message(client, channel_id, message, username="TEQ-BOT", emoji=":robot_face:"):
    """Send a slack message to a specific channel.

    The API call for properly formatting and sending a message to 
    a public slack channel. Messages are accompanied by a username for the bot,
    as well as an emoji used as the bot's profile picture in slack.

    Please view http://www.webpagefx.com/tools/emoji-cheat-sheet/ for
    examples of valid emoji parameters.

    Args:
        client (slackclient._client.SlackClient): SlackClient object 
            created by an API token
        channel_id (str): Slack Channel ID unique to specific slack channel
        message (str): message being sent to the slack channel
        username (str): username alias for message being sent
        emoji (str): emoji used for user icon

    Returns:
            (tuple): tuple containing:

                status (bool): Status of API call
                    if stream is down.
                slack_msg (str): The message sent, or error message if call failed

    :Example:

        >>> import slack
        >>> from slackclient import SlackClient
        >>> token = <YOUR_SLACK_WEB_API_TOKEN>
        >>> client = SlackClient(token)
        >>> cid = slack.get_channel_id(client, "general")
        >>> slack_message = "Hello!"
        >>> msg = slack.send_message(client, cid, slack_message)
        >>> msg
        'User TEQ-BOT\nsent message: Hello!\n to channel #general\n with emoji :robot_face:'
    """
    call = client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username=username,
        icon_emoji=emoji
    )

    if call['ok']:
        #return value is just a message
        status = True
        channel_name = get_channel_name(client, channel_id)
        slack_msg = "User " + username + "\nsent message: " 
        slack_msg = slack_msg + message + "\n to channel #" + channel_name
        slack_msg = slack_msg + "\n with emoji " + emoji
    else:
        #return error message
        status = False
        slack_msg = "slack.send_message() error: message failed to send. | " + call['error']
    return status, slack_msg

def usage():
    """Print Usage Statement.

    Print the usage statement for running slack.py standalone.

    Returns:
        msg (str): usage statement

    Example:

        >>> import slack
        >>> msg = stream.usage()
        >>> msg
        'stream.py usage:\n$ python slack.py "<YOUR_SLACK_WEB_API_TOKEN>"'
    """
    msg = "slack.py usage:\n"
    msg = msg + "$ python slack.py \"<YOUR_SLACK_WEB_API_TOKEN>\""
    return msg
    

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        client = SlackClient( sys.argv[1] )
        channel_list = get_channels(client)
        if channel_list:
            print("List of Slack Channels")
            for channel in channel_list:
                message = channel['id'] + " : " + channel['name']
                print(message)
        else:
            print("Bad Slack API token")
    else:
        print(usage())