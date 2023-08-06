import pymongo
from pprint import pprint


class MongoDB:
    def __init__(self, mongo_url: str):
        """
        Implements connections for MongoDB database and utilities for inserting tweets in collections.
        :param mongo_url: The coonection URL for the MongoDB in this format:
            mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
        """

        self.client = pymongo.MongoClient(mongo_url)
        self.database = self.client.database_tweet
        self.collection = self.database.collection_tweet
        self.admin = self.client.admin

    def insert_one(self, tweet: dict) -> None:
        """
        Insets a given tweet as a dictionary into the database.
        :param tweet: The input tweet as a dictionary
        """

        self.collection.insert_one(tweet)

    def get_db_status(self) -> str:
        """
        Returns the service status as a JSON.
        """

        return self.admin.command("serverStatus")
