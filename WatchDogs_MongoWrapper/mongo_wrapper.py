from .constants import Constants
import pymongo
import re
from textblob import TextBlob
import datetime
import sys

'''
Stocks: A Collection which contains all the Stocks in NYSE.
Tweets: A Collection which contains the tweets related to that particular company entry present in Stocks
Schema:
'''


class MongoWrapper:
    def __init__(self):
        constants = Constants()
        self.Stocks_collection = constants.mongo_stocks_collection_name
        self.Tweets_collection = constants.mongo_tweets_collection_name
        self.my_client = pymongo.MongoClient(
            'mongodb://{username}:{password}@{IP}:27017/{the_database}'.format(username=constants.mongo_username,
                                                                               password=constants.mongo_password,
                                                                               IP=constants.mongo_external_ip,
                                                                               the_database=constants.mongo_db_name))
        self.db = self.my_client[constants.mongo_db_name]
        self.stocks_client = self.db[self.Stocks_collection]
        self.tweets_client = self.db[self.Tweets_collection]

    '''This will load a newline separated text file into the Stocks document'''
    def load_companies(self, companies_file) -> None:
        """
        :param companies_file: A text file object
        :return: Nothing
        """
        companies = companies_file.readlines()
        for each_company in companies:
            each_company = each_company.strip()
            if len(each_company) > 0:
                try:
                    self.stocks_client.insert_one({"Company": each_company})
                except Exception as e:
                    if e.__class__.__name__ == 'DuplicateKeyError':
                        print('Duplicate error, company already present in database, hence ignoring the insert: ', each_company)
                        continue
                    else:
                        print(e)
                        # exit(1)

    def clean_tweet(self, tweet):
        """
        Clean tweet used in analize_sentiment
        :param tweet:
        :return:
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analize_sentiment(self, tweet):
        """
        Analyzing the sentiment of a tweet
        :param tweet:
        :return:
        """
        analysis = TextBlob(self.clean_tweet(tweet))
        return analysis.sentiment.polarity

    def get_all_stocks(self):
        for each_stock in self.stocks_client.find({},{"Company": 1, "_id": 0}):
            yield each_stock


    '''Insert documents into Tweets'''
    def insert_tweet_into_db(self, tweets, search_string)-> None:
        """

        :param tweets: an array of tweepy objects
        :return: None
        """
        for tweet in tweets:
            try:
                date_of_tweet = str(tweet.created_at.date())
                time_of_tweet = str(tweet.created_at.time())
                sentiment_value = self.analize_sentiment(tweet.full_text)
                if sentiment_value < 0:
                    sentiment_polarity = -1
                elif sentiment_value == 0:
                    sentiment_polarity = 0
                else:
                    sentiment_polarity = 1
                self.tweets_client.insert_one({
                    "tweet_id" : tweet.id,
                    "DateTimeObject": tweet.created_at,
                    "Date": date_of_tweet,
                    "Time": time_of_tweet,
                    "Geo": tweet.geo,
                    "Coordinates": tweet.coordinates,
                    # "Place": tweet.place.bounding_box.coordinates,
                    "Search_Text": search_string,
                    "Text": tweet.full_text,
                    "Sentiment_Value": sentiment_value,
                    "Sentiment_Polarity": sentiment_polarity
                })
            except Exception as e:
                if e.__class__.__name__ == 'DuplicateKeyError':
                    # print('Tried to insert duplicates')
                    continue
                else:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    line = exc_tb.tb_lineno
                    raise Exception('Exception is {excp}, line is {line}, some extra comments: {e_string}'.format(excp=exc_type,
                                                                                                                  line=line,
                                                                                                                  e_string = e))
                    # exit(1)

    def filter_docs(self, start: datetime=None, end: datetime=None) -> pymongo.cursor.Cursor:
        """
        Filter documents according to date and time
        :param start: start datetime object
        :param end: end datetime object
        :return:
        """
        class InputArgumentError(Exception):
            def __init__(self):
                print('You should pass atleast a start or end object. Else there is nothing to filter')


        if start or end:
            if end == None:
                my_query = {"DateTimeObject": {"$gte": start} }
                return self.tweets_client.find(my_query)
            elif start == None:
                my_query = {"DateTimeObject": {"$lte": end}}
                return self.tweets_client.find(my_query)
            else:
                my_query = {"DateTimeObject": {"$gte": start, "$lte": end}}
                return self.tweets_client.find(my_query)
        else:
            raise InputArgumentError

    def get_tweets_of_stock(self, stock_name, limit=0):
        """

        :param stock_name: The company stock name you are searching for in database
        :param limit: The threshold tweets I need to return
        :return:
        """
        class InputStockError(Exception):
            def __init__(self):
                print('Either your stock does not exist in the database or it is newly added. Either case check your input')
        if limit:
            my_query = {"Search_Text": stock_name}
            tweets = self.tweets_client.find(my_query).limit(limit)
            if tweets.count() == 0:
                raise InputStockError
            else:
                return tweets
        else:
            my_query = {"Search_Text": stock_name}
            tweets = self.tweets_client.find(my_query)
            if tweets.count() == 0:
                raise InputStockError
            else:
                return tweets

    def get_lat_long(self, stock_name):
        """

        :param stock_name:
        :return:
        """
        class InputStockError(Exception):
            def __init__(self):
                print('Either your stock does not exist in the database or it is newly added. Either case check your input')

        my_query = {"Search_Text": stock_name, "Sentiment_Polarity":-1, "Coordinates":{"$ne":"null"}}
        tweets_negative = self.tweets_client.find(my_query)
        my_query = {"Search_Text": stock_name, "Sentiment_Polarity": 0, "Coordinates":{"$ne":"null"}}
        tweets_neutral = self.tweets_client.find(my_query)
        my_query = {"Search_Text": stock_name, "Sentiment_Polarity": 1, "Coordinates":{"$ne":"null"}}
        tweets_positive = self.tweets_client.find(my_query)
        if tweets_negative.count() == 0 and tweets_neutral.count() == 0 and tweets_positive.count() == 0:
            raise InputStockError
        else:
            neg_lat = []
            neg_long = []
            neu_lat = []
            neu_long = []
            pos_lat = []
            pos_long = []
            for each_tweet in tweets_negative:
                try:
                    lat_long_list = each_tweet['Geo']['coordinates']
                    neg_lat.append(lat_long_list[0])
                    neg_long.append(lat_long_list[1])
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print('Exception is {excp}, line is {line}, some extra comments: {e_string}'.format(excp=exc_type,
                                                                                                                  line=exc_tb.tb_lineno,
                                                                                                                  e_string = e))
                    continue
            for each_tweet in tweets_neutral:
                try:
                    lat_long_list = each_tweet['Geo']['coordinates']
                    neu_lat.append(lat_long_list[0])
                    neu_long.append(lat_long_list[1])
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    if e.__class__.__name__ != 'TypeError':
                        continue
                    else:
                        print('Exception is {excp}, line is {line}, some extra comments: {e_string}'.format(excp=exc_type,
                                                                                                                  line=exc_tb.tb_lineno,
                                                                                                                  e_string = e))
                    continue
            for each_tweet in tweets_positive:
                try:
                    lat_long_list = each_tweet['Geo']['coordinates']
                    pos_lat.append(lat_long_list[0])
                    pos_long.append(lat_long_list[1])
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print('Exception is {excp}, line is {line}, some extra comments: {e_string}'.format(excp=exc_type,
                                                                                                                  line=exc_tb.tb_lineno,
                                                                                                                  e_string = e))
                    continue
            return ([neg_lat, neg_long], [neu_lat, neu_long], [pos_lat, pos_long])


    def get_polarity_tweets_of_stock(self, stock_name):
        """

        :param stock_name: The company stock name you are searching for in database
        :param limit: The threshold tweets I need to return
        :return:
        """
        class InputStockError(Exception):
            def __init__(self):
                print('Either your stock does not exist in the database or it is newly added. Either case check your input')

        my_query = {"Search_Text": stock_name, "Sentiment_Polarity":-1}
        tweets_negative = self.tweets_client.find(my_query)
        my_query = {"Search_Text": stock_name, "Sentiment_Polarity": 0}
        tweets_neutral = self.tweets_client.find(my_query)
        my_query = {"Search_Text": stock_name, "Sentiment_Polarity": 1}
        tweets_positive = self.tweets_client.find(my_query)
        if tweets_negative.count() == 0 and tweets_neutral.count()==0 and tweets_positive.count()==0:
            raise InputStockError
        else:
            return (tweets_negative, tweets_neutral, tweets_positive)


    def print_statistics(self, coll_name) -> int:
        """
        return # of documents in a collection
        :param coll_name:
        :return: Int. # of documents
        """
        my_coll = self.db[coll_name]
        return my_coll.count_documents({})

    '''Delete All documents in a collection'''
    def del_docs_in_collection(self, collection_name) -> int:
        """
        :param collection_name:
        :return: # of deleted documents
        """
        '''For the love of God don't use this function.'''
        my_col = self.db[collection_name]
        x = my_col.delete_many({})
        print('All docs deleted. Count: ', x.deleted_count)
        return x.deleted_count
