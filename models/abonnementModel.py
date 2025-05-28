from api import db

class Abonnement(db.Model):
    __tablename__='abonnements'
    id=db.Column(db.Integer,primary_key=True)
    formule=db.Column(db.String(60))
    dateExpiration=db.Column(db.String(60))
    statut=db.Column(db.String(60))
    montantMensuel=db.Column(db.Integer)
    montantAnnuel=db.Column(db.Integer)
    description=db.Column(db.Text)


    
   
   
    def __init__(self,formule,dateExpiration,statut,montantAnnuel,montantMensuel,description):   
        self.formule=formule
        self.dateExpiration=dateExpiration
        self.statut=statut
        self.montantAnnuel=montantAnnuel
        self.montantMensuel=montantMensuel
        self.description=description
       

