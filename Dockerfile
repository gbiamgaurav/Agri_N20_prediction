FROM python:3.8-slim-buster
EXPOSE 8080
RUN apt update -y && apt install awscli -y

WORKDIR /app 

COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]