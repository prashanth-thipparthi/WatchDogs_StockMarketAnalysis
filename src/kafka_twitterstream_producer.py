import pykafka
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import twitter_credentials

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
	def __init__(self):
		#localhost:9092 = Default Zookeeper Producer Host and Port Adresses
		self.client = pykafka.KafkaClient("localhost:9092")
		
		#Get Producer that has topic name is Twitter
		self.producer = self.client.topics[bytes("twitter", "ascii")].get_producer()
  
	def on_data(self, data):
		#Producer produces data for consumer
		#Data comes from Twitter
		self.producer.produce(bytes(data, "ascii"))
		return True
                                                                                                                                           
	def on_error(self, status):
		print(status)
		return True

#Twitter Stream Config
tweets_stream = Stream(auth, KafkaTweetsProducer())

#Produce Data that has Game of Thrones hashtag (Tweets)
tweets_stream.filter(track=['football'])

