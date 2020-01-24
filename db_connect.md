## PRE-REQUIS

- Installer la derniere version de "Microsoft Visual C++ Redistributable for Visual Studio" x64
(https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads) 

- Installer "MySQL WorkBench"
(https://dev.mysql.com/downloads/workbench/)

## SE CONNECTER A LA DATABASE MYSQL :

Une fois l'ensemble des logiciels installés :
- CTRL+U pour initier une nouvelle connexion
- Entrer les informations : 

```python

endpoint/host: "database.cbg3amltio47.us-east-2.rds.amazonaws.com"
port: 3306
username: "admin"
password: "adminadmin"

```
- Vous voilà connecté !

## CODE CNX

```python
import mysql.connector

cnx = mysql.connector.connect(user='admin', password='adminadmin',
                              host='database.cbg3amltio47.us-east-2.rds.amazonaws.com',
                              database='mydb', port='3306')
#cnx.close()

from mysql.connector import (connection)

cnx = connection.MySQLConnection(user='admin', password='adminadmin',
                              host='database.cbg3amltio47.us-east-2.rds.amazonaws.com',
                              database='mydb', port='3306')

```