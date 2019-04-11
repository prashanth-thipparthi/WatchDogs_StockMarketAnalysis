This is a mongo wrapper developed for the project

# Usage:
> pip install --upgrade git+ssh://git@github.com/CUBigDataClass/WatchDogs_MongoWrapper.git

> pip install --upgrade git+https://github.com/CUBigDataClass/WatchDogs_MongoWrapper.git

After successful install you can import as follows:
```
from WatchDogs_MongoWrapper import MongoWrapper
mongowrapper = MongoWrapper()
# Sample Test
print('# of companies in Companies in the database: ', mongowrapper.print_statistics('Stocks'))
``
