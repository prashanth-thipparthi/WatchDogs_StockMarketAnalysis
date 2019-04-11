from setuptools import setup

setup(
 name='WatchDogs_MongoWrapper',    # This is the name of your PyPI-package.
 packages=['WatchDogs_MongoWrapper'],
install_requires=[
    'pymongo',
    'textblob'
    ],
 version='2.0',

)