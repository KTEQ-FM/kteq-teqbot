import requests


def post(sID, pID, pKey, metadata):
	#post song information to TuneIn

	song, artist = parseMetadata(metadata)
	msg = "http://air.radiotime.com/Playing.ashx?partnerId=" + str(pID)
	msg = msg + "&partnerKey=" + str(pKey)
	msg = msg + "&id=" + str(sID)
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

