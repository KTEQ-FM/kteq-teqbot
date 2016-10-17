"""
KTEQ-FM SLACK API CALLS
"""

import os
import sys
from slackclient import SlackClient

def get_channels(client):
    """Return a full list of channels, with all accompanying info

    :param client:     SlackClient object created by an API token

    :type client:      slackclient._client.SlackClient

    :returns:          channels_call['channels']: A slack channels
    :rtype:            <class 'list'>

    :Example:

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

    :param client:     SlackClient object created by an API token
    :param channel:    name of slack channel

    :type client:      slackclient._client.SlackClient
    :type channel:     string

    :returns:          channel['id']: Specified channel's ID
    :rtype:            string

    :Example:

    >>> import slack
    >>> from slackclient import SlackClient
    >>> token = <YOUR_SLACK_WEB_API_TOKEN>
    >>> client = SlackClient(token)
    >>> msg = slack.get_channel_id(client, "general")
    >>> msg
    '<GENERAL_CHANNEL_ID>'
    """
    "Get Specific Channel ID"
    channels = get_channels(client)
    for channel in channels:
        if channel['name'] == channel:
            return channel['id']
    return None

def get_channel_name(client, channel_id):
    """Get A specific channel's name, if you have its ID.

    :param client:     SlackClient object created by an API token
    :param channel_id: Slack Channel ID unique to specific slack channel

    :type client:      slackclient._client.SlackClient
    :type channel_id:  string

    :returns:          channel['name']: Specified channel's name
    :rtype:            string

    :Example:

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

    :param client:     SlackClient object created by an API token
    :param channel_id: Slack Channel ID unique to specific slack channel

    :type client:      slackclient._client.SlackClient
    :type channel_id:  string

    :returns:          channel_info['channel']: Specified channel's information
    :rtype:            string

    :Example:

    >>> import slack
    >>> from slackclient import SlackClient
    >>> token = <YOUR_SLACK_WEB_API_TOKEN>
    >>> client = SlackClient(token)
    >>> cid = slack.get_channel_id(client, "general")
    >>> msg = slack.get_channel_info(client, cid)
    >>> msg['purpose']['value']
    'This channel is for team-wide communication and announcements. All team members are in this channel.'
    """
    channel_info = client.api_call("channels.info", channel=channel_id)
    if channel_info['ok']:
        return channel_info['channel']
    return None

def send_message(client, channel_id, message, username="TEQ-BOT", emoji=":robot_face:"):
    """Send a slack message to a specific channel.

    please view http://www.webpagefx.com/tools/emoji-cheat-sheet/ for
    examples of valid emoji parameters.

    :param client:     SlackClient object created by an API token
    :param channel_id: Slack Channel ID unique to specific slack channel
    :param message:    message being sent to slack channel
    :param username:   username alias for message being sent
    :param emoji:      emoji used for user icon

    :type client:      slackclient._client.SlackClient
    :type channel_id:  string
    :type message:     string
    :type username:    string
    :type emoji:       string

    :returns:          status, slack_msg: Status of api call, msg sent / error msg
    :rtype:            boolean, string

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

    :returns: msg: Usage Statement
    :rtype: string

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