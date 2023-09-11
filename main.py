from src.churn.configuration.mongodb_connection.mongodb_conn import MongoDBConnection
from src.churn.logger import logging


if __name__ == '__main__':
    conn = MongoDBConnection()
    # logging.info(conn)
