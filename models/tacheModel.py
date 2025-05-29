
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,send_file

from api import db
#db=SQLAlchemy()


class Tache(db.Model):
    __tablename__='taches'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    projet_id=db.Column(db.Integer)
    titre=db.Column(db.String(200))
    priorite=db.Column(db.String(200))
    statut=db.Column(db.String(100))
    created_at=db.Column(db.String(200))
    date_echeance=db.Column(db.String(200))
    date_fin=db.Column(db.String(200))
    description=db.Column(db.Text)


    def __init__(self,user_id,titre,date_echeance,description,priorite,created_at,projet_id):
        self.user_id=user_id
        self.titre=titre
        self.date_echeance=date_echeance
        self.description=description
        self.statut="En attente de demarrage"
        self.created_at=created_at
        self.date_fin=None
        self.priorite=priorite
        self.projet_id=projet_id
