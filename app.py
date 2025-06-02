#! /usr/bin/env python

import os



from api.endpoints import *
from flask import Flask,request,jsonify,send_file
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import glob
from flask_cors import cross_origin
import hashlib, uuid
import os
from datetime import datetime
from api import app,db
from models.HistoriqueLenModel import HistoriqueLen
from models.abonnementLenModel import AbonnementLen
from models.adminLenModel import AdminLen
from models.adminModel import Admin
import hashlib, uuid

from models.beneficiaireLenModel import BeneficiaireLen
from models.commentaireLenModel import CommentaireLen
from models.departementLenModel import DepartementLen
from models.monitoringLenModel import MonitoringLen
from models.notificationLenModel import NotificationLen
from models.pieceLenModel import PieceLen
from models.projetLenModel import ProjetLen
from models.reunionLenModel import ReunionLen
from models.roleLenModel import RoleLen
from models.tacheLenModel import TacheLen
from models.userLenModel import UserLen


@app.route('/createTable',methods=['GET'])
def create_table():
    db.create_all()
    return "Tables created...."



def create_admin():
    with app.app_context():
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

        abLen = AbonnementLen.query.filter_by(id=1).first()
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



def create_abonnementLen():
    with app.app_context():
        

        abLen = AbonnementLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = AbonnementLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()


def create_adminLen():
    with app.app_context():
        

        abLen = AdminLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = AdminLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()


def create_beneficiaireLen():
    with app.app_context():
        

        abLen = BeneficiaireLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = BeneficiaireLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()


def create_commentaireLen():
    with app.app_context():
        

        abLen = CommentaireLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = CommentaireLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()




def create_departementLen():
    with app.app_context():
        

        abLen =DepartementLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = DepartementLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()

def create_HistoriqueLen():
    with app.app_context():
        

        abLen = HistoriqueLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = HistoriqueLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()


def create_monitoringLen():
    with app.app_context():
        

        abLen = MonitoringLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = MonitoringLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()

def create_notificationLen():
    with app.app_context():
        

        abLen = NotificationLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = NotificationLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()


def create_pieceLen():
    with app.app_context():
        

        abLen = PieceLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = PieceLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()


def create_projetLen():
    with app.app_context():
        

        abLen = ProjetLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = ProjetLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()

def create_reunionLen():
    with app.app_context():
        

        abLen = ReunionLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = ReunionLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()

def create_roleLen():
    with app.app_context():
        

        abLen = RoleLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = RoleLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()


def create_tacheLen():
    with app.app_context():
        

        abLen = TacheLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = TacheLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()


def create_userLen():
    with app.app_context():
        

        abLen = UserLen.query.filter_by(id=1).first()
        if abLen:
            print("Existe déjà.")
            return

        # Crée un utilisateur admin par défaut
        ablen = UserLen(taille=0)
           
        db.session.add(ablen)
        db.session.commit()



if __name__ == "__main__":
   
    create_admin()
    create_abonnementLen()
    create_adminLen()
    create_beneficiaireLen()
    create_commentaireLen()
    create_departementLen()
    create_HistoriqueLen()
    create_monitoringLen()
    create_notificationLen()
    create_pieceLen()
    create_projetLen()
    create_reunionLen()
    create_roleLen()
    create_tacheLen()
    create_userLen()
    
    app.run(debug=True,host='0.0.0.0',port=5500)
