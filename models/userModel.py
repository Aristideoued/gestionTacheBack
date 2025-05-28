

from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,send_file

from api import db
#db=SQLAlchemy()


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    role_id=db.Column(db.Integer)
    departement_id=db.Column(db.Integer)
    nom=db.Column(db.String(255))
    prenom=db.Column(db.String(255))
    phone=db.Column(db.String(255))
    email=db.Column(db.String(255))
    password=db.Column(db.String(255))
    code=db.Column(db.String(6))
    titre=db.Column(db.String(255))
    statut=db.Column(db.Integer)
   

    

    def __init__(self,nom,prenom,phone,email,password,role_id,departement_id,titre):
        self.nom=nom
        self.prenom=prenom
        self.phone=phone
        self.email=email
        self.statut=1
        self.password=password
        self.titre=titre
        self.role_id=role_id
        self.code=None
        self.departement_id=departement_id
        
