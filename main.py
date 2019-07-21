import twitter
import config
import datetime

api = twitter.Api(consumer_key=config.CONSUMER_KEY,
                  consumer_secret=config.CONSUMER_SECRET,
                  access_token_key=config.ACCESS_TOKEN,
                  access_token_secret=config.ACCESS_TOKEN_SECRET)

def log(text=""):
    date = datetime.datetime.now()

    file = open(config.LOG_PATH + date.year + '_' + date.month + '_' + date.day, "a+")
    file.write(text)
    file.close()

list = api.GetSearch(term="RT et follow", count=25, lang="fr")
