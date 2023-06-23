import os
import sys
from dataclasses import dataclass
from sklearn.metrics import r2_score
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from src.exception import CustomException
from src.logger import logging
from src.utils.utils import save_object, evaluate_models
from sklearn.model_selection import GridSearchCV


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "XGBRegressor": XGBRegressor()
            }
            params = {
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256],
                    #"max_depth": [None, 5, 10],
                    #"min_samples_split": [2, 5, 10]
                    
                },

                "XGBRegressor": {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256],
                    #"max_depth": [3, 5, 7],
                }

            }

            logging.info("Evaluating models before hyperparameter tuning")
            model_report = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                           models=models, param=params)
            logging.info(f"Model evaluation before hyperparameter tuning: {model_report}")

            # To get the best model score from the dictionary
            best_model_score = max(sorted(model_report.values()))

            # To get the best model name from the dictionary
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score < 0.5:
                raise CustomException("No best model found")

            logging.info(f"Best model found on both training and testing dataset")

            logging.info(f"Hyperparameters for {best_model_name}: {best_model.get_params()}")

            best_model.fit(X_train, y_train)  # Refit the model on the entire training data

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)

            logging.info("Evaluating best model after hyperparameter tuning")
            logging.info(f"Best model name: {best_model_name}")
            logging.info(f"R2 score after hyperparameter tuning: {r2_square}")

            return r2_square, best_model_name

        except Exception as e:
            raise CustomException(e, sys)
