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
import sys
import os
from datetime import datetime
from models.tacheModel import Tache
import requests, json

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from models.adminModel import Admin
from models.beneficiaireModel import Beneficiaire

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




@app.route('/addBeneficiaire' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addBeneficiaire():
    if request.method=='POST':
            data = request.get_json()

            nom=data["nom"]
            prenom=data["prenom"]
            structure=data["structure"]
            email=data["email"]
            telephone=data["telephone"]
                    
            benef=Beneficiaire(nom,prenom,structure,email,telephone)
            db.session.add(benef)
            db.session.commit()


            retour={"code":200,"title":"Creation d'un beneficiaire","contenu":"Beneficiaire ajouté avec succes"}
            return make_response(jsonify(retour),200)
                
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/delete/beneficiaire' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_beneficiaire():
    if request.method=='POST':
            
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Beneficiaire).filter(Beneficiaire.id==id).first()
            if user1:
                Beneficiaire.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression d'un beneficiaire","contenu":"beneficiaire supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"beneficiaire non trouvée"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/all/beneficiaires' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getBeneficiaire():
    if request.method=='GET':
            historiques=[]
            historique = Beneficiaire.query.all()
            #user=db.session.query(User).all()

            for u in historique:
                
                historiques.append({"id":u.id,"nom":u.nom,"prenom":u.prenom,"structure":u.structure,"email":u.email,"telephone":u.telephone})


            retour={"code":200,"title":"Liste des beneficiairess","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)
    

@app.route('/beneficiaires' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getBeneficiaireParPage():
    if request.method=='GET':
            historiques=[]
           
            #user=db.session.query(User).all()
              

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=60, type=int)
            #cat = request.args.get('categorie', type=int)
            historique=Beneficiaire.query.paginate(page=page, per_page=per_page, error_out=False)
           

            for u in historique:
                
                historiques.append({"id":u.id,"nom":u.nom,"prenom":u.prenom,"structure":u.structure,"email":u.email,"telephone":u.telephone})


            retour={"code":200,"title":"Liste des beneficiairess","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)


@app.route('/beneficiaireById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getBeneficiaireById():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            benef=db.session.query(Beneficiaire).filter(Beneficiaire.id==id).first()

               
   
            clients.append({"id":benef.id,"nom":benef.nom,"prenom":benef.prenom,"structure":benef.structure,"email":benef.email,"telephone":benef.telephone})

            retour={"code":200,"title":"Beneficiaire "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)


@app.route('/update/beneficiaire' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def updateBeneficiaire():
    if request.method=='POST':
            data = request.get_json()
            
            id = int(data['id'])
            nom=data["nom"]
            prenom=data["prenom"]
            structure=data["structure"]
            email=data["email"]
            telephone=data["telephone"]
            
            benef=db.session.query(Beneficiaire).filter(Beneficiaire.id==id).first()
            if benef:
                benef.nom=nom
                benef.prenom=prenom
                benef.structure=structure
                benef.email=email
                benef.telephone=telephone
                

                db.session.add(benef)
                db.session.commit()

                retour={"code":200,"title":"Modification d'un beneficiaire","contenu":"Beneficiaire modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Beneficiaire non trouvé"}
                return make_response(jsonify(retour),401)

           
                 
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)







