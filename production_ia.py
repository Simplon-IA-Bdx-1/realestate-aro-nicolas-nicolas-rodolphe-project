import pandas as pd
import numpy as np
import statistics

import warnings
warnings.filterwarnings("ignore") 

from joblib import load
# import xgboost

class iaForHouseFast() :
    """ Set your values, return a prediction by Ia"""

    @staticmethod
    def prediction():

        df = pd.read_csv("Base_Files/house_ligth.csv")
        df['ville'] = df['ville'].str.strip()

        ask_bien = str(input("Quel type de bien ? appartement ou maison ?"))
        ask_piece = int(input("Combien de piéces ? "))
        ask_surface = int(input("La surface habitable en m2 ? "))
        ask_ville = str(input("Dans quelle ville ? "))

        x = pd.DataFrame()
        x.loc[0,"type_de_bien"] = ask_bien
        x.loc[0,"nb_de_pieces"] = ask_piece
        x.loc[0,"surface"] = ask_surface
        x.loc[0,"ville"] = f"{ask_ville}"
   
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

        model = load('model_xgb_v3.joblib')

        pred = model.predict(x)
        pred = np.exp(pred)

        print("Confiance de la prediction : ", niv_confidence)
        print(f"Prediction = {pred}")
        
        return pred  


iaForHouseFast.prediction()        

