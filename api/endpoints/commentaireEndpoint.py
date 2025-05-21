from flask import Flask,request,jsonify,send_file,Response
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
#from response import testpay_response
from PIL import Image
import glob
from flask_cors import cross_origin
import hashlib, uuid
import os
import base64
import pdfcrowd
import sys
import os
from datetime import datetime
from models.tacheModel import Tache
import requests, json

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from models.adminModel import Admin
from models.commentaireModel import Commentaire

from models.userModel import User

from api import app,db
from flask import make_response
from api import app,db,auth,authenticate


UPLOAD_FOLDER = 'types'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','pdf','mov', 'avi', 'mp4', 'flv', 'wmv', 'webm', 'mkv', 'svf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MYDIR = os.path.dirname(__file__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/addCommentaire' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addCommentaire():
    if request.method=='POST':
            data = request.get_json()
            user_id=int(data["user_id"])
            tache_id=int(data["tache_id"])
            contenue=data["contenue"]

            now = datetime.now()

            # Convertir en string
            date_str = now.strftime("%Y-%m-%d %H:%M:%S")
                        
            created_at=date_str

          
                    
            
            

            comm=Commentaire(user_id,tache_id,contenue,created_at)
            db.session.add(comm)
            db.session.commit()


            retour={"code":200,"title":"Creation d'un Commentaire","contenu":"Commentaire ajouté avec succes"}
            return make_response(jsonify(retour),200)
                
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/delete/commentaire' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_Commentaire():
    if request.method=='POST':
            
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Commentaire).filter(Commentaire.id==id).first()
            if user1:
                Commentaire.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression d'un Commentaire","contenu":"Commentaire supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Commentaire non trouvée"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/all/commentaires' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getCommentaire():
    if request.method=='GET':
            historiques=[]
            historique = Commentaire.query.all()
            #user=db.session.query(User).all()

            for u in historique:

                employe=db.session.query(User).filter(User.id==u.user_id).first()
                
                tache=db.session.query(Tache).filter(Tache.id==u.tache_id).first()

                
                historiques.append({"id":u.id,"date":u.created_at,"contenu":u.contenue,"responsable":employe.nom+" "+employe.prenom,"tache":tache.titre})


            retour={"code":200,"title":"Liste des Commentairess","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)
    

@app.route('/commentaires' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getCommentaireParPage():
    if request.method=='GET':
            historiques=[]
           
            #user=db.session.query(User).all()
              

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=60, type=int)
            #cat = request.args.get('categorie', type=int)
            historique=Commentaire.query.paginate(page=page, per_page=per_page, error_out=False)
           

            for u in historique:

                employe=db.session.query(User).filter(User.id==u.user_id).first()
                
                tache=db.session.query(Tache).filter(Tache.id==u.tache_id).first()

                
                historiques.append({"id":u.id,"date":u.created_at,"contenu":u.contenue,"responsable":employe.nom+" "+employe.prenom,"tache":tache.titre})

                


            retour={"code":200,"title":"Liste des Commentairess","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)


@app.route('/commentaireById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getCommentaireById():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            u=db.session.query(Commentaire).filter(Commentaire.id==id).first()
            
            employe=db.session.query(User).filter(User.id==u.user_id).first()
            
            tache=db.session.query(Tache).filter(Tache.id==u.tache_id).first()

            
            clients.append({"id":u.id,"date":u.created_at,"contenu":u.contenue,"responsable":employe.nom+" "+employe.prenom,"tache":tache.titre})

                

               
   

            retour={"code":200,"title":"Commentaire "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)


@app.route('/update/commentaire' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def updateCommentaire():
    if request.method=='POST':
            data = request.get_json()
            
            id = int(data['id'])
            user_id = int(data['user_id'])
            tache_id = int(data['tache_id'])
            contenue=data["contenue"]
            
            comm=db.session.query(Commentaire).filter(Commentaire.id==id).first()
            if comm:
                comm.contenue=contenue
                comm.user_id=user_id
                comm.tache_id=tache_id
                db.session.add(comm)
                db.session.commit()

                retour={"code":200,"title":"Modification d'un Commentaire","contenu":"Commentaire modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Commentaire non trouvé"}
                return make_response(jsonify(retour),401)

           
                 
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)







