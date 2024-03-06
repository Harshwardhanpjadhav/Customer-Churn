from dotenv import find_dotenv, load_dotenv
from dataclasses import dataclass
import os,sys

# find_dotenv function finds the dot .env file from file 
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

@dataclass
class EvironmentVariable:
    """
    This class is used to fetch environment variable from .env file
    """
    # MongoDB Url fetched from .env file (.env file is not pushed in github)
    mongo_url = os.getenv('MONGODB_URL')