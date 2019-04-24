from setuptools import setup

setup(
 name='WatchDogs_MongoWrapper',    # This is the name of your PyPI-package.
 packages=['WatchDogs_MongoWrapper'],
install_requires=[
    'pymongo',
    'textblob',
    'pandas',
    'python-logstash'
    ],
 version='2.0',

)