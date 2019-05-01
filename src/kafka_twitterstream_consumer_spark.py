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
from pyspark.sql.types import StringType, StructField, StructType, BooleanType, ArrayType, IntegerType, DateType, LongType, DoubleType

def add_to_database(rdd):
    pprint("ENTERED INTO THE DATABASE MODULEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    parsedTweetDataFrame = sqlContext.createDataFrame(rdd)
    parsedTweetDataFrame.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()
    parsedTweetDataFrame.pprint()
    pprint("*****************************************************************************************")
    return parsedTweetDataFrame
#if __name__ == "__main__":

def empty_rdd():
    print("RDD is empty")
    
sparkSession = SparkSession.builder.appName("KafkaTweetsConsumerSpark").config("spark.mongodb.input.uri", "mongodb://prth:root@104.198.19.115/dbase.tweets").config("spark.mongodb.output.uri", "mongodb://prth:root@104.198.19.115:27017/dbase.tweets").getOrCreate()
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
#parsedTweet.pprint()
sqlContext = SQLContext(sc)
#parsedTweet.pprint()
schema_inf = StructType([
        StructField("tweet_id", LongType(), True),
        StructField("DateTimeObject", StringType(), True),
        StructField("Date", StringType(), True),
        StructField("Time", StringType(), True),
        StructField("Geo", StringType(), True),
        StructField("Coordinates",StringType(), True),
        StructField("Text",StringType(), True),
        StructField("Sentiment_Value",DoubleType(), True),
        StructField("Sentiment_Polarity",IntegerType(), True),
        StructField("Search_Text",StringType(), True)
    ])
 
#parsedTweetDataframe = parsedTweet.map(add_to_database)  
parsedTweet.foreachRDD(lambda rdd : sqlContext.createDataFrame(rdd,schema_inf).write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save() if rdd.count() != 0 else empty_rdd() )
   # parsedTweetDataFrame = sqlContext.createDataFrame(parsedTweet)
   # parsedTweetDataFrame.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()
parsedTweet.pprint()
    #Count the number of tweets per User
    #user_counts = parsed.map(lambda tweet: (tweet['user']["screen_name"], 1)).reduceByKey(lambda x,y: x + y)

    #Print the User tweet counts
    #user_counts.pprint()

    #Start Execution of Streams
ssc.start()
ssc.awaitTermination()



