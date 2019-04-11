import unittest
import datetime
from WatchDogs_MongoWrapper import MongoWrapper
import tweepy

class MongoWrapperTests(unittest.TestCase):
    def test_filter(self):
        start = datetime.datetime(2019, 4, 8, 20, 16, 6)
        end = datetime.datetime(2019, 4, 8, 20, 16, 10)
        mng = MongoWrapper()
        x = mng.filter_docs(start, end)
        self.assertEqual(x.count(), 2)

    def test_db_insert(self):
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

        pullTweets = twitter_setup()
        tweets = pullTweets.search(q=["Abercrombie & Fitch Company"], count=200, tweet_mode="extended")
        mongo = MongoWrapper()
        mongo.insert_tweet_into_db(tweets, "Abercrombie & Fitch Company")

    def test_stocks_def(self):
        mongo_wrapper = MongoWrapper()
        test = mongo_wrapper.get_tweets_of_stock("3D Systems Corporation")
        self.assertGreater(test.count(), 0)

if __name__ == '__main__':
    unittest.main()


