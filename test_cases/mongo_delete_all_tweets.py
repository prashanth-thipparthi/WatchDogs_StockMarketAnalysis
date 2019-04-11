import pymongo
from mongo_wrapper import MongoWrapper

if __name__ == "__main__":
    mongo_wrapper = MongoWrapper()
    mongo_wrapper.del_docs_in_collection('Tweets')

