import streamlit as st
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

def main():
    st.title('Agri N20 Prediction Web App')

    nh4 = st.slider('NH4', 1.0, 230.0, step=0.1)
    no3 = st.slider('NO3', 0.0, 240.0, step=0.1)
    wfps25cm = st.slider('WFPS25cm', 0.0, 1.0, step=0.01)
    replication = st.selectbox('Replication', ['R1', 'R2', 'R3', 'R4', 'R5'])
    pp7 = st.slider('PP7', 0.0, 270.0, step=0.1)
    daf_td = st.slider('DAF_TD', 1, 720)
    air_t = st.slider('AirT', -30.0, 40.0, step=0.1)
    pp2 = st.slider('PP2', 0.0, 100.0, step=0.1)
    daf_sd = st.slider('DAF_SD', 0, 680)
    DataUse = st.selectbox("DataUse", ["Building", "Testing"])
    Vegetation = st.selectbox("Vegetation", ["Corn", "GLYMX", "TRIAE"])

    if st.button('Predict'):
        try:
            data = CustomData(
                NH4=float(nh4),
                NO3=float(no3),
                WFPS25cm=float(wfps25cm),
                Replication=replication,
                PP7=float(pp7),
                DAF_TD=int(daf_td),
                AirT=float(air_t),
                PP2=float(pp2),
                DAF_SD=int(daf_sd),
                DataUse=DataUse,
                Vegetation=Vegetation
            )

            pred_df = data.get_data_as_data_frame()

            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)

            st.success(f'The prediction result is: {results[0]}')

        except Exception as e:
            st.error(f'An error occurred: {str(e)}')

if __name__ == '__main__':
    main()
