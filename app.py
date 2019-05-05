from flask import Flask
from flask import abort
from WatchDogs_RedisWrapper import RedisWrapper
from WatchDogs_MongoWrapper import MongoWrapper
from bson.json_util import dumps
import json
import sys
import signal


def handler(signal, frame):
    my_logger.info('Flask App is being killed')

app = Flask(__name__)

@app.route('/api')
def it_works():
    return "Prashanth Rocks kafka!"

# @app.route('/api/get_tweets_with_lat_long/<stock_name>')
# def get_tweets_with_lat_long(stock_name):
#     try:
#         r = RedisWrapper()
#         json_data = r.redis_get_json('get_tweets_with_lat_long/', stock_name)
#         return json_data
#     except:
#         abort(404)
#
# @app.route('/api/get_polarity_tweets_of_stock/<stock_name>')
# def get_polarity_tweets_of_stock(stock_name):
#     try:
#         r = RedisWrapper()
#         json_data = r.redis_get_json('get_polarity_tweets_of_stock/', stock_name)
#         return json_data
#     except:
#         abort(404)

@app.route('/api/get_tweets_with_lat_long/<stock_name>')
def get_tweets_with_lat_long(stock_name):
    try:
        mng = MongoWrapper()
        data_frame = mng.get_tweets_with_lat_long(stock_name)
        return data_frame.to_json()
    except:
        abort(404)

@app.route('/api/get_polarity_tweets_of_stock/<stock_name>')
def get_polarity_tweets_of_stock(stock_name):
    mng = MongoWrapper()
    try:
        neg, neu, pos = mng.get_polarity_tweets_of_stock(stock_name)
        neg_tweets = dumps(neg)
        neu_tweets = dumps(neu)
        pos_tweets = dumps(pos)
        data = {"neg_tweets": neg_tweets, "neu_tweets": neu_tweets, "pos_tweets":pos_tweets  }
        return json.dumps(data)
    except:
        abort(404)




if __name__ == '__main__':
    r = RedisWrapper()
    my_logger = r.get_logger('Flask App')
    my_logger.info('Flask API Server Started')
    signal.signal(signal.SIGTERM, handler)
    app.run(host='0.0.0.0')
