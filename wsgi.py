

#! /usr/bin/env python

from api import app as application
from api import db

from models.parcoursModel import Parcours
from models.clientModel import Client
from models.adminModel import Admin
from models.certificationModel import Certification
from models.messageModel import Message
from models.fichierModel import Fichier
from models.tarificationModel import Tarification
from models.notificationModel import Notification
from models.experienceModel import Experience
from models.referenceModel import Reference
from models.categorieModel import Categorie

import logging
from logging.handlers import RotatingFileHandler

from api.endpoints import *


@application.route('/createTable',methods=['GET'])
def create_table2():
    db.create_all()
    #query = 'ALTER TABLE produits ADD couleur character(60);'
    #db.execute(query)
    return "Tables created"


@application.route('/addColumn',methods=['GET'])
def addColumn():
   
    return "ok"

@application.route('/home',methods=['GET'])
def home():
    return "Ok"


app.logger.setLevel(logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

if __name__ == "__main__":
    application.run(host='0.0.0.0')


#from api import app,db

