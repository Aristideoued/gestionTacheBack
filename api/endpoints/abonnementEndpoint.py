from flask import Flask,request,jsonify,send_file
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
#from response import testpay_response
from PIL import Image
import glob
from flask_cors import cross_origin
import hashlib, uuid
import os
from datetime import datetime
from models.abonnementLenModel import AbonnementLen
from models.abonnementModel import Abonnement
from models.userModel import User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from models.adminModel import Admin
from api import app,db
from flask import make_response
from api import app,db,auth,authenticate


UPLOAD_FOLDER = 'fichiers'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','pdf','mov', 'avi', 'mp4', 'flv', 'wmv', 'webm', 'mkv', 'svf','docx','xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MYDIR = os.path.dirname(__file__)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/taille/abonnements' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getLenAbonnement():
    if request.method=='GET':
            historiques=[]
            lenAb=db.session.query(AbonnementLen).filter(AbonnementLen.id==1).first()

            #user=db.session.query(User).all()

           
          
            historiques.append({"taille":lenAb.taille})


            retour={"code":200,"title":"La taille","contenu":historiques}
            #print(users[0])
            return make_response(jsonify(retour),200)
    


@app.route('/addAbonnement' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addAbonnement():
    if request.method=='POST':
            data = request.get_json()
            description=data['description']
            statut=data['statut']
            

            formule=data['formule']
            dateExpiration=data['dateExpiration']
            montantAnnuel=int(data['montantAnnuel'])
            montantMensuel=int(data['montantMensuel'])
            
                    
            proj=Abonnement(formule,dateExpiration,statut,montantAnnuel,montantMensuel,description)
           
            db.session.add(proj)
            db.session.commit()

            abLen=db.session.query(AbonnementLen).filter(AbonnementLen.id==1).first()
            abLen.taille+=1
            db.session.add(abLen)
            db.session.commit()


            retour={"code":200,"Title":"Ajout d'un Abonnement","contenu":"Abonnement ajouté avec succès"}
            return make_response(jsonify(retour),200)
    
           
                 
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/delete/abonnement' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_Abonnement():
    if request.method=='POST':
            
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Abonnement).filter(Abonnement.id==id).first()
            if user1:
                Abonnement.query.filter_by(id=id).delete()
                db.session.commit()
                abLen=db.session.query(AbonnementLen).filter(AbonnementLen.id==1).first()
                abLen.taille-=1
                db.session.add(abLen)
                db.session.commit()

                retour={"code":200,"title":"Suppression d'un Abonnement","contenu":"Abonnement supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Abonnement non trouvé"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/all/abonnements' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getAbonnement():
    if request.method=='GET':
            historiques=[]
            historique = Abonnement.query.all()
            #user=db.session.query(User).all()

            for u in historique:
          
                historiques.append({"formule":u.formule,"statut":u.statut,"dateExpiration":u.dateExpiration,"montantAnnuel":u.montantAnnuel,"montantMensuel":u.montantMensuel,"description":u.description})


            retour={"code":200,"title":"Liste des Abonnements","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)
    

@app.route('/abonnements' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getAbonnementParPage():
    if request.method=='GET':
            historiques=[]
           
            #user=db.session.query(User).all()
              

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=60, type=int)
            #cat = request.args.get('categorie', type=int)
            historique=Abonnement.query.paginate(page=page, per_page=per_page, error_out=False)
           

            for u in historique:


                historiques.append({"formule":u.formule,"statut":u.statut,"dateExpiration":u.dateExpiration,"montantAnnuel":u.montantAnnuel,"montantMensuel":u.montantMensuel,"description":u.description})

            retour={"code":200,"title":"Liste des Abonnements","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)


@app.route('/abonnementById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getAbonnementById():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            u=db.session.query(Abonnement).filter(Abonnement.id==id).first()
            clients.append({"formule":u.formule,"statut":u.statut,"dateExpiration":u.dateExpiration,"montantAnnuel":u.montantAnnuel,"montantMensuel":u.montantMensuel,"description":u.description})


    
                #print(u.nom)


            retour={"code":200,"title":"Abonnement "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
    



 

@app.route('/update/abonnement' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def update_Abonnement():
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])
            description=data['description']
            statut=data['statut']
            

            formule=data['formule']
            dateExpiration=data['dateExpiration']
            montantAnnuel=int(data['montantAnnuel'])
            montantMensuel=int(data['montantMensuel'])
            

            user1=db.session.query(Abonnement).filter(Abonnement.id==id).first()
            
            if user1:
                user1.formule=formule
                user1.dateExpiration=dateExpiration
                user1.montantAnnuel=montantAnnuel
                user1.statut=statut
                user1.montantMensuel=montantMensuel
                user1.description=description
                db.session.add(user1)
                db.session.commit()
               
                

                retour={"code":200,"title":"Modification d'un Abonnement","contenu":"Abonnement modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Abonnement non trouvé"}
                return make_response(jsonify(retour),401)


