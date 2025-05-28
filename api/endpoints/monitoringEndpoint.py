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
from models.monitoringModel import Monitoring
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





@app.route('/addMonitoring' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addMonitoring():
    if request.method=='POST':
            data = request.get_json()
            commentaire=data['commentaire']
            statut=data['statut']
            

            url=data['url']
            beneficiaire=data['beneficiaire']
            dateMonitoring=data['dateMonitoring']

            user1=db.session.query(Monitoring).filter(Monitoring.url==url).first()

            if user1:
                retour={"code":401,"Title":"Ajout d'un Monitoring","contenu":"Un site existe deja avec cete addresse"}
                return make_response(jsonify(retour),401)
            else:
                         
                proj=Monitoring(url,beneficiaire,statut,dateMonitoring,commentaire)
            
                db.session.add(proj)
                db.session.commit()
                retour={"code":200,"Title":"Ajout d'un Monitoring","contenu":"Monitoring ajouté avec succès"}
                return make_response(jsonify(retour),200)
        
           
                 
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/delete/monitoring' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_Monitoring():
    if request.method=='POST':
            
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Monitoring).filter(Monitoring.id==id).first()
            if user1:
                Monitoring.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression d'un Monitoring","contenu":"Monitoring supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Monitoring non trouvé"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/all/monitorings' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getMonitoring():
    if request.method=='GET':
            historiques=[]
            historique = Monitoring.query.all()
            #user=db.session.query(User).all()

            for u in historique:
          
                historiques.append({"url":u.url,"statut":u.statut,"dateMonitoring":u.dateMonitoring,"commentaire":u.commentaire,"beneficiaire":u.beneficiaire})


            retour={"code":200,"title":"Liste des Monitorings","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)
    

@app.route('/monitorings' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getMonitoringParPage():
    if request.method=='GET':
            historiques=[]
           
            #user=db.session.query(User).all()
              

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=60, type=int)
            #cat = request.args.get('categorie', type=int)
            historique=Monitoring.query.paginate(page=page, per_page=per_page, error_out=False)
           

            for u in historique:


                historiques.append({"url":u.url,"statut":u.statut,"dateMonitoring":u.dateMonitoring,"commentaire":u.commentaire,"beneficiaire":u.beneficiaire})

            retour={"code":200,"title":"Liste des Monitorings","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)


@app.route('/monitoringById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getMonitoringById():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            u=db.session.query(Monitoring).filter(Monitoring.id==id).first()
            clients.append({"url":u.url,"statut":u.statut,"dateMonitoring":u.dateMonitoring,"commentaire":u.commentaire,"beneficiaire":u.beneficiaire})


    
                #print(u.nom)


            retour={"code":200,"title":"Monitoring "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
    



 

@app.route('/update/monitoring' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def update_Monitoring():
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])
            commentaire=data['commentaire']
            statut=data['statut']
            

            url=data['url']
            beneficiaire=data['beneficiaire']
            dateMonitoring=data['dateMonitoring']
            

            user1=db.session.query(Monitoring).filter(Monitoring.id==id).first()
            
            if user1:
                user1.url=url
                user1.dateMonitoring=dateMonitoring
                user1.beneficiaire=beneficiaire
                user1.statut=statut
                user1.commentaire=commentaire
               
                db.session.add(user1)
                db.session.commit()
               
                

                retour={"code":200,"title":"Modification d'un Monitoring","contenu":"Monitoring modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Monitoring non trouvé"}
                return make_response(jsonify(retour),401)


@app.route('/update/monitoring/status' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def update_Monitoring_status():
    if request.method=='POST':
            test=False
            data = request.get_json()
            url=data['url']
            statut=data['statut']
            dateMonitoring=data['dateMonitoring']
            

            user1=db.session.query(Monitoring).filter(Monitoring.url==url).first()
            
            if user1:
                user1.url=url
                user1.dateMonitoring=dateMonitoring
                user1.statut=statut               
                db.session.add(user1)
                db.session.commit()
               
                

                retour={"code":200,"title":"Modification d'un Monitoring","contenu":"Monitoring modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Monitoring non trouvé"}
                return make_response(jsonify(retour),401)


