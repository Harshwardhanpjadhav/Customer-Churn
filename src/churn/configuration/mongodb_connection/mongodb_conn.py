import pymongo
import certifi
import os,sys
from src.churn.logger import logging
from src.churn.exception import CustomException
from src.churn.constants.environment_variable import EvironmentVariable as ev
from src.churn.constants.database import DATABASE_NAME,COLLECTION_NAME


class MongoDBConnection:
    '''
    MongoDB Connection Class
    '''
    client = None  # Initilizing client to None

    logging.info("Started MongoDB Connection >>>")
    def __init__(self,database_name = DATABASE_NAME)->None:
        try:
            # Fetching Mongo Url from env variable
            self.mongo_url = ev.mongo_url
            if MongoDBConnection.client is None: # when mongo client is None it will create a connection with given credentials
                MongoDBConnection.client = pymongo.MongoClient(self.mongo_url,tlsCAFile=certifi.where())
                self.client = MongoDBConnection.client
                self.db = self.client[database_name]
            logging.info("MongoDB Connection Successfull >>>")
        except Exception as e:
            raise CustomException(e,sys)


