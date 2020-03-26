## Real-Estate-Dev full industrial Pipeline as Code

Cette branche regroupe l'industrialisation du code.

le script indusPipline.py contient toute la chaine de production mise sous conditions.

cmd = python indusPipline.py
    choisir option 1 pour toute la pipeline
    option 2 : scraping seulement
    option 3 entrainement du modèle

Autre option, depuis le dossier Labo, exécuter docker-compose up et toute la Pipeline est éxécutée.    

Etape : 
    
    -Scrap des URL depuis la source de Data
    -Si nouvelle URL alors Scrap data
    -envoie vers BDD des nouvelles url et des nouvelles données
    -si il y'a du nouveau --> Entrainement du modèle
    -Comparaison des metrcis avec celle du modèle en production
    -Enregistrement des données metrics sur bdd BDD
    -Si meilleur métrics alors on dump le modèle et on l'inscrit sur Azure (le modéle est alors versionné), 
    et deploiement du modèle sur Azure ou lien vers API Flask ?

Requirements :
    
    - créer un script sec.py à la racine du dossier :

    class secureLog():

        sqlLogUser="xxxxxxx"
        sqlLogPass="xxxxxxx"
        sqlLogHost='xxxxxxx'
        sqlLogDatabase='xxxxxxx'
        sqlLogPort='3306'  

        AZsubscription_id='xxxxx', (Azure id)
        AZresource_group='xxxxxx' (Azure group)

    - librairie Python : 

        -  Python==3.7.0
        -  xgboost==0.90
        -  scikit-learn==0.22.1
        -  joblib==0.14.1
        -  beautifulsoup4==4.8.2
        -  mysql-connector-python==8.0.19
        -  azureml-sdk==1.0.85
        -  pandas==0.23.4
        -  numpy==1.16.2

Le Notebook 01-Modelisation est le script qui a permis de créer le modèle et celui surlequel nous pouvons l'améliorer

Attention l'opération de scraping peut être longue

Ce script est presque indépendant d'Azure, si jamais on utilise plus azure alors il suffira de remplacer le chemin d'enregistrement du modéle vers le nouvel espace de stockage, tout le reste du code est une Pipeline python.

