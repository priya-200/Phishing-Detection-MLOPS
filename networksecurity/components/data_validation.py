import pandas as pd
import numpy as np
import os
import sys

from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constants import training_pipeline
from networksecurity.utils.main_utils import utils

from scipy.stats import ks_2samp # For the drift checking

"""
What is data Drift?

Data drift refers to the change in the distribution of input data over time, which can negatively impact the performance of machine learning models.
"""

class DataValidation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config : DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = utils.read_yaml_file(training_pipeline.SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns : {number_of_columns}")
            logging.info(f"DataFrame has columns : {(len(dataframe.columns))}")

            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drif(self,base_df,current_df,threshold = 0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_dist = ks_2samp(d1,d2) # Compare the distribution of 2 samples
                if threshold <= is_sample_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    column : {
                        "p_value":float(is_sample_dist.pvalue),
                        "drift_status" : is_found
                    }
                })
            drift_report_file_path = self.data_validation_config.drift_report_file_path 

            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info("Report is dumped in drift_report path")
            utils.write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read the data from train and test 
            logging.info("Reading the data from train and test")

            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            logging.info("Dataset has been successfully read from the file path")

            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contail all columns.\n"
            
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contail all columns.\n"
            
            # Check data drift

            status = self.detect_dataset_drif(base_df=train_dataframe,current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,header=True,index = False
                )

            dir_path = os.path.dirname(self.data_validation_config.valid_test_file_path)
            os.makedirs(dir_path,exist_ok=True)

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,header=True,index = False
                )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)
