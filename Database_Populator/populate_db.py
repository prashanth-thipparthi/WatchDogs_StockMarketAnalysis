from kafka import KafkaConsumer
from json import loads
from WatchDogs_MongoWrapper import MongoWrapper
from WatchDogs_RedisWrapper import RedisWrapper
from constants import Constants

"""
Mongo_Group: The consumer is Mongo
Redis_Group: The consumer is Redis
"""

if __name__ == "__main__":
    Constants = Constants()
    r = RedisWrapper(Constants.decrypt_key)
    mng = MongoWrapper(Constants.decrypt_key)
    test_logger = mng.get_logger('Kafka DB Populator')
    consumer = KafkaConsumer(
        'mongoredis',
         bootstrap_servers=['34.83.10.248:9092'],
         auto_offset_reset='earliest',
         enable_auto_commit=True,
         group_id='MongoRedis',
         value_deserializer=lambda x: loads(x.decode('utf-8')))

    # r.redis_flush_all()
    # test_logger.info('Redis Cache Flushed')

    #### Pull all Companies and update the cache first
    for each_company in mng.get_all_stocks():
        stock_name = each_company['Company']
        r.redis_update_json('get_tweets_with_lat_long/', stock_name)
        r.redis_update_json('get_polarity_tweets_of_stock/', stock_name)
    test_logger.info('Redis Cache Updated')

    for message in consumer:
        message_value = message.value
        # print('message: ', message_value)
        # test_logger = mng.get_logger('Kafka DB Populator')
        # test_logger.info(message_value)
        mng.insert_kafka_tweet_into_db(message_value, message_value['Search_Text'])
        r.redis_insert_tweet(message_value['Search_Text'], message_value)







