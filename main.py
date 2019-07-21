import twitter
import config
import datetime
import json as JSON
import os

def log(text=""):
    date = datetime.datetime.now()
    filename = config.LOG_PATH+str(date.year)+'_'+str(date.month)+'_'+str(date.day)

    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file = open(filename, "w+")
    else:
        file = open(filename, "a+")

    file.write(str(date.hour)+':'+str(date.minute)+':'+str(date.second)+' | '+text)
    file.close()

def Follow(post):
    text = post.text

    if "follow" in text.lower():
        try:
            api.CreateFriendship(user_id=post.user.id)
            log("success: follow user : "+post.user.screen_name)
        except:
            log("error: cannot follow user : "+post.user.screen_name)

def Retweet(post):
    text = post.text

    if ["rt", "retweet"] in text.lower():
        try:
            api.PostRetweet(status_id=post.id)
            log("success: retweet tweet: " + post.id + " from user " + post.user.screen_name)
        except:
            log("error: Cannot retweet tweet: "+post.id+" from user "+post.user.screen_name)

#file to ignore contest that you already participate to
def ReadIgnoreFile():
    filename = config.IGNORE_PATH

    if os.path.exists(filename):
        file = open(filename, "r")
    else:
        file = open(filename, "w+")

    json = file.read()
    file.close()

    return json

def WriteIgnoreFile(post):
    filename = config.IGNORE_PATH

    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file = open(filename, "w+")
    else:
        file = open(filename, "a+")

    file.write()
    file.close()

log("info: script is  starting")

json = ReadIgnoreFile()
ignore_list = list()
if json:
    ignore_list = JSON.loads(json)

try:
    api = twitter.Api(consumer_key=config.CONSUMER_KEY,
                      consumer_secret=config.CONSUMER_SECRET,
                      access_token_key=config.ACCESS_TOKEN,
                      access_token_secret=config.ACCESS_TOKEN_SECRET)
    log("sucess: successfully contact the API")
except:
    log("error: cannot contact the API")
#
# list = api.GetSearch(term=config.TERMS, count=5, lang=config.LANG)
# for tweet in list:
