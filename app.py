from flask import Flask, render_template, request
import pickle
import pandas as pd

import webbrowser
from threading import Timer

webbrowser.open_new('http://127.0.0.1:5000')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/predict')
def get_predict():
    return render_template('get-prediction.html')

@app.route('/predict', methods=['POST'])
def predict():

    input_data = {"type_de_bien":[request.form['type_de_bien']],
        "année":[request.form['annee']],
        "nb_de_pieces":[request.form['nb_de_pieces']],
        "surface":[request.form['surface']],
        "ville":[request.form['ville']]
        }
    input_data = pd.DataFrame(input_data)

    model = pickle.load(open('./model/HPv2.sav', 'rb'))
    output = model.predict(input_data)

    return render_template('predict.html', classe = output)

if __name__ == '__main__':
    app.run(debug=False)