import datetime
from WatchDogs_MongoWrapper import MongoWrapper

if __name__ == "__main__":
    mng = MongoWrapper()
    for stock in mng.get_all_stocks():
        print(stock['Company'])