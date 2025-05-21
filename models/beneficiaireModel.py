from api import db
from sqlalchemy.dialects.postgresql import JSON  # si tu utilises PostgreSQL

class Beneficiaire(db.Model):
    __tablename__='beneficiaires'
    id=db.Column(db.Integer,primary_key=True)
    nom=db.Column(db.String(200))
    prenom=db.Column(db.String(200))
    structure=db.Column(db.String(200))
    email=db.Column(db.String(255))
    telephone=db.Column(db.String(60))

    def __init__(self,nom,prenom,structure,email,telephone):
        self.nom=nom
        self.prenom=prenom
        self.structure=structure
        self.email=email
        self.telephone=telephone
        
       
        
        
   


