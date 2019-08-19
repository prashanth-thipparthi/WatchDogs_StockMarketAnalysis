# docker build --build-arg ssh_prv_key="$(cat ~/.ssh/id_rsa)" --build-arg ssh_pub_key="$(cat ~/.ssh/id_rsa.pub)" --squash .
FROM gcr.io/vaulted-zodiac-236605/watchdogs_dbpopulator_base


WORKDIR /home
RUN git clone git@github.com:CUBigDataClass/WatchDogs_MongoWrapper.git
RUN pip install --upgrade git+ssh://git@github.com/CUBigDataClass/WatchDogs_MongoWrapper.git
WORKDIR /home/WatchDogs_MongoWrapper/test_cases
RUN pip install tweepy
RUN python test_cases.py