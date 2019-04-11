import tweepy
from WatchDogs_MongoWrapper import MongoWrapper

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
    pullTweets = twitter_setup()
    tweets = pullTweets.search(q=["python"], count=200)
    mongo = MongoWrapper()
    mongo.insert_tweet_into_db(tweets, "python")
