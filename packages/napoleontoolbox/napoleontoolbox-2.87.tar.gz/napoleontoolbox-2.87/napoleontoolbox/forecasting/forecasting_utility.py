import lightgbm as lgb

import numpy as np

from scipy.stats import uniform, randint

from sklearn.datasets import load_breast_cancer, load_diabetes, load_wine
from sklearn.metrics import auc, accuracy_score, confusion_matrix, mean_squared_error
from sklearn.model_selection import cross_val_score, GridSearchCV, KFold, RandomizedSearchCV, train_test_split
from sklearn.linear_model import Lasso
import xgboost as xgb
from sklearn import datasets, linear_model

from napoleontoolbox.forecasting import lgbm_model_wrapper
from napoleontoolbox.forecasting import arima_model_wrapper
from napoleontoolbox.forecasting import sma_model_wrapper
from napoleontoolbox.forecasting import simple_threshold_model_wrapper
from napoleontoolbox.forecasting import simple_baseline
from napoleontoolbox.forecasting import anova_like_model

from abc import ABC, abstractmethod


def instantiate_model(method = 'default',idios = {}):
    if method == 'lgbm':
        return lgbm_model_wrapper.LGBMModel(**idios)
    if method == 'arima':
        return arima_model_wrapper.ArimaModel(**idios)
    if method == 'sma':
        return sma_model_wrapper.SmaModel(**idios)
    if method == 'simple_threshold':
        return simple_threshold_model_wrapper.SimpleThresholdModel(**idios)
    if method == 'simple_baseline':
        return simple_baseline.BaselineModel(**idios)
    if method == 'anova_like_model':
        return anova_like_model.AnovaLikeModel(**idios)

class AbstractForecasterWrapper(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def calibrate(self, X, y):#, method = 'standard'):
        pass

    @abstractmethod
    def fit(self, X_train, y_train, X_val, y_val):#, method = 'standard'):
        pass

    @abstractmethod
    def predict(self, X_test):#, method = 'standard'):
        pass

    @abstractmethod
    def get_features_importance(self, features_names):#, method = 'standard'):
        pass
