from pymongo import MongoClient


def mongo_connect(connection_string: str) -> MongoClient:
    return MongoClient(connection_string)
