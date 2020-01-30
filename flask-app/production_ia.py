import numpy as np
import pandas as pd
from joblib import load
import os


class Model:
    """ Import your json with new inputs, return a prediction by Ia"""

    def make_prediction(self, input_data):
        print(input_data)
        x = pd.DataFrame()
        x.loc[0, "type_de_bien"] = input_data['type_de_bien']
        x.loc[0, "nb_de_pieces"] = input_data['nb_de_pieces']
        x.loc[0, "surface"] = input_data['surface']
        x.loc[0, "ville"] = input_data['ville']

        model = load(
            os.path.abspath('flask-app/model_xgb_v2.joblib')
            )

        pred = model.predict(x)
        pred = np.exp(pred)

        print(pred)
        return pred.tolist()


# input_data = {
#     'type_de_bien': 'maison',
#     'nb_de_pieces': '2',
#     'surface': '20',
#     'ville': 'ARCACHON'}
# model = Model()
# model.make_prediction(input_data)