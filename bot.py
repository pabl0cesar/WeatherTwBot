#-*- coding: utf-8 -*-
__author__ = 'pabl0cesar'

from bs4 import BeautifulSoup
import requests, time, twitter

print("Weather on Twitter")

# CAUTION: Don't share your credentials out here...
# Keep 'em as enviroment variables like this:
# import os
# export MY_API_KEY=thisIsMyApiKey
# my_api_key = os.environ.get('MY_API_KEY', None)

api = twitter.Api(consumer_key='[your_consumer_key]',
                  consumer_secret='[your_consumer_secret]',
                  access_token_key='[your_access_token_key]',
                  access_token_secret='[your_access_token_secret]')

# Request to the web
try :
    print("\nRequesting URL...")
    # Get weather.com URL from any city (be sure to be on 'today' section)
    URL = "https://weather.com/es-AR/tiempo/hoy/l/-27.45,-58.99"
    req = requests.get(URL)
except requests.exceptions.RequestException as e :
    print("Error, Requests said: {0}.".format(e))
    
# Make a soup
html = BeautifulSoup(req.text, "html.parser")

# Define attrs with divs to scrap from web
phraseDiv = "today_nowcard-phrase"
tempDiv = "today_nowcard-temp"
feelsDiv = "today_nowcard-feels"

# Our source URL works with JS
# Requests lib don't always wait for JS to load data
# Specially on slow internet connections...
# So we're gonna assume that data is loaded and request over and over 'till it comes true :)
for tempDiv in html.find_all(attrs={"class":"today_nowcard-temp"}):
    temp = tempDiv.text
while "obs" in temp:
    req = requests.get(URL)
    html = BeautifulSoup(req.text, "html.parser")
    for tempDiv in html.find_all(attrs={"class":"today_nowcard-temp"}):
        temp = tempDiv.text
    print("JS isn't working/Slow connection, retrying...")
    
# Getting all the data
x = 1
while x > 0 :
    for phraseDiv in html.find_all(attrs={"class":"today_nowcard-phrase"}):
        phrase = phraseDiv.text
        print("\n{0}".format(phrase))
    for tempDiv in html.find_all(attrs={"class":"today_nowcard-temp"}):
        temp = tempDiv.text
        print("Temperature: {0}".format(temp))
    for feelsDiv in html.find_all(attrs={"class":"today_nowcard-feels"}):
        feels = feelsDiv.text
        #To extract only numbers
        def get_num(z):
            return int(''.join(ele for ele in z if ele.isdigit()))
        print("Feels like: {0}°".format(get_num(feels)))

    # Define a status with lastest data
    status = "{0}, Temp: {1}, Feels like: {2}°".format(phrase,temp,get_num(feels))
    
    # If weather repeats, avoid duplicate tweets error by adding a counter to status.
    statusx = "{0} x{1}".format(status, x)

    # And now let's publish status
    try:
        tweet = api.PostUpdate(status)
        x = 1
    except twitter.error.TwitterError as e:
        print("Error, twitter said: {0}".format(e))
        tweet = api.PostUpdate(statusx) 
        x += 1
    #Wait 1h to repeat this thing :)
    time.sleep(3600)
