import pandas as pd
import yaml
import os
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constants import training_pipeline


df = pd.read_csv("Network_Data\\phisingData.csv")  

SCHEMA_FILE_PATH = training_pipeline.SCHEMA_FILE_PATH
dir_path = os.path.dirname(SCHEMA_FILE_PATH)
dir_path = os.makedirs(dir_path,exist_ok=True)

def infer_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "int"
    elif pd.api.types.is_float_dtype(dtype):
        return "float"
    elif pd.api.types.is_bool_dtype(dtype):
        return "bool"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "datetime"
    else:
        return "string"

# Generate schema structure
schema = {
    "columns": [{col: infer_dtype(df[col].dtype)} for col in df.columns],
    "numerical_columns": [col for col in df.columns if infer_dtype(df[col].dtype) in ["int", "float"]],
    "categorical_columns": [col for col in df.columns if infer_dtype(df[col].dtype) == "string"]
}

# Save to schema.yaml
with open(SCHEMA_FILE_PATH, "w") as file:
    yaml.dump(schema, file, default_flow_style=False)

print("schema.yaml generated successfully!")
