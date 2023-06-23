import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from src.logger import logging
from src.exception import CustomException
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split


try:
    import joblib
    has_joblib = True
except ImportError:
    has_joblib = False
    import pickle


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        if has_joblib:
            joblib.dump(obj, file_path)
        else:
            with open(file_path, "wb") as file_obj:
                pickle.dump(obj, file_obj)
            
    except Exception as e:
        raise CustomException(e, sys)
    
    
def load_object(file_path):
    try:
        if has_joblib:
            obj = joblib.load(file_path)
        else:
            with open(file_path, "rb") as file_obj:
                obj = pickle.load(file_obj)
        return obj
    
    except Exception as e:
        raise CustomException(e, sys)
    
    
def evaluate_models(X_train, y_train, X_test, y_test, models, selected_model=None):
    try:
        report = {}

        if selected_model:
            model_names = [selected_model]
            model_list = [(selected_model, models[selected_model])]
        else:
            model_names = models.keys()
            model_list = models.items()

        for model_name, model in model_list:
            if isinstance(model, (RandomForestRegressor, XGBRegressor)):
                model.fit(X_train, y_train)  # Fit the model

                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)

                train_model_score = r2_score(y_train, y_train_pred)
                test_model_score = r2_score(y_test, y_test_pred)

                report[model_name] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)


# Main training logic
def train_model(train_data, test_data):
    try:
        logging.info("Splitting training and test input data")
        X_train, X_test, y_train, y_test = train_test_split(
            train_data[:, :-1],
            train_data[:, -1],
            test_size=0.2,
            random_state=42
        )

        models = {
            "RandomForest": RandomForestRegressor(),
            "XGBRegressor": XGBRegressor()
        }

        logging.info("Evaluating models before hyperparameter tuning")
        report_before_tuning = evaluate_models(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            models=models
        )
        logging.info(f"Model evaluation before hyperparameter tuning: {report_before_tuning}")

        param_grid = {
            "RandomForest": {
                "n_estimators": [100, 200, 300],
                "max_depth": [None, 5, 10],
                "min_samples_split": [2, 5, 10],
            },
            "XGBRegressor": {
                "n_estimators": [100, 200, 300],
                "max_depth": [3, 5, 7],
                "learning_rate": [0.1, 0.01, 0.001],
            },
        }

        best_model_score = 0.0
        best_model_name = ""
        best_model = None

        for model_name, model in models.items():
            logging.info(f"Performing hyperparameter tuning for {model_name}")

            grid_search = GridSearchCV(
                estimator=model,
                param_grid=param_grid[model_name],
                scoring="r2",
                cv=5
            )

            grid_search.fit(X_train, y_train)

            if grid_search.best_score_ > best_model_score:
                best_model_score = grid_search.best_score_
                best_model_name = model_name
                best_model = grid_search.best_estimator_

        if best_model is None or best_model_score < 0.5:
            raise CustomException("No best model found")

        logging.info(f"Best model found on both training and testing dataset")
        logging.info(f"Best parameters for {best_model_name}: {best_model.get_params()}")

        # Save the best_model using pickle
        save_object("artifacts/model.pkl", best_model)

        logging.info("Evaluating best model after hyperparameter tuning")
        report_after_tuning = evaluate_models(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            models={best_model_name: best_model}
        )
        logging.info(f"Model evaluation after hyperparameter tuning: {report_after_tuning}")

        y_pred = best_model.predict(X_test)
        score = r2_score(y_test, y_pred)

        return score

    except Exception as e:
        raise CustomException(e, sys)
