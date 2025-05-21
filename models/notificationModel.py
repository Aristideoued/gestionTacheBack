from api import db

class Notification(db.Model):
    __tablename__='notifications'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    message=db.Column(db.Text)
    type=db.Column(db.String(200))
    est_lue=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.String(200))
    

    def __init__(self,message,type,user_id,created_at):
        self.message=message
        self.type=type
        self.created_at=created_at
        self.user_id=user_id
        
       
        
        
   


