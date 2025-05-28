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
from models.adminModel import Admin
import hashlib, uuid


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

if __name__ == "__main__":
   
    create_admin()
    app.run(debug=True,host='0.0.0.0',port=5500)
