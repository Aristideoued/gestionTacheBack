

#! /usr/bin/env python

from api import app as application
from api import db

import hashlib, uuid

from models.roleModel import Role
from models.userModel import User
from models.adminModel import Admin
from models.departementModel import Departement
from models.projetModel import Projet
from models.tacheModel import Tache


from models.commentaireModel import Commentaire
from models.abonnementModel import Abonnement
from models.monitoringModel import Monitoring
from models.pieceModel import Piece

from models.reunionModel import Reunion
from models.historiqueModel import Historique
from models.beneficiaireModel import Beneficiaire

from models.notificationModel import Notification



import logging
from logging.handlers import RotatingFileHandler

from api.endpoints import *



def create_admin():
    with application.app_context():
        db.create_all()
        # Vérifie si un utilisateur admin existe déjà
        admin = Admin.query.filter_by(username='admin').first()
        if admin:
            print("Le compte admin existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        admin = Admin(
            nom="Ouedraogo",
            prenom="Aristide",
            telephone="54007038",
            username='admin',
            password = hashlib.sha256(("admin").encode("utf-8")).hexdigest())
        db.session.add(admin)
        db.session.commit()
        print("Compte admin créé avec succès !")

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
    create_admin()
    
    application.run(host='0.0.0.0')

#from api import app,db

