from flask import Flask
from WatchDogs_MongoWrapper import MongoWrapper
from flask import abort
from bson.json_util import dumps
import json

app = Flask(__name__)


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
    app.run()
