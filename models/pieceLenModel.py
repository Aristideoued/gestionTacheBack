from api import db

class PieceLen(db.Model):
    __tablename__='piece_len'
    id=db.Column(db.Integer,primary_key=True)
    taille=db.Column(db.Integer,default=0)
   
   
    def __init__(self,taille):   
        self.taille=taille
       
       
