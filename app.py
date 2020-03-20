from flask import Flask, render_template, request
import joblib
import pandas as pd
import math
import os
import statistics


import webbrowser

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

    df = joblib.load("./model/dataBrick_for_v3.joblib")
    ville = [request.form['ville']]

    ville = str(ville[0].upper())
    print(f"--------------------{ville}-------------")

    sclol = df[df['ville'].isin([f"{ville}"])]
    if len(sclol) < 4 :
        niv_confidence = "Faible, l'IA connait peut cette ville"
    elif len(sclol) >3 and len(sclol) <10 : 
        niv_confidence = "Normal, l'IA connait cette ville, mais manque un peu d'information"
    elif len(sclol) >=10 : 
        niv_confidence = "Forte, l'IA connait bien cette ville"
    if len(sclol) != 0 :
        pm_2 = statistics.mean(sclol["p_m2"])
    else :
        niv_confidence = "Faible, l'IA connait pas cette ville"
        pm_2 = statistics.mean(df["p_m2"])

    input_data = {
        "type_de_bien":[request.form['type_de_bien']],
        "nb_de_pieces":[request.form['nb_de_pieces']],
        "surface":[request.form['surface']],
        "ville":ville,
        "p_m2":pm_2,
        }

    input_data = pd.DataFrame(input_data)
    print(input_data)

    model = joblib.load("./model/model_xgb_v3.joblib")
    output = model.predict(input_data)
    output = math.exp (output)
    output = int(output)

    ui_display_var = f"{output}, confiance :  {niv_confidence}"

    return render_template('predict.html', classe = ui_display_var)

if __name__ == '__main__':
    app.run(debug=False)