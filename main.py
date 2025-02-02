from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
import sys

if __name__ == "__main__":
    try:
       training_pipeline_config = TrainingPipelineConfig()
       data_ingestion_config = DataIngestionConfig(training_pipeline_config)
       dataingestion = DataIngestion(data_ingestion_config) 

       logging.info("Initiated the data ingestion")

       data_ingestion_artifact = dataingestion.initiate_data_ingestion()
       print(data_ingestion_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)