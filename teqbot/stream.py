import os
import subprocess as sub
from urllib.request import urlopen
from bs4 import BeautifulSoup

def now_playing(data):
    data = str(data[-1])
    data = data.replace("<td class=\"streamdata\">","")
    data = data.replace("</td>","")
    data = "#NowPlaying: " + data
    return data

def ping_stream(url,debug=False):
    # Check the Stream
    
    page = urlopen( url, timeout = 1 )

    soup = BeautifulSoup(page, 'html.parser')

    # Check to see if "streamdata" exists
    data = soup.findAll('td', attrs={"class" : "streamdata" })

    if len(data) > 0:
        if debug:
            return now_playing(data)
        return True
    else:
        return False
    

if __name__ == "__main__":
    ping = ping_stream(None, True)
    if ping:
        print(ping)
        print("Stream is UP")
    else:
        print("Stream is DOWN")