import sys
import os

import pandas as pd
import numpy as np

from pymongo import MongoClient

from typing import List

from sklearn.model_selection import train_test_split

from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Configuration of Data Ingestion Config

from networksecurity.entity.config_entity import DataIngestionConfig

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGODB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        """
        Read data from mongo db database.
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            dataframe = pd.DataFrame(list(collection.find()))

            if "_id" in dataframe.columns.to_list():
                dataframe.drop(columns = ["_id"],inplace = True)

            dataframe.replace({"na":np.nan},inplace=True)

            logging.info("The data has been read from mongodb")

            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self,dataframe : pd.DataFrame):
        """
        It is highly recommanded not to read the data from database everytime you work on so it is best to store it
        in a folder where we can access it.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            
            # Creating a folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)

            logging.info(f"The raw data has been stored in {feature_store_file_path}")

            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        """
        Split the data into train and test data.
        """
        try:
            train_set,test_set = train_test_split(
                dataframe, test_size= self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting train and test data to file path.")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index = False,header = True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")
            


        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(train_file_path= self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)

            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)