import sys
import pandas as pd
from src.exception import CustomException
from src.utils.utils import load_object
import os


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path=os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join("artifacts","proprocessor.pkl")
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)



class CustomData:
    def __init__(self,
        NH4: float,
        NO3: float,
        WFPS25cm: float,
        Replication: float,
        PP7: float,
        DAF_TD: float,
        AirT: float,
        PP2: float,
        Month: float,
        DAF_SD: float
        ):

        self.NH4 = NH4
        self.NO3 = NO3
        self.WFPS25cm = WFPS25cm
        self.Replication = Replication
        self.PP7 = PP7
        self.DAF_TD = DAF_TD
        self.AirT = AirT
        self.PP2 = PP2
        self.Month = Month
        self.DAF_SD = DAF_SD

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "NH4": [self.NH4],
                "NO3": [self.NO3],
                "WFPS25cm": [self.WFPS25cm],
                "Replication": [self.Replication],
                "PP7": [self.PP7],
                "DAF_TD": [self.DAF_TD],
                "AirT": [self.AirT],
                "PP2": [self.PP2],
                "Month": [self.Month],
                "DAF_SD": [self.DAF_SD]
                
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)