import json 
from textblob import TextBlob
import re
from time import sleep
from kafka import KafkaProducer


class Tweet():

    def __init__(self,in_json):
        
        #in_json = json.loads(in_json)
        #self.tweet_id = in_json.id
        #self.dateTime = in_json.created_at
        #self.geo = in_json.geo
        #self.coordinates= in_json.coordinates
        #self.search_text = in_json.text
        #self.text = in_json.text

        pass   
    @staticmethod
    def clean_tweet(tweet):
        """
        Clean tweet used in analize_sentiment
        :param tweet:
        :return:
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    @staticmethod
    def analize_sentiment(tweet):
        """
        Analyzing the sentiment of a tweet
        :param tweet:
        :return:
        """
        analysis = TextBlob(Tweet.clean_tweet(tweet))
        return analysis.sentiment.polarity

    @staticmethod		
    def parse_from_log_line(in_json):
        #print(in_json)
    #    print("DATA_TYPE:",in_json)
        new = {}
        if "text" in in_json:
            sentiment_value = Tweet.analize_sentiment(in_json["text"])
            if sentiment_value < 0:
                sentiment_polarity = -1
            elif sentiment_value == 0:
                sentiment_polarity = 0
            else:
                sentiment_polarity = 1
            new["tweet_id"] = in_json["id"]
            new["DateTimeObject"] = in_json["date_time"]
            new["Date"] = in_json["date"]
            new["Time"] = in_json["time"]
            if in_json["geo"] is not None :
                new["Geo"] = in_json["geo"]
            else:
                new["Geo"] = "null"
            if in_json["coordinates"] is not None :
                new["Coordinates"] = in_json["coordinates"]
            else:
                new["Coordinates"] = "null"
            new["Text"] = in_json["text"]
            new["Sentiment_Value"] = sentiment_value
            new["Sentiment_Polarity"] = sentiment_polarity
            new["Search_Text"] = in_json["search_text"]
            return new
        else:
            return new      
#        return json.loads(new)
    def __repr__(self):
        return "{} {} {} [{}] \"{} {} {}\" {} {}".format(self.tweet_id, self.dateTime,self.geo, self.coordinates, self.search_text,self.text, self.sentiment_value, self.sentiment_polarity)


di = {"id":1,"created_at":123,"geo":123,"coordinates":12,"search_text":"abc","text":"xyz","date_time":"1233","date":"1","time":"3"}
t = Tweet.parse_from_log_line(di)
print("val:", t)
