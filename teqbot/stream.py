"""
KTEQ-FM STREAM STATUS FUNCTIONS
"""

import sys
from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup

#potential stream errors
NO_DATA   = "no data read from Icecast Server"
URL_ERROR = "HTTP Request Timeout"

#how long to wait for timeout
TIMEOUT_VALUE = 60

def prep_message(cause="None"):
    """returns message

    Prepare a message to be generated and sent to the 
    slack channel designated for reporting stream incidents.
    The current incidents teq-bot can report on are:

    NO_DATA:   Icecast server is up, but no data is being output
               to it. This usually means that the stream is
               up, but Altacast encoders are not connected.
    URL_ERROR: Icecast is either down, or HTTP request simply
               simply timed out. Technically this happens
               purely because the HTTP request times out. 
               This can occur accidentally if internet speeds 
               happen to be slow at the time. However, 
               they can also mean that the timeout occurs 
               because the Icecast page isn't up at all.

    :param cause: the error that explains how the stream is down
    :type cause: string
    :returns: message
    :rtype: string

    :Example:

    >>> import stream
    >>> msg = stream.prep_message(stream.NO_DATA)
    >>> msg
    <Prints stream error message for NO_DATA case>

    .. warning:: failing to supply cause param returns unknown error.
    .. todo:: add any additional error types encountered.
    """
    msg = "ALERT!! STREAM IS DOWN!!\n"
    msg = msg + "Likely cause: \n"
    if cause == NO_DATA:
        msg = msg + "No data read from Icecast server. \n"
        msg = msg + "This at least means the computer is on, "
        msg = msg + "and icecast is running, but the altacast "
        msg = msg + "encoders aren't hooked up properly. This "
        msg = msg + "most often happens when someone boots up "
        msg = msg + "multiple instances of altacast on the station "
        msg = msg + "computer. I would start with looking at that."
    elif cause == URL_ERROR:
        msg = msg + "HTTP Request Timeout. \n"
        msg = msg + "This could mean a multitude of things. "
        msg = msg + "Right off the bat, we know that icecast is "
        msg = msg + "acting off. This could be from the following "
        msg = msg + "problems: \n"
        msg = msg + "1) icecast has been closed on the computer\n"        
        msg = msg + "2) multiple instances of icecast are running\n"
        msg = msg + "3) the station computer has lost internet access\n"
        msg = msg + "4) the station computer is rebooting\n"
        msg = msg + "5) the station computer is off, either from "
        msg = msg + "shutting down or from crashing.\n\n"
        msg = msg + "When diagnosing this issue, please check on AltaCast "
        msg = msg + "as well, because that could also possibly be down.\n"
    else:
        msg = msg + "Unknown Error!!! \n"
        msg = msg + "This should have never happened. "
        msg = msg + "I have no idea what is wrong. I'm truly sorry.\n"
        msg = msg + "Just sit things out for a bit and and everything will "
        msg = msg + "be fine before long.\n"
    return msg

def now_playing(data):
    """returns data

    Clean up a portion of HTML that contains the data for
    whatever song is currently broadcasting on an IceCast 
    stream.

    Once the song is identified in the message, a #NowPlaying 
    tag is added to it to identify the returned data as a 
    successful song ID.

    Full HTML example for KTEQ.ORG stream:
        [<td class="streamdata">KTEQ-FM</td>, 
        <td class="streamdata">91.3FM</td>, 
        <td class="streamdata">audio/mpeg</td>, 
        <td class="streamdata">
            Sun, 02 Oct 2016 13:33:52 Mountain Daylight Time
        </td>, 
        <td class="streamdata">192</td>, 
        <td class="streamdata">1</td>, 
        <td class="streamdata">6</td>, 
        <td class="streamdata">Alternative</td>, 
        <td class="streamdata">
            <a href="http://www.kteq.org/" target="_blank">http://www.kteq.org/</a>
        </td>, 
        <td class="streamdata">Beat Market by Sun Machine</td>, 
        <td class="streamdata">KTEQ-FM</td>, 
        <td class="streamdata">91.3FM</td>, 
        <td class="streamdata">audio/mpeg</td>, 
        <td class="streamdata">
            Sun, 02 Oct 2016 13:33:53 Mountain Daylight Time
        </td>, <td class="streamdata">96</td>, 
        <td class="streamdata">0</td>, 
        <td class="streamdata">4</td>, 
        <td class="streamdata">Alternative</td>, 
        <td class="streamdata">
            <a href="http://www.kteq.org/" target="_blank">http://www.kteq.org/</a>
        </td>, <td class="streamdata">Beat Market by Sun Machine</td>, 
        <td class="streamdata">KTEQ-FM</td>, 
        <td class="streamdata">91.3FM</td>, 
        <td class="streamdata">audio/mpeg</td>, 
        <td class="streamdata">
            Sun, 02 Oct 2016 13:33:54 Mountain Daylight Time
        </td>, 
        <td class="streamdata">128</td>, 
        <td class="streamdata">1</td>, 
        <td class="streamdata">6</td>, 
        <td class="streamdata">Alternative</td>, 
        <td class="streamdata">
            <a href="http://www.kteq.org/" target="_blank">http://www.kteq.org/</a>
        </td>, 
        <td class="streamdata">Beat Market by Sun Machine</td>]

    The crawler grabs this entire html segment, the only part needed is 
    the very last value in this list, which contains the song information.
    
    (In the case of KTEQ's Stream, there appear to be several duplicates.
    This is due to the fact that the kteq station has 3 encodings
    192kbps, 96kbps, 128kbps respectively. It is easiest to just
    grab the last encoding's song info, as they should all be the
    same and this method should work for any number of encodings
    on a given server.)

    :param data: HTML segment containing song information
    :type cause: string
    :returns: data: cleaned data string, containing just song info 
    :rtype: string

    :Example:

    >>> import stream
    >>> from urllib.request import urlopen
    >>> import urllib.error
    >>> from bs4 import BeautifulSoup
    >>> url  = <YOUR_STREAM_URL_HERE>
    >>> page = urlopen( url, timeout=60 )
    >>> soup = BeautifulSoup(page, 'html.parser')
    >>> data = soup.findAll('td', attrs={"class" : "streamdata" })
    >>> msg  = stream.now_playing(data)
    >>> msg
    '#NowPlaying Beat Market by Sun Machine'
    """

    # The very last <td> tagged value is the one we want. (contains song)
    data = str(data[-1])

    # get rid of html tags
    data = data.replace("<td class=\"streamdata\">","")
    data = data.replace("</td>","")

    # add '#NowPlaying: ' to the beginning of song information
    data = "#NowPlaying: " + data
    return data

def ping_stream(url,debug=False):
    """returns stream_status, message

    perform an HTTP request to copy all html data from an Icecast
    Stream. 

    If html data was successfullly retrieved:
        find all html tags labeled 'td' with attribute 'class=streamdata'
        if data was found:
            clean up the data to retrieve song information
            report that the stream is up, return song information
        if data was not found:
            report that the stream is down, return NO_DATA error message
    If HTTP request times out, resulting in no html data:
        report that the stream is down, return URL_ERROR error message

    This function uses the BeautifulSoup library for html parsing and
    urllib library to perform an HTTP request. After a successful HTTP request,
    the function parses the html retrieved from the stream's site. This 
    returns all of the html used for the site, which is pruned down to 
    instances of <td>, or table, tags in the site's html. In particular, this 
    pruning is done on <td> tags that have been labeled with the class "streamdata".
    While several of these cells contain other information about the stream, such 
    as bitrate, number of current listeners, station name, etc., the last cell 
    contains information about the currently playing song on the station as 
    long as icecast is pushing out metadata containing such information.

    If the http request fails to return any streamdata at all, this means that 
    while the Icecast page is up, there are no encoders being broadcasted.

    If the http request fails after the timeout threshold, this means that the 
    Icecast page is possibly down.

    :param url:   Online stream url
    :param debug: Optional flag for debugging outputs (unused)

    :type url: string
    :type debug: boolean

    :returns: stream_status, message: status of stream (true=up), message payload
    :rtype: boolean, string

    :Example:

    >>> import stream
    >>> url  = <YOUR_STREAM_URL_HERE>
    >>> msg = stream.ping_stream(url)
    >>> msg
    (True, '#NowPlaying: I Think I Smell a Rat by The White Stripes')
    """

    # Check the Stream
    try:
        # Try to access the page for 60 seconds
        page = urlopen( url, timeout=TIMEOUT_VALUE )
        soup = BeautifulSoup(page, 'html.parser')

        # Check to see if "streamdata" exists
        data = soup.findAll('td', attrs={"class" : "streamdata" })

        if len(data) > 0:
            # Stream is up, and retrieved current song data
            return True, now_playing(data)
        else:
            # IceCast Server is up, Altacast isn't.
            return False, prep_message(NO_DATA)
    except urllib.error.URLError:
        # http request timed out after 60 seconds
        # IceCast Server not set up, Altacast might also be down.
        return False, prep_message(URL_ERROR)

def usage():
    """returns msg

    Print the usage statement for running stream.py standalone.

    :returns: msg: Usage Statement
    :rtype: string

    >>> import stream
    >>> msg = stream.usage()
    >>> msg
    'stream.py usage:\n$ python stream.py "<YOUR_STREAM_URL>"'
    """
    msg = "stream.py usage:\n"
    msg = msg + "$ python stream.py \"<YOUR_STREAM_URL>\""
    return msg
    

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        ping, message = ping_stream(sys.argv[1], True)
        if ping:
            print("Station is online")
        else:
            print("Station is offline")
        print(message)
    else:
        print(usage())