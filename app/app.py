from flask import Flask, render_template, request
from joblib import load
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/predict')
def post_predict():
    # input_data = [[
    #     request.form['sepal-length'],
    #     request.form['sepal-width'],
    #     request.form['petal-length'],
    #     request.form['petal-width']
    # ]]

    # input_data = pd.DataFrame.from_dict({'type_de_bien': ['maison'], 'nb_de_pieces': [4], 'surface': [100], 'ville': ['BORDEAUX'], 'p_m2': [1000]})
    # model = load('./models/model_xgb_v3.joblib')
    # output = model.predict(input_data)
    # print(output)

    return {'precision': '99.99', 'price': '100 000'}

if __name__ == '__main__':
    app.run()
