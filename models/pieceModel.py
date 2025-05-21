from api import db

class Piece(db.Model):
    __tablename__='pieces'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    tache_id=db.Column(db.Integer)

    nom=db.Column(db.String(255))
    created_at=db.Column(db.String(100))
    

    def __init__(self,user_id,tache_id,nom,created_at):
        self.user_id=user_id
        self.tache_id=tache_id
        self.nom=nom
        self.created_at=created_at
        
       
        
        
   


