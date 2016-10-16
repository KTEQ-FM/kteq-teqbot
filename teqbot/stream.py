import os
import subprocess as sub
from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup

def prep_message(cause):
    msg = "ALERT!! STREAM IS DOWN!!\n"
    msg = msg + "Likely cause: \n"
    if cause == "NO_DATA":
        msg = msg + "No data read from Icecast server. \n"
        msg = msg + "This at least means the computer is on, "
        msg = msg + "and icecast is running, but the altacast "
        msg = msg + "encoders aren't hooked up properly. This "
        msg = msg + "most often happens when someone boots up "
        msg = msg + "multiple instances of altacast on the station "
        msg = msg + "computer. I would start with looking at that."
    elif cause == "URL_ERROR":
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
    return msg

def now_playing(data):
    data = str(data[-1])
    data = data.replace("<td class=\"streamdata\">","")
    data = data.replace("</td>","")
    data = "#NowPlaying: " + data
    return data

def ping_stream(url,debug=False):
    # Check the Stream
        
    try:
        # Try to access the page for 10 seconds
        page = urlopen( url, timeout=10 )
        soup = BeautifulSoup(page, 'html.parser')

        # Check to see if "streamdata" exists
        data = soup.findAll('td', attrs={"class" : "streamdata" })

        if len(data) > 0:
            # Stream is up, and retrieved current song data
            return True, now_playing(data)
        else:
            # IceCast Server is up, Altacast isn't.
            message = prep_message("NO_DATA")
            return False, message
    except urllib.error.URLError:
        # http request timed out after 15 seconds
        # IceCast Server not set up, Altacast might also be down.
        message = prep_message("URL_ERROR")
        return False, message


    

if __name__ == "__main__":
    ping, message = ping_stream(os.environ.get('STREAM_URL'), True)
    if ping:
        print(message)
    else:
        print(message)