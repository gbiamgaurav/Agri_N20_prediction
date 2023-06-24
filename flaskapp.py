from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/predict_datapoint', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        try:
            data = CustomData(
                NH4=float(request.form['NH4']),
                NO3=float(request.form['NO3']),
                WFPS25cm=float(request.form['WFPS25cm']),
                Replication=request.form['Replication'],
                PP7=float(request.form['PP7']),
                DAF_TD=int(request.form['DAF_TD']),
                AirT=float(request.form['AirT']),
                PP2=float(request.form['PP2']),
                DAF_SD=int(request.form['DAF_SD']),
                DataUse=request.form['DataUse'],
                Vegetation=request.form['Vegetation']
            )

            pred_df = data.get_data_as_data_frame()

            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)

            return render_template('home.html', results=results[0])

        except Exception as e:
            error_message = f"Error occurred: {str(e)}"
            return render_template('home.html', error=error_message)

""" if __name__ == "__main__":
    app.run(host='0.0.0.0') """
