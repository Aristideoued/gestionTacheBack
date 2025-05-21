from api import db

class Historique(db.Model):
    __tablename__='historiques'
    id=db.Column(db.Integer,primary_key=True)
    type_action=db.Column(db.String(200))
    created_at=db.Column(db.String(200))
    description=db.Column(db.Text)
    user_id=db.Column(db.Integer)
    tache_id=db.Column(db.Integer)


    

    def __init__(self,user_id,tache_id,type_action,description,created_at):
        self.created_at=created_at
        self.user_id=user_id
        self.tache_id=tache_id
        self.description=description
        self.type_action=type_action
        
       
        
        
   


