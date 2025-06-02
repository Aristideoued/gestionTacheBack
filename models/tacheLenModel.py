from api import db

class TacheLen(db.Model):
    __tablename__='tache_len'
    id=db.Column(db.Integer,primary_key=True)
    taille=db.Column(db.Integer,default=0)
   
   
    def __init__(self,taille):   
        self.taille=taille
       
       
