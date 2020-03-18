import json
import joblib
import numpy as np
import pandas as pd
from azureml.core.model import Model

# Called when the service is loaded
def init():
    global model
    # Get the path to the registered model file and load it
    model_path = Model.get_model_path('fastv3')
    model = joblib.load(model_path)

# Called when a request is received
def run(xx):
    try:
        v1 = xx[0] 
        v2 = xx[1]  
        v3 = xx[2]
        v4 = xx[3]
        v5 = xx[4]

        x = pd.DataFrame()
        x.loc[0,"type_de_bien"] = f"{v1}"
        x.loc[0,"nb_de_pieces"] = v2
        x.loc[0,"surface"] = v3
        x.loc[0,"ville"] = f"{v4}"
        x.loc[0,"p_m2"] = v5

        predictions = model.predict(x)
        predictions = np.exp(predictions)
        return predictions.tolist()
    except Exception as e:
        result = str(e)
        return result
