from src.churn.configuration.mongodb_connection.mongodb_conn import MongoDBConnection
from src.churn.logger import logging
import sys
from src.churn.exception import CustomException
from src.churn.data_access import GetChurnData


if __name__ == '__main__':
    try:
        conn = GetChurnData()
        conn.export_collection_as_dataframe()
    except Exception as e:
        raise CustomException(e,sys)
