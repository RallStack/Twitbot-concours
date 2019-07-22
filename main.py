import twitter
import config
import datetime
import json as JSON
import os
import time

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
        log("success: follow user")
    except Exception as e:
        log("error:"+str(e))

    for user in post.user_mentions:
        api.CreateFriendship(user_id=user.id)

def Retweet(post):
    text = post.full_text

    log("info: retweet starting: " + str(post.id) + " from user " + post.user.screen_name)

    if any(x in text.lower() for x in config.RT_LIST):
        try:
            api.PostRetweet(status_id=post.id)
            log("success: retweet tweet")
        except Exception as e:
            log("error:"+str(e))

def Fav(post):
    text = post.full_text

    log("info: Fav starting: " + str(post.id) + " from user " + post.user.screen_name)

    if any(x in text.lower() for x in config.FAV_LIST):
        try:
            api.CreateFavorite(status_id=post.id)
            log("success: Fav tweet")
        except Exception as e:
            log("error:"+str(e))

def Identify(post):
    text = post.full_text

    log("info: Identify starting: " + str(post.id) + " from user " + post.user.screen_name)

    if any(x in text.lower() for x in config.IDENTIFY_LIST):
        try:
            api.PostUpdate(status="@RallStack",in_reply_to_status_id=post.id,auto_populate_reply_metadata=True, )
            log("success: Identify tweet")
        except Exception as e:
            log("error:"+str(e))

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
except Exception as e:
    log("error:"+str(e))

count = 0

while count < 4:
    list = api.GetSearch(term=config.TERMS, count=config.SEARCH_CONTER, lang=config.LANG)
    for tweet in list:
        if tweet.retweeted_status:
            post = tweet.retweeted_status
        else:
            post = tweet

        if post.id not in ignore_list:
            if not any(x in post.full_text.lower() for x in config.BAN_WORDS):
                ignore_list.append(post.id)
                Follow(post)
                Retweet(post)
                Fav(post)
                Identify(post)
                time.sleep(30)

    count += 1


    ignore_list_string = JSON.dumps(ignore_list)
    WriteIgnoreFile(ignore_list_string)

log("sucess: work is done")