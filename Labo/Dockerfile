FROM python:3.7-buster

RUN pip install numpy==1.16.2 pandas==0.23.4 mysql-connector-python==8.0.19 beautifulsoup4==4.8.2 joblib==0.14.1 scikit-learn==0.22.1 xgboost==0.90 azureml-sdk==1.0.85 

COPY . /usr/src/Labo
WORKDIR /usr/src/Labo

CMD python indusManage.py
