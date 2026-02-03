"""
MongoDB Connection - Core Infrastructure

This module provides the MongoDB connection wrapper used throughout the application.
It is the foundation layer that all database operations depend on.
"""

from pymongo import MongoClient
from nba_app.config import config


class Mongo:
    """
    MongoDB connection wrapper.

    Usage:
        mongo = Mongo()
        collection = mongo.db.games
        results = collection.find({...})
    """

    def __init__(self):
        self.client = MongoClient(config["mongo_conn_str"])
        self.db = self.client.heroku_jrgd55fg
