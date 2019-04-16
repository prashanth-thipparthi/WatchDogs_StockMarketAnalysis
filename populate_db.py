import signal
import tweepy
from WatchDogs_MongoWrapper import MongoWrapper
import time
import random

def get_keys():
    if random.randint(0, 1) == 3:
        CONSUMER_KEY = '1pmAQV2KBiItz3OsGWIrAPQrv'
        CONSUMER_SECRET = 'oPIkrswP7eJh1gwaDiyOY8meYbcMTMhEsKnG5sdtethQSxSlMB'
        ACCESS_TOKEN = '985993112-hRyi1aAGNzOGy0jan6WxC5UiEedZsCezpl1WxVKF'
        ACCESS_SECRET = 'LrbZTey5eVpeRtOwOpdAMj0XVztupHF3vkqze4yBcdq7h'
    else:
        CONSUMER_KEY = "lQu7vXPH6hMNQ92LLVOFD5K8b"
        CONSUMER_SECRET = "NwoUxJgXZkA6Fm0IJpNC6S0bavZy3YVcblKrQQbna7R4lwj39X"
        ACCESS_TOKEN = "1170146904-NfXboXT6cjI8zcThUiixJp1AztyJH4Hw8wdkDwj"
        ACCESS_SECRET = "rpRprMkactMVuKiJsESZGjEUmbixPABB3NjIKOxymJT7K"
    return (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

def twitter_setup():
    try:
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET = get_keys()
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api
    except:
        print("Error: Authentication Failed")
if __name__ == "__main__":
    mng = MongoWrapper()
    killer = GracefulKiller()
    while 1:
        pullTweets = twitter_setup()  # Should this be in or out of the loop. An eternal confusion
        stock_companies = []
        for stock in mng.get_all_stocks():
            stock_companies.append(stock['Company'])
        for stock_name in stock_companies:
            tweets = pullTweets.search(q=[stock_name], count=200, tweet_mode="extended")
            mng.insert_tweet_into_db(tweets, stock_name)
            time.sleep(20)
        if killer.kill_now:
            break
    print('Process killed. Please put it in a logstash')
