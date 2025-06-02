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
from models.reunionLenModel import ReunionLen
from models.roleModel import Role
from models.reunionModel import Reunion
from models.userModel import User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import json
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



@app.route('/taille/reunions' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getLenReunion():
    if request.method=='GET':
            historiques=[]
            lenAb=db.session.query(ReunionLen).filter(ReunionLen.id==1).first()

            #user=db.session.query(User).all()

           
          
            historiques.append({"taille":lenAb.taille})


            retour={"code":200,"title":"La taille","contenu":historiques}
            #print(users[0])
            return make_response(jsonify(retour),200)



@app.route('/addReunion' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addReunion():
    if request.method=='POST':
            data = request.get_json()

            ordre_du_jour=data['ordre_du_jour']
            date=data['date']
            heure_debut=data['heure_debut']
            heure_fin=data['heure_fin']
            participants=data['participants']
            participant=json.loads(participants)

            now = datetime.now()

            # Convertir en string
            date_str = now.strftime("%Y-%m-%d %H:%M:%S")
                        
            created_at=date_str

           
            
                    
            proj=Reunion(ordre_du_jour,date,heure_debut,heure_fin,participant,created_at)
           
            db.session.add(proj)
            db.session.commit()
            abLen=db.session.query(ReunionLen).filter(ReunionLen.id==1).first()
            abLen.taille+=1
            db.session.add(abLen)
            db.session.commit()
            retour={"code":200,"Title":"Ajout d'un Reunion","contenu":"Reunion ajouté avec succès"}
            return make_response(jsonify(retour),200)
    
           
                 
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/delete/reunion' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_Reunion():
    if request.method=='POST':
            
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Reunion).filter(Reunion.id==id).first()
            if user1:
                Reunion.query.filter_by(id=id).delete()
                db.session.commit()
                abLen=db.session.query(ReunionLen).filter(ReunionLen.id==1).first()
                abLen.taille-=1
                db.session.add(abLen)
                db.session.commit()

                retour={"code":200,"title":"Suppression d'un Reunion","contenu":"Reunion supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Reunion non trouvé"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/all/reunions' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getReunion():
    if request.method=='GET':
            historiques=[]
            historique = Reunion.query.all()
            #user=db.session.query(User).all()

            for u in historique:

          
                
                historiques.append({"ordre_du_jour":u.ordre_du_jour,"date":u.date,"heure":u.heure_debu,"heure_fin":u.heure_fin,"participants":u.participants})


            retour={"code":200,"title":"Liste des Reunions","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)
    

@app.route('/reunions' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getReunionParPage():
    if request.method=='GET':
            historiques=[]
           
            #user=db.session.query(User).all()
              

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=60, type=int)
            #cat = request.args.get('categorie', type=int)
            historique=Reunion.query.paginate(page=page, per_page=per_page, error_out=False)
           

            for u in historique:


                
                
                historiques.append({"ordre_du_jour":u.ordre_du_jour,"date":u.date,"heure":u.heure_debu,"heure_fin":u.heure_fin,"participants":u.participants})

            retour={"code":200,"title":"Liste des Reunions","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)


@app.route('/reunionById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getReunionById():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            u=db.session.query(Reunion).filter(Reunion.id==id).first()
            
            clients.append({"ordre_du_jour":u.ordre_du_jour,"date":u.date,"heure":u.heure_debu,"heure_fin":u.heure_fin,"participants":u.participants})


    
                #print(u.nom)


            retour={"code":200,"title":"Reunion "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
    


@app.route('/update/reunion' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def update_Reunion():
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])
            ordre_du_jour=data['ordre_du_jour']
            date=data['date']
            heure_debut=data['heure_debut']
            heure_fin=data['heure_fin']
            participants=data['participants']
            participant=json.loads(participants)

            user1=db.session.query(Reunion).filter(Reunion.id==id).first()
            
            if user1:
                user1.ordre_du_jour=ordre_du_jour
                user1.date=date
                user1.heure_debut=heure_debut
                user1.heure_fin=heure_fin
                user1.participants=participant
               
                db.session.add(user1)
                db.session.commit()
               
                

                retour={"code":200,"title":"Modification d'une Reunion","contenu":"Reunion modifiée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Reunion non trouvée"}
                return make_response(jsonify(retour),401)


