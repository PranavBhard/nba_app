from pymongo import MongoClient
from nba_app.config import config

class Mongo():
	def __init__(self):
		self.client = MongoClient(config["mongo_conn_str"])
		self.db = self.client.heroku_jrgd55fg

