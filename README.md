# WatchDogs_Kafka_Spark
Kafka and Spark Integration in the Watch Dogs Project

## Starting the pipeline

1.Starting a zookeeper server  - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/zookeeper-server-start.sh /home/prth3635/kafka/kafka_2.12-2.2.0/config/zookeeper.properties

2.Starting a kafka server - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-server-start.sh /home/prth3635/kafka/kafka_2.12-2.2.0/config/server.properties

3.Create a topic - creating a topic - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --topic twitter --replication-factor 1 -partitions 3

cd into src folder: 
4.-Run KafkaTweetsProducer.py (Start Producer)

/home/prth3635/spark/spark-2.4.1-bin-hadoop2.7/bin/spark-submit kafka_push_listener.py

5.-Run KafkaTweetsConsumerSpark.py (Start Consumer)

/home/prth3635/spark/spark-2.4.1-bin-hadoop2.7/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.1 kafka_twitter_spark_streaming.py

## optional
starting a console producer - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic video-stream-event

starting a console consumer - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic twitter --from-beginning
