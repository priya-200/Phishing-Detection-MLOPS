from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import os
import sys

from sklearn.metrics import f1_score,precision_score,recall_score,accuracy_score

def get_classification_score(y_true,y_pred) -> ClassificationMetricArtifact:
    try:
        logging.info("Calculating the models metric inside the get_classification_score from classification_metric module.")
        model_f1_score = f1_score(y_true,y_pred)
        model_recall_score = recall_score(y_pred=y_pred,y_true=y_true)
        model_precision_score = precision_score(y_true=y_true,y_pred=y_pred)
        model_accuracy = accuracy_score(y_true=y_true,y_pred=y_pred)

        classification_metric = ClassificationMetricArtifact(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score,
            accuracy=model_accuracy
        )
        logging.info("Returning the classification metrix in the form of ClassificationMetricArtifact")

        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)