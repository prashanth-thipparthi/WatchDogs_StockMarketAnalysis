from WatchDogs_MongoWrapper import MongoWrapper
if __name__ == "__main__":
    mongo = MongoWrapper()
    logger = mongo.get_logger('Tweets Stats')
    logger.info('# of companies in Companies in the database: '+str(mongo.print_statistics('Stocks')))
    logger.info('# of companies in Tweets in the database: '+str(mongo.print_statistics('Tweets')))

