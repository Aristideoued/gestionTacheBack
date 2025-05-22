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
from models.departementModel import Departement

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




@app.route('/addDepartement' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addDepartement():
    if request.method=='POST':
            data = request.get_json()
            
            nom=data["nom"]
            
            dep=Departement(nom)
            db.session.add(dep)
            db.session.commit()


            retour={"code":200,"title":"Creation d'un Departement","contenu":"Departement ajouté avec succes"}
            return make_response(jsonify(retour),200)
                
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/delete/Departement' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_Departement():
    if request.method=='POST':
            
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Departement).filter(Departement.id==id).first()
            if user1:
                Departement.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression d'un Departement","contenu":"Departement supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Departement non trouvée"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/all/departements' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getDepartement():
    if request.method=='GET':
            historiques=[]
            historique = Departement.query.all()
            #user=db.session.query(User).all()

            for u in historique:

                

                
                historiques.append({"id":u.id,"nom":u.nom})


            retour={"code":200,"title":"Liste des Departementss","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)
    

@app.route('/departements' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getDepartementParPage():
    if request.method=='GET':
            historiques=[]
           
            #user=db.session.query(User).all()
              

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=60, type=int)
            #cat = request.args.get('categorie', type=int)
            historique=Departement.query.paginate(page=page, per_page=per_page, error_out=False)
           

            for u in historique:

                
                historiques.append({"id":u.id,"nom":u.nom})

                


            retour={"code":200,"title":"Liste des Departementss","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)


@app.route('/departementById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getDepartementById():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            u=db.session.query(Departement).filter(Departement.id==id).first()
            
           
            
            clients.append({"id":u.id,"nom":u.nom})

                

               
   

            retour={"code":200,"title":"Departement "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)


@app.route('/update/departement' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def updateDepartement():
    if request.method=='POST':
            data = request.get_json()
            
            id = int(data['id'])
            
            nom=data["nom"]
            
            dep=db.session.query(Departement).filter(Departement.id==id).first()
            if dep:
                dep.nom=nom
               
                db.session.add(dep)
                db.session.commit()

                retour={"code":200,"title":"Modification d'un Departement","contenu":"Departement modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Departement non trouvé"}
                return make_response(jsonify(retour),401)

           
                 
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)







