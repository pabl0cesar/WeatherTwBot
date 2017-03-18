# Weather Bot for Twitter
A simple python bot.
<br>It gets data from a weather website and publish hourly on Twitter.

There are a few libs <b>needed</b> and you can install them using pip:		 

		pip install requests
		pip install beautifulsoup4
		pip install python-twitter
		
You have to register a Twitter App (https://apps.twitter.com/app/new), in order to get the OAuth credentials and replace these values in the code:

		api = twitter.Api(consumer_key='[your_consumer_key]',
                  consumer_secret='[your_consumer_secret]',
                  access_token_key='[your_access_token_key]',
                  access_token_secret='[your_access_token_secret]')
									
You'll want a fresh Twitter account for this, though you could have it post to one you already own :)

From http://weather.com you can get any city URL (just be sure to be on 'today' section) and replace the URL value in the code.
