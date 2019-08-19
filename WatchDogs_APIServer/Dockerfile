FROM gcr.io/vaulted-zodiac-236605/watchdogs_dbpopulator_base

WORKDIR /home
RUN pip install flask
RUN pip install --upgrade git+ssh://git@github.com/CUBigDataClass/WatchDogs_MongoWrapper.git
RUN pip install --upgrade git+ssh://git@github.com/CUBigDataClass/RedisWrapper.git
RUN git clone git@github.com:CUBigDataClass/watchodogs_api_server.git
WORKDIR /home/watchodogs_api_server
#RUN python app.py