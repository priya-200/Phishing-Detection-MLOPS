from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import yaml
import os
import sys

import pandas as pd
import numpy as np
import dill
import pickle

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path : str) -> dict:
    try:
        with open(file_path,"rb") as yaml_file:
            logging.info(f"Returning the yaml file in the file_path {file_path}")
            return yaml.safe_load(yaml_file) # The output is in the form of dict
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def write_yaml_file(file_path : str,content : object,replace : bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
            logging.info(f"The ymal file has been saved in the file_path {file_path} and the content is {content}")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array_data(file_path: str,array: np.array):
    """
    Saves numpy array data to file
    file_path : str Location of file to save
    array : np.array Data to be saved.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
        logging.info("Saved the numpy array object")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_object(file_path: str,obj : object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Saved the object")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
            logging.info(f"save the numpy object in the file_path {file_path}")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_object(file_path:str) -> object:
    try:
        if not os.path.exists(file_path):
            raise NetworkSecurityException(f"The file {file_path} doesn't exist", None)
        
        if not file_path.endswith(".pkl"):  # Ensure it's a pickle file
            raise NetworkSecurityException(f"Invalid file format: {file_path}. Expected a .pkl file", None)

        with open(file_path, "rb") as file_obj:
            logging.info(f"Loading the object from {file_path}")
            return pickle.load(file_obj)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array_data(file_path:str) ->object:
    try:
        if not os.path.exists(file_path):
            raise NetworkSecurityException(f"The file path {file_path} doesn't exist")
        logging.info(f"Loading the numpy array data from the file path {file_path}")
        return np.load(file_path, allow_pickle=True)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    


"""def load_numpy_array_data(file_path: str):
    try:
        if not file_path.endswith(".npy"):
            raise NetworkSecurityException(f"Expected a .npy file but got {file_path}", None)

        return np.load(file_path, allow_pickle=True)  # ✅ Load NumPy array correctly
    except Exception as e:
        raise NetworkSecurityException(f"Error loading NumPy array from {file_path}", e)"""

def evaluate_model(X_train,X_test,y_train,y_test,models,param):
    try:
       report = {}

       for i in range(len(list(models))):
           model = list(models.values())[i]
           para=param[list(models.keys())[i]]

           gs = GridSearchCV(model,para,cv=3)
           gs.fit(X_train,y_train)

           model.set_params(**gs.best_params_)
           model.fit(X_train,y_train)
           y_train_pred = model.predict(X_train)

           y_test_pred = model.predict(X_test)

           train_model_score = r2_score(y_train, y_train_pred)

           test_model_score = r2_score(y_test, y_test_pred)

           report[list(models.keys())[i]] = test_model_score

       return report

    except Exception as e:
       raise NetworkSecurityException(e, sys)