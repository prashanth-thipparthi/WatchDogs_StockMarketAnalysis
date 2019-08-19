# WatchDogs_Kafka_Spark
Kafka and Spark Integration in the Watch Dogs Project

## Software Versions
Jdk - 11  
Spark - spark-2.4.1-bin-hadoop2.7  
Kafka - kafka_2.12-2.2.0   

## Starting the pipeline

1.Starting a zookeeper server  - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/zookeeper-server-start.sh -daemon /home/prth3635/kafka/kafka_2.12-2.2.0/config/zookeeper.properties

2.Starting a kafka server - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-server-start.sh -daemon /home/prth3635/kafka/kafka_2.12-2.2.0/config/server.properties

3.Create a topic - creating a topic - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --topic twitter --replication-factor 1 -partitions 3

cd into "/src" folder of the repository:  
4.-Run kafka_twitterstream_producer.py (Start Producer)

/home/prth3635/spark/spark-2.4.1-bin-hadoop2.7/bin/spark-submit kafka_twitterstream_producer.py

5.-Run kafka_twitterstream_consumer_spark.py (Start Consumer)

/home/prth3635/spark/spark-2.4.1-bin-hadoop2.7/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.1,org.mongodb.spark:mongo-spark-connector_2.11:2.4.0 kafka_twitterstream_consumer_spark.py

## optional
starting a console producer - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic video-stream-event

starting a console consumer - /home/prth3635/kafka/kafka_2.12-2.2.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic twitter --from-beginning
