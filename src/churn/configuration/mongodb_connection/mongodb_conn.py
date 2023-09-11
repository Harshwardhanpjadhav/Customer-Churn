import pymongo
import certifi
import os,sys
from src.churn.logger import logging
from src.churn.exception import CustomException
from src.churn.constants.environment_variable import EvironmentVariable as ev
from src.churn.constants.database import DATABASE_NAME,COLLECTION_NAME


class MongoDBConnection:
    client = None  # Initilizing client to None
    db = None  # Initilizing db to None
    collection = None  # Initilizing collection to None

    logging.info("Started MongoDB Connection >>>")
    def __init__(self,database_name = DATABASE_NAME,collection_name = COLLECTION_NAME)->None:

        # Creating a class variable 
        self.database_name = database_name
        self.collection_name = collection_name
        self.mongo_url = ev.mongo_url

        try:
            pass
            if MongoDBConnection.client != None:
                MongoDBConnection.client = pymongo.MongoClient(self.mongo_url,tlsCAFile=certifi.where())
                self.client = MongoDBConnection.client
                self.db = self.client[self.database_name]
                self.collection = self.db[self.collection_name]
            logging.info("MongoDB Connection Successfull >>>")
        except Exception as e:
            raise CustomException(sys,e)


