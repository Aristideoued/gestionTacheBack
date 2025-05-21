from api import db

class Projet(db.Model):
    __tablename__='projets'
    id=db.Column(db.Integer,primary_key=True)
    nom=db.Column(db.String(60))
    description=db.Column(db.Text)
    date_debut=db.Column(db.String(60))
    date_fin_prevue=db.Column(db.String(60))
    statut=db.Column(db.String(60))
    responsable_id=db.Column(db.Integer)




    def __init__(self,nom,description,date_debut,date_fin_prevue,statut,responsable_id):
        self.nom=nom
        self.description=description
        self.date_debut=date_debut
        self.date_fin_prevue=date_fin_prevue
        self.statut=statut
        self.responsable_id=responsable_id
   


