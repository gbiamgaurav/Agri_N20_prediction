# Agri_N20_prediction

## Create env
`conda create -p agri python==3.8 -y`

## Activate env
`conda activate agri/`

## install dependencies
`pip install -r requirements.txt`

## Run the commands
 
`sudo apt-get update -y`

`sudo apt-get upgrade`

`curl -fsSL https://get.docker.com -o get-docker.sh`

`sudo sh get-docker.sh`

`sudo usermod -aG docker ubuntu`

`newgrp docker`

`docker --version`

## Build a local docker image
`docker build -t n20_prediction .`

## Run the image
`docker run -p 8080:8080 n20_prediction`

## run the command below 
`gcloud builds submit --tag gcr.io/<PROJECT_ID>/<SOME_PROJECT_NAME>--timeout=2h`