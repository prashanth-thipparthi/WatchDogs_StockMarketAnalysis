import tweepy
from WatchDogs_MongoWrapper import MongoWrapper
import time

CONSUMER_KEY = '1pmAQV2KBiItz3OsGWIrAPQrv'
CONSUMER_SECRET = 'oPIkrswP7eJh1gwaDiyOY8meYbcMTMhEsKnG5sdtethQSxSlMB'
ACCESS_TOKEN = '985993112-hRyi1aAGNzOGy0jan6WxC5UiEedZsCezpl1WxVKF'
ACCESS_SECRET = 'LrbZTey5eVpeRtOwOpdAMj0XVztupHF3vkqze4yBcdq7h'


def twitter_setup():
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api
    except:
        print("Error: Authentication Failed")


if __name__ == "__main__":
    mng = MongoWrapper()
    while 1:
        pullTweets = twitter_setup() #Should this be in or out of the loop. An eternal confusion
        for stock in mng.get_all_stocks():
            stock_name = stock['Company']
            tweets = pullTweets.search(q=[stock_name], count=200)
            mng.insert_tweet_into_db(tweets, stock_name)
