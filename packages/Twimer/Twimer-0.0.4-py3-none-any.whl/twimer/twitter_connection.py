import os
import json
import gzip
from pathlib import Path
from tweepy import OAuthHandler, Stream, StreamListener

from twimer.database import MongoDB


class TwitterConnection(StreamListener):
    def __init__(self, storage_method: str, storage_param: str, max_tweet_num: int):
        """
        Implements connection to Twitter suing Tweepy Stream.
        :param storage_method: The storage destination that can be "file/plain", "file/targz", or "mongodb"
        :param storage_param: The parameter for storage, a directory path for files and connection URL for MongoDB
        :param max_tweet_num: The maximum number of tweets to get
        """

        self.storage_method = storage_method
        self.storage_param = storage_param
        self.max_tweet_num = max_tweet_num
        self.tweet_num = 0

    def on_data(self, tweet: str) -> None:
        """
        Called when a tweet is retrieved and store it.
        :param tweet: The tweet as string
        """

        try:

            # retrieve tweet ID
            tweet_id = json.loads(tweet)["id"]

            # storage
            if self.storage_method == "plain":
                with open(
                    Path(self.storage_param) / Path(f"{tweet_id}.json"), "w"
                ) as fout:
                    fout.write(tweet)
            elif self.storage_method == "targz":
                with gzip.GzipFile(
                    Path(self.storage_param) / Path(f"{tweet_id}.json.gz"), "w"
                ) as fout:
                    fout.write(tweet.encode("utf-8"))
            elif self.storage_method == "mongodb":
                self.storage_param.insert_one(json.loads(tweet))

            # check the number of tweets so far
            self.tweet_num = self.tweet_num + 1
            if self.tweet_num > self.max_tweet_num:
                pass

        except Exception as e:
            print(f"runtime error: {e}")

    def on_error(self, status: str) -> None:
        """
        Called if there is an error, prints the status.
        :param status: The status as string
        """

        print(f"error: {status}")
