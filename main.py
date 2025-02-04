from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import (DataIngestionConfig,TrainingPipelineConfig,
                                                  DataValidationConfig,DataTransformationConfig,
                                                  ModelTrainerConfig)
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        dataingestion = DataIngestion(data_ingestion_config) 
        data_validation_config = DataValidationConfig(training_pipeline_config)
   
        # Data ingestion
        logging.info("Initiated the data ingestion") 
        data_ingestion_artifact = dataingestion.initiate_data_ingestion()
        print(data_ingestion_artifact) 

        # Data Validation
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("Initiated data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")   

        # Data transformation   
        logging.info("Entered the data transformation pipeline")
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_Artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)

        # Model Trainer
        model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()





       
    except Exception as e:
        raise NetworkSecurityException(e,sys)