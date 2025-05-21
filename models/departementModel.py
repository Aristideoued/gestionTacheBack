from api import db

class Departement(db.Model):
    __tablename__='departements'
    id=db.Column(db.Integer,primary_key=True)
    nom=db.Column(db.Integer)
    
   
   
    def __init__(self,nom):   
        self.nom=nom
       

