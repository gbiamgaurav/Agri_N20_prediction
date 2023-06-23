from flask import Flask,request,render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
from src.logger import logging

application = Flask(__name__)

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            NH4=request.form.get('NH4'),
            NO3=request.form.get('NO3'),
            WFPS25cm=request.form.get('WFPS25cm'),
            Replication=request.form.get('Replication'),
            PP7=request.form.get('PP7'),
            DAF_TD=request.form.get('DAF_TD'),
            Journey_year=request.form.get('Journey_year'),
            AirT=request.form.get('AirT'),
            PP2=request.form.get('PP2'),
            Month=request.form.get('Month'),
            DAF_SD=request.form.get('DAF_SD'),
            
        )

        pred_df=data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df)
        return render_template('home.html',results=results[0])
     

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

        
     
