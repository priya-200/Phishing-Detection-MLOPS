import os
import sys

import mlflow

from networksecurity.entity.config_entity import ModelTrainerConfig,DataTransformationConfig
from networksecurity.constants import training_pipeline 
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils import utils
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import(
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)

class ModelTrainer:
    def __init__(self,model_trainer_config: ModelTrainerConfig,data_transformation_artifact : DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def track_mlflow(self,best_model,classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score
            accuracy = classification_metric.accuracy

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.log_metric("accuracy",accuracy)
            mlflow.sklearn.log_model(best_model,"model")

        
    def train_model(self,X_train,y_train,X_test,y_test):
        """
        This fuction is to train our model
        params:
        X_train :
            Training features

        y_train: 
            target feature of the train dataset
        """
        logging.info("Entered the train_model function inside the model_trainer class")

        models = {
            "Random Forest":RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting" : GradientBoostingClassifier(),
            "Logistic Regression" : LogisticRegression(),
            "AdaBoost Classifier" : AdaBoostClassifier()
        }
        
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost Classifier":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }  
        }

        model_report : dict = utils.evaluate_model(X_train = X_train,X_test = X_test,y_train = y_train,y_test = y_test,models = models,param = params)

        # To get the best model score from the dict
        logging.info("Got the best model from hyperparameter tying.")
        best_model_score = max(sorted(model_report.values()))

        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)

        classification_train_metrix = get_classification_score(y_pred=y_train_pred,y_true=y_train)

        # Tracking the experiments with mlflow
        self.track_mlflow(best_model,classification_train_metrix)

        y_test_pred = best_model.predict(X_test)

        classification_test_metrix = get_classification_score(y_pred=y_test_pred,y_true=y_test)

        self.track_mlflow(best_model,classification_test_metrix)


        preprocessor = utils.load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        network_model = NetworkModel(preprocessor=preprocessor,model=best_model)
        utils.save_object(self.model_trainer_config.trained_model_file_path,obj=NetworkModel)

        # Model Trainer Artifact

        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
        train_metric_artiface=classification_train_metrix,test_metric_artiface=classification_test_metrix
        )
        return model_trainer_artifact


    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            logging.info("Initiating the load_numpy_array_data inside the initiate_model_trainer")
            train_arr = utils.load_numpy_array_data(train_file_path)
            test_arr = utils.load_numpy_array_data(test_file_path)

            X_train,y_train,X_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            model_trainer_artifact = self.train_model(X_train=X_train,X_test=X_test,y_test=y_test,y_train=y_train)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)