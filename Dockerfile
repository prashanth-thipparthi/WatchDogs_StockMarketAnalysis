FROM gcr.io/vaulted-zodiac-236605/watchdogs_dbpopulator_base

WORKDIR /home
RUN pip install flask
RUN pip install --upgrade git+ssh://git@github.com/CUBigDataClass/WatchDogs_MongoWrapper.git
RUN pip install bson