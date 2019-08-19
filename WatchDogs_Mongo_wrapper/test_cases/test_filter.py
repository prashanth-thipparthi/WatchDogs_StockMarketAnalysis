import datetime
from WatchDogs_MongoWrapper import MongoWrapper

if __name__ == "__main__":
    start = datetime.datetime(2019, 4, 8, 20, 16, 6)
    end = datetime.datetime(2019, 4, 8, 20, 16, 10)

    mng = MongoWrapper()
    x = mng.filter_docs(start, end)
    for each_x in x:
        print(each_x)
