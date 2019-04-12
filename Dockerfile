# docker build --build-arg ssh_prv_key="$(cat ~/.ssh/id_rsa)" --build-arg ssh_pub_key="$(cat ~/.ssh/id_rsa.pub)" --squash .
FROM gcr.io/vaulted-zodiac-236605/watchdogs_dbpopulator

#Clone and Run the populator code
WORKDIR /home/WatchDogs_DatabasePopulator
RUN git pull && pip install --upgrade git+ssh://git@github.com/CUBigDataClass/WatchDogs_MongoWrapper.git
#RUN python populate_db.py
