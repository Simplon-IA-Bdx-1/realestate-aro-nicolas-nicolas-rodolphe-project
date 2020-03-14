from flask import Flask, render_template, request
from joblib import load
import pandas as pd
import numpy as np
import statistics

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/predict')
def get_predict():
    return "COuocu ejlkdjlqksjdlKQKSDJFKJQLFDS"

@app.route('/predict', methods=['POST'])
def post_predict():
    # input_data = [[
    #     request.form['sepal-length'],
    #     request.form['sepal-width'],
    #     request.form['petal-length'],
    #     request.form['petal-width']
    # ]]

    # input_data = pd.DataFrame.from_dict({'type_de_bien': ['maison'], 'nb_de_pieces': ['4'], 'surface': ['100'], 'ville': ['BORDEAUX'], 'p_m2': ['1000']})
 
    model = load('./models/model_xgb_v3.joblib')
    df = pd.read_csv("house_ligth.csv")
    df['ville'] = df['ville'].str.strip()

    x = pd.DataFrame()
    
    ask_ville = "BORDEAUX"

    x.loc[0,"type_de_bien"] = 'maison'
    x.loc[0,"nb_de_pieces"] = 4
    x.loc[0,"surface"] = 100
    x.loc[0,"ville"] = ask_ville

    count = 0

    for i in df["ville"]:
        df.loc[count,"p_m2"] = df.loc[count,"prix"]/df.loc[count,"surface"]
        count +=1

    sclol = df[df['ville'].isin([f"{ask_ville}"])]    

    if len(sclol) < 4 :
        niv_confidence = "Faible, l'Ia connait peut cette ville"
    elif len(sclol) >3 and len(sclol) <10 : 
        niv_confidence = "Normal, l'Ia connait cette ville, mais manque un peu d'information"
    elif len(sclol) >=10 : 
        niv_confidence = "Forte"
    
    if len(sclol) != 0 :
        k5 = statistics.mean(sclol["p_m2"])
    else :
        niv_confidence = "Faible, l'Ia connait pas cette ville"
        k5 = statistics.mean(df["p_m2"])

    x.loc[0,"p_m2"] = k5

    pred = model.predict(x)
    pred = np.exp(pred)

    print("Confiance de la prediction : ", niv_confidence)
    print(f"Prediction = {pred}")
    
    return str(pred)

if __name__ == '__main__':
    app.run()
