from api import db

class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    role=db.Column(db.String(60))
    permissions=db.Column(db.String(200))
    

    def __init__(self,role,permissions):
        self.role=role
        self.permissions=permissions
        
       
        
        
   


