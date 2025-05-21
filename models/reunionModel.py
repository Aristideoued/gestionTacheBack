from api import db
from sqlalchemy.dialects.postgresql import JSON  # si tu utilises PostgreSQL

class Reunion(db.Model):
    __tablename__='reunions'
    id=db.Column(db.Integer,primary_key=True)
    ordre_du_jour=db.Column(db.Text)
    date=db.Column(db.String(200))
    heure_debut=db.Column(db.String(200))
    heure_fin=db.Column(db.String(200))
    created_at=db.Column(db.String(200))
    participants = db.Column(JSON, nullable=False, default=list)    

    def __init__(self,ordre_du_jour,date,heure_debut,heure_fin,participants,created_at):
        self.ordre_du_jour=ordre_du_jour
        self.date=date
        self.created_at=created_at
        self.heure_debut=heure_debut
        self.heure_fin=heure_fin
        self.participants=participants
        
       
        
        
   


