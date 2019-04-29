import pykafka
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import twitter_credentials
import threading

#TWITTER API CONFIGURATIONS
consumer_api_key = twitter_credentials.consumer_api_key
consumer_api_secret_key = twitter_credentials.consumer_api_secret_key
access_token = twitter_credentials.access_token
access_token_secret = twitter_credentials.access_token_secret

#TWITTER API AUTH
auth = OAuthHandler(consumer_api_key, consumer_api_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)





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
        print("DATA TYPE:",self.stock)
        js = json.loads(data)
        js["search_text"] = self.stock
        data = json.dumps(js)
        #print(data)
        self.producer.produce(bytes(data, "ascii"))
        return True
                                                                                                                                           
    def on_error(self, status):
        print(status)
        return True

def multiple_producer_thread(auth,topic):    
    tweets_stream = Stream(auth, KafkaTweetsProducer(topic))
    tweets_stream.filter(track=[topic])

arr = ["like","football","love","car"]
threads = []
i = 0
for a in arr:
    thread = threading.Thread(target = multiple_producer_thread, args = (auth,a))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()


#t1 = threading.Thread(target = multiple_producer_thread, args = (auth,"president"))
#t2 = threading.Thread(target = multiple_producer_thread, args = (auth,"love"))
#t3 = threading.Thread(target = multiple_producer_thread, args = (auth,"football"))

#t1.start()
#t2.start()
#t3.start()

#t1.join()
#t2.join()
#t3.join()
#Twitter Stream Config


#Produce Data that has Game of Thrones hashtag (Tweets)


