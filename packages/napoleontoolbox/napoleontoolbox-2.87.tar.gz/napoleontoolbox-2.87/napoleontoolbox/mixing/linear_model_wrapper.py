from napoleontoolbox.mixing import mixing_utility

import lightgbm as lgb

import numpy as np

from scipy.stats import uniform, randint

from sklearn.datasets import load_breast_cancer, load_diabetes, load_wine
from sklearn.metrics import auc, accuracy_score, confusion_matrix, mean_squared_error
from sklearn.model_selection import cross_val_score, GridSearchCV, KFold, RandomizedSearchCV, train_test_split
from sklearn.linear_model import Lasso
import xgboost as xgb
from sklearn import datasets, linear_model

class LinearModel():

    def __init__(self):
        self.model = linear_model.LinearRegression()

    def calibrate(self, X, y):#, method = 'standard'):
        # no hyper parameter to tune
        pass


    def fit(self, X_train, y_train, X_val, y_val):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        y_pred = self.model.predict(X_test)
        return y_pred


    def get_features_importance(self, features_names):
        run_importances = {}
        for (name, imp) in zip(features_names, self.model.coef_):
            run_importances[name] = imp
        return run_importances

