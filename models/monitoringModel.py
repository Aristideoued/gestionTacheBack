from api import db

class Monitoring(db.Model):
    __tablename__='monitorings'
    id=db.Column(db.Integer,primary_key=True)
    url=db.Column(db.String(60))
    beneficiaire=db.Column(db.String(200))
    statut=db.Column(db.String(60))
    dateMonitoring=db.Column(db.String(60))
    commentaire=db.Column(db.Text)

   
    def __init__(self,url,beneficiaire,statut,dateMonitoring,commentaire):   
        self.url=url
        self.beneficiaire=beneficiaire
        self.statut=statut
        self.dateMonitoring=dateMonitoring
        self.commentaire=commentaire
       
       

