import numpy as np
import pandas as pd
from joblib import load


class Model:
    """ Import your json with new inputs, return a prediction by Ia"""

    def make_prediction(self, input_data):
        print(input_data)
        x = pd.DataFrame()
        x.loc[0, "type_de_bien"] = input_data['type_de_bien']
        x.loc[0, "nb_de_pieces"] = input_data['nb_de_pieces']
        x.loc[0, "surface"] = input_data['surface']
        x.loc[0, "ville"] = input_data['ville']

        model = load('Models/model_xgb_v2.joblib')

        pred = model.predict(x)
        pred = np.exp(pred)
        return pred[0]
