# docker build --build-arg ssh_prv_key="$(cat ~/.ssh/id_rsa)" --build-arg ssh_pub_key="$(cat ~/.ssh/id_rsa.pub)" --squash .
FROM gcr.io/vaulted-zodiac-236605/watchdogs_dbpopulator_base

## Travis Testing
WORKDIR /home
RUN git clone git@github.com:CUBigDataClass/WatchDogs_DatabasePopulator.git
RUN pip install --upgrade git+ssh://git@github.com/CUBigDataClass/WatchDogs_MongoWrapper.git
RUN pip install --upgrade git+ssh://git@github.com/CUBigDataClass/RedisWrapper.git
RUN pip install pykafka
RUN pip install kafka-python
WORKDIR /home/WatchDogs_DatabasePopulator

#RUN python populate_db.py
