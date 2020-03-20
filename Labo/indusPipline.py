import os
import requests
from bs4 import BeautifulSoup

import csv
import mysql
import pandas as pd
import numpy as np
from mysql.connector import (connection)
from sec import secureLog as SL ### See readme
from joblib import dump

from random import randrange
from datetime import date

from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_error as MAE
import statistics

import xgboost

class Sqldd():
    """Class return connection & cursor for bdd,you need to close them, for import log's see readme"""

    def __init__(self) :
        self.log_user = SL.sqlLogUser
        self.log_pass = SL.sqlLogPass
        self.log_host = SL.sqlLogHost
        self.log_bdd = SL.sqlLogDatabase
        self.log_port = SL.sqlLogPort
    
    def get_bdd_co(self):
        cnx = mysql.connector.connect(user=f'{self.log_user}', password=f'{self.log_pass}',
                              host=f'{self.log_host}',
                              database=f'{self.log_bdd}', port=f'{self.log_port}')

        cnx = connection.MySQLConnection(user=f'{self.log_user}', password=f'{self.log_pass}',
                              host=f'{self.log_host}',
                              database=f'{self.log_bdd}', port=f'{self.log_port}')

        cursor = cnx.cursor(named_tuple=True)

        return cnx, cursor

class Scraper:
    """ Class call for scrap Url's from source + scraping data to database """

    def __init__(self):
        self.base_url = 'https://www.fnaim-gironde.com'
        
    def get_soup(self, page):
        try:
            soup = BeautifulSoup(page.text, 'html.parser')
        except AttributeError as e:
            print(f'bs4 error: {e}')
            return None
        return soup
    
    def get_response(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'error in request: {e}')
            return None
        return r
        
    def get_all_sales_csv(self):
        url = f'{self.base_url}/achat-immobilier-gironde/12/'

        doc = requests.get('https://www.fnaim-gironde.com/achat-immobilier-gironde/12/1')
        soup_back = BeautifulSoup(doc.text, 'html.parser')
        link = soup_back.find("li", class_="last").contents[0].get('href')
        last_page = link.split('/')[-1]
        last_page = int(last_page)

        
        cleanUrl  = []
        for page in range(1, (last_page+1)):

            large_soup = self.get_soup(self.get_response(f'{url}{page}'))
            if large_soup is None:
                continue
            sale_ancres = large_soup.find_all('a',
                                                attrs={'class': 'voir2'})

            for link in sale_ancres:
                link_url = link.attrs['href']
                cleanlink = f'{self.base_url}{link_url}'
                cleanUrl.append(cleanlink)
        return cleanUrl            
                                           
    def routeScrap(self,cnx,cursor,linkList):
        """ scraping data to BDD """

        print("scraping des données sur ",len(linkList)," liens")
        data_scraped = 0

        for url in linkList:
            gourl = str(url)

            try :
                r = requests.get(gourl)
                soup = BeautifulSoup(r.text, "html.parser")

                price = soup.find(class_="subh1").get_text().split("-")[1].replace("€","").replace(" ","")
                surface = soup.find(class_="subh1").get_text().split("-")[0].replace("m2","").replace(" ","") 
                surface = int(surface)

                feats = []

                allsec = soup.find(class_="infos").children 

                count = 0
                for i in allsec :
                    count +=1          
                    feats.append(i.get_text().split(":")[1])
                    if count == 4 :
                        break # crash sometime's with out of range ... 

                type_bien = feats[0].replace(" ","")
                annee = int(feats[1].replace(" ",""))

                nb_pieces = int(feats[2].replace(" ",""))
                ville = soup.find("h1").get_text().split("à")[1]

                # All var's send to bdd
                vals = type_bien,annee,nb_pieces,surface,ville,int(price),gourl

                cursor.execute(f"INSERT INTO `orR9HUwT41`.`maison_appartement_full` (`type_de_bien`, `année`, `nb_de_pieces`, `surface`, `ville`,`prix`,`url`) VALUES {vals}")
                cnx.commit()
                data_scraped +=1
            except:
                pass
        
        print("Data scrape : ",data_scraped)

        return data_scraped

class CleanData():
    """loading Data from BDD & clean them, returns data for X & Y ready for Pipeline"""
    def __init__(self,cursor):
        self.cursor = cursor

    def cleanJob(self):    

        #### request data from BDD with condition for clean data beacause there is a problem whith years ####
        result = self.cursor.execute("SELECT * FROM `orR9HUwT41`.`maison_appartement_full` where année < 100")
        result = self.cursor.fetchall()
        df_un = pd.DataFrame(result, columns=["id","type_de_bien","année","nb_de_pieces","surface","ville","prix","url"])

        result = self.cursor.execute("SELECT * FROM `orR9HUwT41`.`maison_appartement_full` where année > 100")
        result = self.cursor.fetchall()
        df_de = pd.DataFrame(result, columns=["id","type_de_bien","année","nb_de_pieces","surface","ville","prix","url"])

        #### data was offset during scraping ####
        df_un['nb_de_pieces'] = df_un['année']

        #### data was NA ####
        count = 0
        for each in df_un['année'] :
            df_un.loc[count,'année'] = None
            count +=1

        #### concatenante All Data ####
        df = df_un.append(df_de)

        df["surface"] = df["surface"].astype(np.int64)

        #### reset index for loop on them with no bug ####
        df.reset_index(inplace = True)

        #### Set data ready for split ####
        df = df.drop(['id','année','url'], axis=1)
        df['ville'] = df['ville'].str.strip() #Corect first character == " ".

        #### create new features price m2 ####
        count = 0
        for i in df["ville"]:
            df.loc[count,"p_m2"] = df.loc[count,"prix"]/df.loc[count,"surface"]
            count +=1

        ########## issue with index will replace by IsolationForest  ##########
        #######################################################################
        #######################################################################

        df['PriceLog'] = np.log(df.prix)

        y_full = df['PriceLog'].values

        x_full = df.drop(['prix','PriceLog'], axis=1)

        return x_full,y_full

class PipelineModel():
    """class for create and train full pipeline, return model as full Pipeline"""
    def __init__(self,x_full,y_full):
        self.x_full = x_full
        self.y_full = y_full
    
    def goPip(self):
        
        ### Part of code preprocessing + model to Full Python pipeline ####
        categoricals = ['type_de_bien', 'ville']
        categorical_pipe = Pipeline([
            ('oe', OneHotEncoder(handle_unknown="ignore"))
        ])

        poly = ['nb_de_pieces', 'surface',"p_m2"]
        poly_pipe = Pipeline([
            ("poly", PolynomialFeatures(2))
        ])

        scale_pipe = Pipeline([
            ('scaler', StandardScaler())
        ])

        preprocess_pipe = ColumnTransformer([
            ("enc", categorical_pipe, categoricals),
            ("sca", scale_pipe, poly),
            ("pol", poly_pipe , poly),
        ])

        xgb = xgboost.XGBRegressor(colsample_bytree=0.5, subsample=0.7,
                                    learning_rate=0.05, max_depth=5, 
                                    min_child_weight=1.8, n_estimators=1000,
                                    reg_alpha=0.1, reg_lambda=0.3, gamma=0.01, 
                                    silent=1, random_state =7, nthread = -1)

        seed = 60
        np.random.seed(seed)

        x_train, x_val, y_train, y_val = train_test_split(self.x_full,self.y_full , test_size=0.1, random_state=seed)
        x_train.shape, x_val.shape, y_train.shape, y_val.shape

        model = Pipeline([
            ('pre', preprocess_pipe),
            ('reg', xgb)
        ])

        return x_train, x_val, y_train, y_val, model

def goToazure():
    """ Only load modules if Azure is call, store model & deploy endpoint, function returns number of version model uploaded"""
    
    print("pip pour Azure")
    from azureml.core import Workspace
    from azureml.core.model import Model
    from azureml.core.conda_dependencies import CondaDependencies
    from azureml.core.model import InferenceConfig
    from azureml.core.webservice import AciWebservice

    ws = Workspace.get(name='FastImmoStud',
                subscription_id= SL.AZsubscription_id, ## see readme for log's
                resource_group=SL.AZresource_group)

    fastv3 = Model.register(workspace=ws,
                    model_name='fastv3',
                    model_path='model_xgb_v4.joblib', # local path
                    description='xgboost reg')

    # Add the dependencies for your model
    myenv = CondaDependencies()
    myenv.add_conda_package("xgboost")
    myenv.add_pip_package("azureml-defaults")
    myenv.add_pip_package("scikit-learn==0.22.1")
    myenv.add_pip_package("joblib==0.14.1")


    # Save the environment config as a .yml file
    env_file = 'service_files/env.yml'
    with open(env_file,"w") as f:
        f.write(myenv.serialize_to_string())
    print("Saved dependency info in", env_file)


    _inference_config = InferenceConfig(runtime= "python",
                                                    source_directory = 'service_files',
                                                    entry_script="score.py",
                                                    conda_file="env.yml")

    aciconfig = AciWebservice.deploy_configuration(cpu_cores=1, 
                                                    memory_gb=1)

    model = ws.models['fastv3']

    ### we can't deploy model with same name (crash), so we generate a random number, but we can register a model with same name, he is vers by Azure.
    is_versionage = False
    while is_versionage != True:
        try:
            vers = randrange(10000000) ## generate random int for unique id deployment
            vers = str(vers)
            service = Model.deploy(workspace=ws,
                            name = f'fast-service-{vers}',
                            models = [model],
                            inference_config = _inference_config,
                            deployment_config = aciconfig)
            is_versionage = True ## if deploy is pass, go out of loops & wait to azure finish job
        except :
            is_versionage = False

    service.wait_for_deployment(show_output = True)
    endpoint = service.scoring_uri
    print(endpoint)

    ## loop on model list & keep the last version just created
    for model in Model.list(ws):
        num_mod_ver = model.version 
    return num_mod_ver


############################################ start routine #################################

# Call Bdd connection class 
tip = Sqldd()
cnx, cursor = tip.get_bdd_co()

# call class Scraper url
scraper = Scraper()
print("Start Scrap url")
outputLink = scraper.get_all_sales_csv()

# call class Scraper data
should = scraper.routeScrap(cnx,cursor,outputLink)

if should == 0:
    print(" -------------------  Nothing to scrap !! Exit program ---------------------- ")
    exit()


# Call clean Data Class
ccl = CleanData(cursor)
x_full,y_full = ccl.cleanJob()

# call class Pipeline model
fft = PipelineModel(x_full, y_full)
x_train, x_val, y_train, y_val, model = fft.goPip()


#### trainning & evaluate model ####

model.fit(x_train,y_train)

y_valid_pred = model.predict(x_train)
xgb_pred_ref = np.exp(y_valid_pred)

y_val_rescale = y_train.reshape(y_train.shape[0])
y_val_rescale = np.exp(y_val_rescale)

Train_RMSE = np.sqrt(MSE(xgb_pred_ref, y_val_rescale))
Train_score = MAE(xgb_pred_ref, y_val_rescale)

y_valid_pred = model.predict(x_val)
xgb_pred_ref = np.exp(y_valid_pred)

y_val_rescale = y_val.reshape(y_val.shape[0])
y_val_rescale = np.exp(y_val_rescale)

Val_RMSE = np.sqrt(MSE(xgb_pred_ref, y_val_rescale))
Val_score = MAE(xgb_pred_ref, y_val_rescale)


#### reaplace with request to bdd -- load metric from model in Prod ####
max_version = cursor.execute("SELECT MAX(version) version FROM `orR9HUwT41`.`Suivis_metrics`")
max_version = cursor.fetchone()
old_train_rmse = cursor.execute(f"SELECT `Train_RMSE` FROM `orR9HUwT41`.`Suivis_metrics` WHERE `version`={max_version[0]}")
old_train_rmse = cursor.fetchone()
old_train_score = cursor.execute(f"SELECT `Train_MAE` FROM `orR9HUwT41`.`Suivis_metrics` WHERE `version`={max_version[0]}")
old_train_score = cursor.fetchone()
old_val_rmse = cursor.execute(f"SELECT `Val_RMSE` FROM `orR9HUwT41`.`Suivis_metrics` WHERE `version`={max_version[0]}")
old_val_rmse = cursor.fetchone()
old_val_score = cursor.execute(f"SELECT `Val_MAE` FROM `orR9HUwT41`.`Suivis_metrics` WHERE `version`={max_version[0]}")
old_val_score = cursor.fetchone()

### Check if metric are better then the model metric in prod, if True we will register model to Azure storage, then deploy it ####

if Train_RMSE < old_train_rmse and Train_score < old_train_score :
    if Val_RMSE < old_val_rmse and Val_score < old_val_score :
        print("!!! Innit register model !!!")
        dump(model,"model_xgb_v4.joblib")
        num_mod_ver = goToazure()
        is_push_onProd = 1
        version = num_mod_ver
        print("!!! Better Model Created !!!")
        print("new metrics = Train_RMSE : ",round(Train_RMSE,4),"Train_MAE : ",round(Train_score,4),"Val_RMSE :", round(Val_RMSE,4),"Val_MAE : ",round(Val_score,4))
    else:
        is_push_onProd=0
        version = 0
        print("Train metrics are better, but not Val metrics")
else :
    is_push_onProd = 0
    version = 0
    print("Train metrics are not better")
    if Train_RMSE < old_val_rmse and Train_score < old_val_score :
        print(" but Val metrics are better")
    else:
        print("Val metrics are not better")


####  need send métric to bdd ####
vals = Train_RMSE,Train_score,Val_RMSE,Val_score,is_push_onProd,version
cursor.execute(f"INSERT INTO `orR9HUwT41`.`Suivis_metrics` (`Train_RMSE`, `Train_MAE`, `Val_RMSE`, `Val_MAE`, `is_push_onProd`,`version`) VALUES {vals}")
cnx.commit()

cursor.close
cnx.close()

###################################################################### It's Finish :) :) ############################################################################
#####################################################################################################################################################################