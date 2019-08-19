# Status:
[![Build Status](https://travis-ci.com/CUBigDataClass/WatchDogs_MongoWrapper.svg?token=kN4PmwFFW7UpnvGkMmzk&branch=master)](https://travis-ci.com/CUBigDataClass/WatchDogs_MongoWrapper)

This is a mongo wrapper developed for the project

# SSH Installation:
> pip install --upgrade git+ssh://git@github.com/CUBigDataClass/WatchDogs_MongoWrapper.git

# HTTPS Installation:
> pip install --upgrade git+https://github.com/CUBigDataClass/WatchDogs_MongoWrapper.git

After successful install you can import as follows:
```
from WatchDogs_MongoWrapper import MongoWrapper
mongowrapper = MongoWrapper()
# Sample Test
print('# of companies in Companies in the database: ', mongowrapper.print_statistics('Stocks'))
``
