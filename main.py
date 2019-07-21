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

    file.write(str(date.hour)+':'+str(date.minute)+':'+str(date.second)+' | '+text+'\n')
    file.close()

def Follow(post):
    text = post.full_text

    log("info: follow user : "+post.user.screen_name)

    try:
        api.CreateFriendship(user_id=post.user.id)
        log("success: follow user : "+post.user.screen_name)
    except:
        log("error: cannot follow user : "+post.user.screen_name)

def Retweet(post):
    text = post.full_text

    log("info: retweet starting: " + str(post.id) + " from user " + post.user.screen_name)

    if any(x in text.lower() for x in ["rt", "retweet"]):
        try:
            api.PostRetweet(status_id=post.id)
            log("success: retweet tweet: " + str(post.id) + " from user " + post.user.screen_name)
        except:
            log("error: Cannot retweet tweet: "+str(post.id)+" from user "+post.user.screen_name)

def Fav(post):
    text = post.full_text

    log("info: Fav starting: " + str(post.id) + " from user " + post.user.screen_name)

    if any(x in text.lower() for x in ["fav", "like", "coeur"]):
        try:
            api.CreateFavorite(status_id=post.id)
            log("success: Fav tweet: " + str(post.id) + " from user " + post.user.screen_name)
        except:
            log("error: Cannot fav tweet: "+str(post.id)+" from user "+post.user.screen_name)

#file to ignore contest that you already participate to
def ReadIgnoreFile():
    filename = config.IGNORE_PATH

    log("info: read ignore file")

    if os.path.exists(filename):
        file = open(filename, "r")
    else:
        file = open(filename, "w+")

    json = file.read()
    file.close()

    log("success: read ignore file done")

    return json

def WriteIgnoreFile(content):
    filename = config.IGNORE_PATH

    log("info: write ignore file")

    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    file = open(filename, "w+")

    file.write(content)
    file.close()

    log("success: write ignore file done")

log("info: script is  starting")

json = ReadIgnoreFile()
ignore_list = []
if json:
    ignore_list = JSON.loads(json)

try:
    api = twitter.Api(consumer_key=config.CONSUMER_KEY,
                      consumer_secret=config.CONSUMER_SECRET,
                      access_token_key=config.ACCESS_TOKEN,
                      access_token_secret=config.ACCESS_TOKEN_SECRET,
                      cache=None,
                      tweet_mode='extended')

    log("success: successfully contact the API")
except:
    log("error: cannot contact the API")

list = api.GetSearch(term=config.TERMS, count=5, lang=config.LANG)
for tweet in list:
    if tweet.retweeted_status:
        x = tweet.retweeted_status
    else:
        x = tweet

    if x.id not in ignore_list:
        ignore_list.append(x.id)
        Follow(x)
        Retweet(x)

ignore_list_string = JSON.dumps(ignore_list)
WriteIgnoreFile(ignore_list_string)

log("sucess: work is done")