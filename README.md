# teq-bot
TEQ-Bot: KTEQ-FM bot for monitoring stream status, current song playing, and equipment pinging.

# Author
* <a href="http://julianbrackins.me/" target="_blank">J. Anthony Brackins</a> - KTEQ Station Programming Manager

# Steps for Configuring This project:
* install python 3
* install slackclient library for python 3

        $ pip install slackclient

* install beautifulsoup4 for python 3

        $ pip install beautifulsoup4

* add the following environment variable exports to your ~/.profile:

        $ export SLACK_TOKEN='your_slack_token'
        $ export STREAM_URL='your_online_stream_url'
        $ export PYTHONPATH='path_to_python3'
        $ export TUNEIN_STATION_ID='your_tunein_station_id'  
        $ export TUNEIN_PARTNER_ID='your_tunein_partner_id'  
        $ export TUNEIN_PARTNER_KEY='your_tunein_partner_key'

# Usage:
        $ python3 teqbot <command> [options]

        Commands:

	        usage             		Print Usage statement
        	scheduler         		Run the scheduler that handles calling each task
        	task              		Run an individual scheduler task

        Scheduler Options:

        	-n, --nowplaying  		Start Up Nowplaying messages to slack
        	-s, --status      		Check the status of the stream

        Test Commands:
        
        	kill          		Send a message to stop the scheduler
        	message <text>		Send a test message to #boondoggling channel

# <a href="http://kteq.org" target="_blank">About KTEQ</a>

Established in 1971, KTEQ is the South Dakota School of Mines and Technology student-run, non-profit alternative radio station. The only rule KTEQ has about music, is that it cannot be Top 40 (the stuff played on 99.99% of radio). 

The DJs set their own playlists, ranging from metal, rap, rock, oldies, techno, country...etc.  

Currently, KTEQ broadcasts on 91.3 FM, internet streaming on KTEQ.ORG, and via <a href="http://tunein.com/radio/KTEQ-FM-913-s144657/" target="_blank">Tunein.com</a>.

