"""
Starting the pipeline

1.Starting a zookeeper server  - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/zookeeper-server-start.sh /home/prth3635/kafka/kafka_2.12-2.2.0/config/zookeeper.properties

2.Starting a kafka server - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-server-start.sh /home/prth3635/kafka/kafka_2.12-2.2.0/config/server.properties

3.Create a topic - creating a topic - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --topic twitter --replication-factor 1 -partitions 3

4.-Run KafkaTweetsProducer.py (Start Producer)

/home/prth3635/spark/spark-2.4.1-bin-hadoop2.7/bin/spark-submit kafka_push_listener.py

5.-Run KafkaTweetsConsumerSpark.py (Start Consumer)

/home/prth3635/spark/spark-2.4.1-bin-hadoop2.7/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.1 kafka_twitter_spark_streaming.py

##optional
starting a console producer - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic video-stream-event

starting a console consumer - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic twitter --from-beginning

"""

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
from TweetParser import Tweet 
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext 

def add_to_database(rdd, sqlContext):
    parsedTweetDataFrame = sqlContext.createDataFrame(rdd)
    parsedTweetDataFrame.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()
    parsedTweetDataFrame.pprint()

if __name__ == "__main__":

    
    sparkSession = SparkSession.builder.appName("KafkaTweetsConsumerSpark").config("spark.mongodb.input.uri", "mongodb://prth3635:bigdata@34.83.10.248/check.check").config("spark.mongodb.output.uri", "mongodb://prth3635:bigdata@34.83.10.248/check.check").getOrCreate()
	#Create Spark Context to Connect Spark Cluster
    sc = sparkSession.sparkContext

	#Set the Batch Interval is 10 sec of Streaming Context
    ssc = StreamingContext(sc, 10)

	#Create Kafka Stream to Consume Data Comes From Twitter Topic
	#localhost:2181 = Default Zookeeper Consumer Address
    kafkaTwitterStream = KafkaUtils.createStream(ssc, 'localhost:2181', 'spark-streaming', {'twitter':1})
    
    #Parse Twitter Data as json
    parsed = kafkaTwitterStream.map(lambda v: json.loads(v[1]))

    parsedTweet = parsed.map(Tweet.parse_from_log_line)
    sqlContext = SQLContext(sc)
    
    parsedTweet.foreachRDD(lambda rdd, sqlContext : add_to_database)
   # parsedTweetDataFrame = sqlContext.createDataFrame(parsedTweet)
   # parsedTweetDataFrame.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()
   # parsedTweetDataFrame.pprint()
    #Count the number of tweets per User
    #user_counts = parsed.map(lambda tweet: (tweet['user']["screen_name"], 1)).reduceByKey(lambda x,y: x + y)

    #Print the User tweet counts
    #user_counts.pprint()

    #Start Execution of Streams
    ssc.start()
    ssc.awaitTermination()



