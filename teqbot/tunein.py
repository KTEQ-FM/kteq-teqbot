"""
KTEQ-FM TUNEIN API FUNCTIONS
"""

import requests

def post(sID, pID, pKey, metadata):
    #post song information to TuneIn

    #split metadata into song and artist info
    song, artist = parseMetadata(metadata)

    #build the HTTP request
    msg = "http://air.radiotime.com/Playing.ashx?partnerId=" + pID
    msg = msg + "&partnerKey=" + pKey
    msg = msg + "&id=" + sID
    msg = msg + "&title=" + song
    msg = msg + "&artist=" + artist

    #prints the HTTP request to terminal, sends out as HTTP GET request
    print("Sending HTTP GET REQUEST:", msg)
    req = requests.get(msg)



def parseMetadata(metadata):
    #Will need to devise a more sophisticated method of
    #cleaning up metadata in the future, as of
    #right now this will screw up on any song
    #with the actual word "by" in either the
    #song name or the artist name.
    #easiest solution will be to 
    #set up metadata so that the "by"
    #separator is obviously different, ie "<by>"
    #instead of just "by"
    #(This needs to be done on station computer)

    split  = metadata.split("by", 1)
    song   = split[0].rstrip().lstrip()
    artist = split[1].rstrip().lstrip()




    #get rid of NowPlaying
    fullsong = song.split("#NowPlaying: ", 1)
    if len(fullsong) > 1:
        song = fullsong[1]
    else:
        song = fullsong[0]

    #clean up the song and artist strings
    song   = song.replace(" ", "+")
    artist = artist.replace(" ", "+")

    #return song and artist pair
    return song, artist

