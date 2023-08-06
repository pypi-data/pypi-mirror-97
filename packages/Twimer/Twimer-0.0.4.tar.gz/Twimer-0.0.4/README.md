# twimer
Stream Tweets into Your Favorite Databases

[![Build Status](https://circleci.com/gh/owhadi/twimer.svg)](https://app.circleci.com/pipelines/github/owhadi)

Analyzing tweets reveals very interesting insights about events in a specific time and location, people's opinions 
about the news, etc.
twimer aims to make the data collection easier for you so you can focus on your data analysis only!
This tool stores tweets with certain keywords and from specific geographic regions into JSON files or MongoDB databases.

## Twitter API
To use twimer, you need to obtain _CONSUMER_KEY_, _CONSUMER_SECRET_, _ACCESS_TOKEN_, _ACCESS_TOKEN_SECRET_ 
from [Twitter Developer](https://developer.twitter.com/en). You can either set these as environment variables or directly pass them to twimer.

## Installation
Simply install this package by running the following command:
 ```bash
pip install twimer 
```

## Usage
In the current version, you can stream the tweets using keywords and store them in files (JSON and JSON.tar.gz)
and MongoDB databases.

- To store tweets that contain _keyword1_ and _keyword2_ keywords as JSON (tar.gz) files into the `my_path` directory:
```python
import twimer

stream_tweet = twimer.Twimer(CONSUMER_KEY, 
                             CONSUMER_SECRET, 
                             ACCESS_TOKEN, 
                             ACCESS_TOKEN_SECRET, 
                             storage_method='targz', 
                             file_path=my_path)
stream_tweet.start_streaming(filters=['keyword1', 'keyword2'])
```

- To store the tweets in a MongoDB database using url `mongo_url`:
```python
import twimer

stream_tweet = twimer.Twimer(CONSUMER_KEY, 
                             CONSUMER_SECRET, 
                             ACCESS_TOKEN, 
                             ACCESS_TOKEN_SECRET, 
                             storage_method='mongodb', 
                             mongo_url=mongo_url)
stream_tweet.start_streaming(filters=['keyword1', 'keyword2'])
```

The `my_url` is in _mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]_ format. If you set your Twitter credentials as environment variables, you do not need to pass them and can simply run the following code.
```python
import twimer

stream_tweet = twimer.Twimer(storage_method='targz', 
                             file_path=my_path)
stream_tweet.start_streaming(filters=['keyword1', 'keyword2'])
```

## Local MongoDB Database
To store tweets using MongoDB locally, you can use docker-compose by running `docker-compose up`. Note that you need to install docker on your system before running this command. To view the MongoDB Express dashboard, simply open `http://localhost:8081` on your browser. The default username and password for MongoDB are set to _root_ and _example_ and you need to update them to prevent unauthorized access to your local database.

## Contribution
You are very welcome to contribute to this project with your code (as pull-requests), mention the bugs, or ask for new 
features (as GitHub Issues), or just tell your friends about it! 

You can also directly contact me by [email](mkareshk@outlook.com).
 