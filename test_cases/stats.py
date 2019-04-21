from WatchDogs_MongoWrapper import MongoWrapper
if __name__ == "__main__":
    mongo = MongoWrapper()
    print('# of companies in Companies in the database: ', mongo.print_statistics('Stocks'))
    print('# of companies in Tweets in the database: ',mongo.print_statistics('Tweets'))

