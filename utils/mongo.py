from .utils import Singleton
from pymongo import MongoClient

class Mongo(MongoClient, Singleton):
    pass



