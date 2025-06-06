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
from models.projetModel import Projet
from models.tacheLenModel import TacheLen
from models.tacheModel import Tache

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from models.adminModel import Admin
from models.userModel import User

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



@app.route('/taille/taches' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getLenTache():
    if request.method=='GET':
            historiques=[]
            lenAb=db.session.query(TacheLen).filter(TacheLen.id==1).first()

            #user=db.session.query(User).all()

           
          
            historiques.append({"taille":lenAb.taille})


            retour={"code":200,"title":"La taille","contenu":historiques}
            #print(users[0])
            return make_response(jsonify(retour),200)



@app.route('/addTache' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addTache():
    if request.method=='POST':
            data = request.get_json()

            user_id=int(data['user_id'])
            titre=data['titre']
            date_echeance=data['date_echeance']
            description=data['description']
            now = datetime.now()

            # Convertir en string
            date_str = now.strftime("%Y-%m-%d %H:%M:%S")
                        
            created_at=date_str
            
            priorite=data['priorite']

            projet_id=None
            if "projet_id" in data:
                 projet_id=int(data['projet_id'])
                 

            user1=db.session.query(User).filter(User.id==user_id).first()
            if user1.statut==1:
                 


                tache=Tache(user_id,titre,date_echeance,description,priorite,created_at,projet_id)
                db.session.add(tache)
                db.session.commit()
                abLen=db.session.query(TacheLen).filter(TacheLen.id==1).first()
                abLen.taille+=1
                db.session.add(abLen)
                db.session.commit()

                retour={"code":200,"title":"Ajout d'une Tache","contenu":"Tache ajoutée avec succes"}
                return make_response(jsonify(retour),200)
            
            else:
                retour={"code":401,"title":"Ajout d'une Tache","contenu":user1.nom+ " "+user1.prenom+" est actuellement inactif(ve)"}
                return make_response(jsonify(retour),401)
                 
                    
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/delete/tache' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_Tache():
    if request.method=='POST':
            
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Tache).filter(Tache.id==id).first()
            if user1:
                Tache.query.filter_by(id=id).delete()
                db.session.commit()
                abLen=db.session.query(TacheLen).filter(TacheLen.id==1).first()
                abLen.taille-=1
                db.session.add(abLen)
                db.session.commit()

                retour={"code":200,"title":"Suppression d'une Tache","contenu":"Tache supprimée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Tache non trouvé"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/all/taches' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getTacheAll():
    if request.method=='GET':
            taches=[]
            

           
            tache=Tache.query.all()
            #user=db.session.query(User).all()

            for u in tache:

                employe=db.session.query(User).filter(User.id==u.user_id).first()
                projet=db.session.query(Projet).filter(Projet.id==u.projet_id).first()


               
                taches.append({"id":u.id,"titre":u.titre,"projet":projet.nom,"priorite":u.priorite,"date_echeance":u.date_echeance,"description":u.description,"date_creation":u.created_at,"responsable":employe.nom+" "+employe.prenom})


            retour={"code":200,"title":"Liste des Taches","contenu":taches,"taille":len(tache)}
            #print(users[0])
            return make_response(jsonify(retour),200)
    



@app.route('/taches' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getTache():
    if request.method=='GET':
            taches=[]
            

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=60, type=int)
            #cat = request.args.get('categorie', type=int)
            tache=Tache.query.paginate(page=page, per_page=per_page, error_out=False)
            #user=db.session.query(User).all()

            for u in tache:

                employe=db.session.query(User).filter(User.id==u.user_id).first()
                projet=db.session.query(Projet).filter(Projet.id==u.projet_id).first()


               
                taches.append({"id":u.id,"titre":u.titre,"projet":projet.nom,"priorite":u.priorite,"date_echeance":u.date_echeance,"description":u.description,"date_creation":u.created_at,"responsable":employe.nom+" "+employe.prenom})


               


            retour={"code":200,"title":"Liste des Taches","contenu":taches,"taille":len(tache)}
            #print(users[0])
            return make_response(jsonify(retour),200)
    


@app.route('/tacheById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getTacheById():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            f=db.session.query(Tache).filter(Tache.id==id).first()

            employe=db.session.query(User).filter(User.id==f.user_id).first()
            projet=db.session.query(Projet).filter(Projet.id==f.projet_id).first()

            if projet:
                clients.append({"id":f.id,"titre":f.titre,"projet":projet.nom,"priorite":f.priorite,"date_echeance":f.date_echeance,"description":f.description,"date_creation":f.created_at,"responsable":employe.nom+" "+employe.prenom})

            else:
                clients.append({"id":f.id,"titre":f.titre,"priorite":f.priorite,"date_echeance":f.date_echeance,"description":f.description,"date_creation":f.created_at,"responsable":employe.nom+" "+employe.prenom})

            retour={"code":200,"title":"Tache "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
    

@app.route('/update/tache' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def updateTransactionType():
    if request.method=='POST':
            data = request.get_json()
            
            id = int(data['id'])
            user_id=int(data['user_id'])
            titre=data['titre']
            date_echeance=data['date_echeance']
            date_fin=data['date_fin']

            description=data['description']
           
            
            priorite=data['priorite']
            
            tache=db.session.query(Tache).filter(Tache.id==id).first()

            projet_id =tache.projet_id
            
            if "projet_id"  in data:
                 
                projet_id=int(data["projet_id"])
            
            if tache:
                tache.user_id=user_id
                tache.date_echeance=date_echeance
                tache.date_fin=date_fin
                tache.description=description
                tache.priorite=priorite
                tache.titre=titre
                tache.projet_id=projet_id

                db.session.add(tache)
                db.session.commit()

                retour={"code":200,"title":"Modification d'une Tache","contenu":"Tache modifiée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"TransactionType non trouvé"}
                return make_response(jsonify(retour),401)

           
                 
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/tacheByUserId' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getTacheByUserId():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            user_id=int(data['user_id'])

            tache=db.session.query(Tache).filter(Tache.user_id==user_id)

            for f in tache:
                 

                #employe=db.session.query(User).filter(User.id==f.user_id).first()
                projet=db.session.query(Projet).filter(Projet.id==f.projet_id).first()

                if  projet:
                    clients.append({"id":f.id,"titre":f.titre,"projet":projet.nom,"priorite":f.priorite,"date_echeance":f.date_echeance,"description":f.description,"date_creation":f.created_at})
                else:
                    #print(u.nom)
                    clients.append({"id":f.id,"titre":f.titre,"priorite":f.priorite,"date_echeance":f.date_echeance,"description":f.description,"date_creation":f.created_at})


            retour={"code":200,"title":"Tache "+str(id),"contenu":clients,"taille":len(clients)}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
    


@app.route('/tacheByStatut' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getTacheByStatut():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            statut=data['statut']

            tache=db.session.query(Tache).filter(Tache.statut==statut)

            for f in tache:
                 

                #employe=db.session.query(User).filter(User.id==f.user_id).first()
                projet=db.session.query(Projet).filter(Projet.id==f.projet_id).first()

                if  projet:
                    clients.append({"id":f.id,"titre":f.titre,"projet":projet.nom,"priorite":f.priorite,"date_echeance":f.date_echeance,"description":f.description,"date_creation":f.created_at})
                else:
                    #print(u.nom)
                    clients.append({"id":f.id,"titre":f.titre,"priorite":f.priorite,"date_echeance":f.date_echeance,"description":f.description,"date_creation":f.created_at})


            retour={"code":200,"title":"Tache "+str(id),"contenu":clients,"taille":len(clients)}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
    
    