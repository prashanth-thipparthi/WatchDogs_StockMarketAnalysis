import pykafka
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import twitter_credentials
import threading
import time
import dateutil.parser as parser
from WatchDogs_MongoWrapper import MongoWrapper
import random

#TWITTER API CONFIGURATIONS
'''
consumer_api_key = twitter_credentials.consumer_api_key
consumer_api_secret_key = twitter_credentials.consumer_api_secret_key
access_token = twitter_credentials.access_token
access_token_secret = twitter_credentials.access_token_secret

#TWITTER API AUTH
auth = OAuthHandler(consumer_api_key, consumer_api_secret_key)
auth.set_access_token(access_token, access_token_secret)

#api = tweepy.API(auth)
'''

#Twitter Stream Listener
class KafkaTweetsProducer(StreamListener):          
	
    def __init__(self,stock_name):
        #localhost:9092 = Default Zookeeper Producer Host and Port Adresses
        self.client = pykafka.KafkaClient("localhost:9092")
        self.stock = stock_name
	#Get Producer that has topic name is Twitter
        self.producer = self.client.topics[bytes("twitter", "ascii")].get_producer()

    def on_data(self, data):
        #Producer produces data for consumer
        #Data comes from Twitter
        #print(data)
        #print("DATA TYPE:",self.stock)
        js = json.loads(data)
        js["search_text"] = self.stock
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(js["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
        date = parser.parse(ts)
        tsa = ts.split(" ")
        js["date"] = tsa[0];
        js["time"] = tsa[1];
        js["date_time"] = str(date)
        print(js)
        
        if "retweeted_status" in js:
            try:
                tweet = js["retweeted_status"]
                if "extended_tweet" in tweet:
                    t =  tweet["extended_tweet"]
                    if "full_text" in t:
                        tweet = t["full_text"]
                else:
                    tweet = js["text"]
            except:
                #tweet = js["retweeted_status"]
                tweet = js["text"]
        else:
            tweet = js["text"]
        print("tweet: ",tweet)
        '''
        if "full_text" in js:
            print("full_text")
            print("js[full_text]: ",js["full_text"])
        else:
           print("text")
           print("js[text]: ",js["text"])
        '''           
        data = json.dumps(js)
        #print(data)
        self.producer.produce(bytes(data, "ascii"))
        return True
                                                                                                                                           
    def on_error(self, status):
        print(status)
        return True

def multiple_producer_thread(auth,topic):    
    tweets_stream = Stream(auth, KafkaTweetsProducer(topic), tweet_mode='extended')
    tweets_stream.filter(track=[topic])

def getAuth():
    number = random.randint(1, 3)
    print("number:", number)
    consumer_api_key = '1pmAQV2KBiItz3OsGWIrAPQrv'
    consumer_api_secret_key = 'oPIkrswP7eJh1gwaDiyOY8meYbcMTMhEsKnG5sdtethQSxSlMB'
    access_token = '985993112-hRyi1aAGNzOGy0jan6WxC5UiEedZsCezpl1WxVKF'
    access_token_secret = 'LrbZTey5eVpeRtOwOpdAMj0XVztupHF3vkqze4yBcdq7h'
    if number == 3:
        consumer_api_key = '1pmAQV2KBiItz3OsGWIrAPQrv'
        consumer_api_secret_key = 'oPIkrswP7eJh1gwaDiyOY8meYbcMTMhEsKnG5sdtethQSxSlMB'
        access_token = '985993112-hRyi1aAGNzOGy0jan6WxC5UiEedZsCezpl1WxVKF'
        access_token_secret = 'LrbZTey5eVpeRtOwOpdAMj0XVztupHF3vkqze4yBcdq7h'
    elif number == 2:
        consumer_api_key = "lQu7vXPH6hMNQ92LLVOFD5K8b"
        consumer_api_secret_key = "NwoUxJgXZkA6Fm0IJpNC6S0bavZy3YVcblKrQQbna7R4lwj39X"
        access_token = "1170146904-NfXboXT6cjI8zcThUiixJp1AztyJH4Hw8wdkDwj"
        access_token_secret = "rpRprMkactMVuKiJsESZGjEUmbixPABB3NjIKOxymJT7K"
    elif number == 1:
        consumer_api_key = twitter_credentials.consumer_api_key
        consumer_api_secret_key = twitter_credentials.consumer_api_secret_key
        access_token = twitter_credentials.access_token
        access_token_secret = twitter_credentials.access_token_secret
	
    auth = OAuthHandler(consumer_api_key, consumer_api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    return auth
    
arr = ["like","football","love","car"]
threads = []
i = 0

mng = MongoWrapper()
stock_companies = []
for stock in mng.get_all_stocks():
    stock_companies.append(stock['Company'])

print(stock_companies)    



for a in stock_companies:
    auth = getAuth()
    thread = threading.Thread(target = multiple_producer_thread, args = (auth,a))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

'''
t1 = threading.Thread(target = multiple_producer_thread, args = (auth,"Facebook"))
t2 = threading.Thread(target = multiple_producer_thread, args = (auth,"apple"))
t3 = threading.Thread(target = multiple_producer_thread, args = (auth,"Visa"))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
'''
#Twitter Stream Config


#Produce Data that has Game of Thrones hashtag (Tweets)


