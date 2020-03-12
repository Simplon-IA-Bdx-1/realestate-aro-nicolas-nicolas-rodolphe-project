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

endpoint/host: "remotemysql.com"
port: 3306
username: "orR9HUwT41"
password: "wR8Oms9iMD"

```
- Vous voilà connecté !

## CODE CNX

```python
import mysql.connector

cnx = mysql.connector.connect(user='orR9HUwT41', password='wR8Oms9iMD',
                              host='remotemysql.com',
                              database='orR9HUwT41', port='3306')
#cnx.close()

from mysql.connector import (connection)

cnx = connection.MySQLConnection(user='orR9HUwT41', password='wR8Oms9iMD',
                              host='remotemysql.com',
                              database='orR9HUwT41', port='3306')

```