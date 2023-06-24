# Agri_N20_prediction

## Create env
`conda create -p agri python==3.8 -y`

## Activate env
`conda activate agri/`

## install dependencies
`pip install -r requirements.txt`



## Build a local docker image
`docker build -t n20_prediction .`

## Run the image
`docker run -p 8080:8080 n20_prediction`

## run the command below 
`gcloud builds submit --tag gcr.io/<PROJECT_ID>/<SOME_PROJECT_NAME>--timeout=2h`