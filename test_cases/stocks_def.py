from WatchDogs_MongoWrapper import MongoWrapper

if __name__ == "__main__":
    mongo_wrapper = MongoWrapper()
    test = mongo_wrapper.get_tweets_of_stock("3D Systems Corporation")

    for x in test:
        print(x)


