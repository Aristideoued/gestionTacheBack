from api import db

class Commentaire(db.Model):
    __tablename__='commentaires'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    tache_id=db.Column(db.Integer)
    contenue=db.Column(db.Text)
    created_at=db.Column(db.String(200))
    

    def __init__(self,user_id,tache_id,contenue,created_at):
        self.created_at=created_at
        self.user_id=user_id
        self.tache_id=tache_id
        self.contenue=contenue
        
       
        
        
   


