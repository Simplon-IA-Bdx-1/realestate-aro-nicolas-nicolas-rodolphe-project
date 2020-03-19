from flask import Flask, render_template, request
import joblib
import pandas as pd
import math
import os


import webbrowser

webbrowser.open_new('http://127.0.0.1:5000')

# print(input_data)
# print(output)
# os.system("pause")
# exit()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/predict')
def get_predict():
    return render_template('get-prediction.html')

@app.route('/predict', methods=['POST'])
def predict():

    input_data = {
        "type_de_bien":[request.form['type_de_bien']],
        "nb_de_pieces":[request.form['nb_de_pieces']],
        "surface":[request.form['surface']],
        "ville":[request.form['ville']],
        "p_m2":[request.form['p_m2']]
        }
    input_data = pd.DataFrame(input_data)

    model = joblib.load("./model/model_xgb_v3.joblib")
    output = model.predict(input_data)
    output = math.exp (output)
    return render_template('predict.html', classe = output)

if __name__ == '__main__':
    app.run(debug=False)