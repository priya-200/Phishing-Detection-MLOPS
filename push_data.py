import os
import sys
import json
import pymongo
from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

# certifi provides set of root cetrificates that helps us to provide root connections.
import certifi
ce = certifi.where() # retrives the path and bundel it to the certifi and store in ce

import pandas as pd
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def csv_to_json_convertor(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop = True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.records = records
            self.collection = collection

            self.mongo_client = pymongo.MongoClient(MONGODB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__ == '__main__':
    FILE_PATH = "Network_Data\\phisingData.csv"
    DATABASE = "sample_mflix"
    COLLECTIONS = "NetworkData"
    networkobj = NetworkDataExtract()
    rec = networkobj.csv_to_json_convertor(FILE_PATH)
    print(rec)
    no_of_records = networkobj.insert_data_mongodb(rec,DATABASE,COLLECTIONS)
    print(no_of_records)
