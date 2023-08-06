from pathlib import Path
import json
import gzip
import os

from tweepy import OAuthHandler, Stream, StreamListener

from twimer.database import MongoDB
from twimer.twitter_connection import TwitterConnection


class Twimer:
    def __init__(
        self,
        file_path=Path("tweets_raw"),
        max_tweet_num=100,
        consumer_key=None,
        consumer_secret=None,
        access_token=None,
        access_token_secret=None,
        storage_method=None,
        mongo_url=None,
    ):
        """
        Implements the main module to stream tweets and store them.
        :param consumer_key: Provided by Twitter API
        :param consumer_secret: Provided by Twitter API
        :param access_token: Provided by Twitter API
        :param access_token_secret: Provided by Twitter API
        :param storage_method: The storage destination that can be "file/plain", "file/targz", or "mongodb"
        :param file_path: The file path, if the storage_method is files
        :param mongo_url: The MongoDB connection if the storage_method is MongoDB. In this format:
            mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
        :param max_tweet_num: The maximum number of tweeter to get
        """

        # storage
        if storage_method in ("plain", "targz"):

            if file_path is None:
                raise Exception(
                    "Pass file_path for the plain and targz storage methods"
                )
            elif not os.path.isdir(file_path):
                try:
                    file_path.mkdir(parents=True, exist_ok=True)
                except:
                    raise Exception(
                        f"Cannot create the target directory {file_path} to store tweets"
                    )

            self.storage_param = file_path

        elif storage_method == "mongodb":
            if mongo_url is None:
                raise Exception("Pass mongo_url for the mongodb storage method")

            try:
                self.storage_param = MongoDB(mongo_url)
            except:
                print(f"MongoDB connection error. Could not connect to {mongo_url}")

        else:
            raise Exception(
                f"{storage_method} is not a valid storage method. "
                f"The current options are: plain, targz, and mongodb"
            )

        # credentials
        if not consumer_key:
            if True:
                consumer_key = os.environ["CONSUMER_KEY"]
                consumer_secret = os.environ["CONSUMER_SECRET"]
                access_token = os.environ["ACCESS_TOKEN"]
                access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
            # except Exception as e:
            #     print(f"Could not reteive environment variables for credentials.\n{e}")

        self.storage_method = storage_method
        self.max_tweet_num = max_tweet_num

        # tweepy Stream
        if True:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.tweeter_connection = TwitterConnection(
                self.storage_method, self.storage_param, self.max_tweet_num
            )
            self.stream = Stream(self.auth, self.tweeter_connection)
        else:
            print("Invalid API credentials")

    def start_streaming(self, filters: str, languages: str = ["en"]) -> None:
        """
        Start the process of streaming, given a list of filters and languages.
        :param filters: The list of filters, each of them is an string
        :param languages: The list of languages, each of them is an string
        """

        self.stream.filter(track=filters, languages=languages)
