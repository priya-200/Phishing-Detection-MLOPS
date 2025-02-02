import os
import sys
import numpy as np
import pandas as pd

"""
Definign common constant variable for training pipeline
"""

TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "NetworkData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("Data Schema","Schema.yaml")

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "sample_mflix"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data validation related constants starting with DATA_VALIDATION var name.
"""

DATA_VALIDATION_DIR_NAME: str = "Data Validation"
DATA_VALIDATION_VALID_DIR: str = "Validated"
DATA_VALIDATION_INVALID_DIR: str = "Invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "Drift Report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "Report.yaml"

"""
Data Transformation related constants starts with DATA_TRANSFORMATION VAR NAME
"""

DATA_TRANSFORMATION_DIR_NAME: str = "Data Transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

# KNN imputer to replace the missing value.
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values":np.nan,
    "n_neighbors": 3,
    "weights" : "uniform"
}