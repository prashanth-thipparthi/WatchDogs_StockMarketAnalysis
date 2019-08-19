import tweepy
from WatchDogs_MongoWrapper import MongoWrapper

CONSUMER_KEY = "lQu7vXPH6hMNQ92LLVOFD5K8b"
CONSUMER_SECRET = "NwoUxJgXZkA6Fm0IJpNC6S0bavZy3YVcblKrQQbna7R4lwj39X"
ACCESS_TOKEN = "1170146904-NfXboXT6cjI8zcThUiixJp1AztyJH4Hw8wdkDwj"
ACCESS_SECRET = "rpRprMkactMVuKiJsESZGjEUmbixPABB3NjIKOxymJT7K"


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
    tweets = pullTweets.search(q=["Boeing"], count=200, tweet_mode="extended")
    mongo = MongoWrapper()
    mongo.get_polarity_tweets_of_stock("Aramark")
