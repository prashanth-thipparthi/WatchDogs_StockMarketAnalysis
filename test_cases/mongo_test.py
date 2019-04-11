import pymongo
from WatchDogs_MongoWrapper import MongoWrapper

if __name__ == "__main__":
    mongo_wrapper = MongoWrapper()
    comapny_file = open('test_cases/companies.txt', 'r')
    mongo_wrapper.load_companies(comapny_file)
