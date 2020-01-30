import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore") 

from joblib import load
import xgboost

class iaForHouseFast() :
    """ Import your json with new inputs, return a prediction by Ia"""

    @staticmethod
    def prediction():

        x = pd.DataFrame()
        x.loc[0,"type_de_bien"] = "maison"
        x.loc[0,"nb_de_pieces"] = 5
        x.loc[0,"surface"] = 100
        x.loc[0,"ville"] = "PORT STE FOY ET PONCHAPT"

        model = load('model_xgb_v2.joblib')

        pred = model.predict(x)

        pred = np.exp(pred)

        print(f"Prediction = {pred}")
        
        return pred  


iaForHouseFast.prediction()        

