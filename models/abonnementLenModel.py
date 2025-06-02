from api import db

class AbonnementLen(db.Model):
    __tablename__='abonnement_len'
    id=db.Column(db.Integer,primary_key=True)
    taille=db.Column(db.Integer,default=0)
   
   
    def __init__(self,taille):   
        self.taille=taille
       
       

