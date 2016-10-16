import requests


def post(sID, pID, pKey, metadata):
	#post song information to TuneIn

	song, artist = parseMetadata(metadata)
	msg = "http://air.radiotime.com/Playing.ashx?partnerId=" + pID
	msg = msg + "&partnerKey=" + pKey
	msg = msg + "&id=" + sID
	msg = msg + "&title=" + song
	msg = msg + "&artist=" + artist
	req = requests.get(msg)



def parseMetadata(metadata):
	split  = metadata.split("by", 1)
	song   = split[0]
	artist = split[1]

	#clean up the song and artist strings
	song   = song.replace(" ", "+")
	artist = artist.replace(" ", "+")

	return song, artist

