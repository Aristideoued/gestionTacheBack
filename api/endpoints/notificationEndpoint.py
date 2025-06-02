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
from models.notificationLenModel import NotificationLen
from models.tacheModel import Tache
import requests, json

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from models.adminModel import Admin
from models.notificationModel import Notification

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


@app.route('/taille/notifications' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getLenNotif():
    if request.method=='GET':
            historiques=[]
            lenAb=db.session.query(NotificationLen).filter(NotificationLen.id==1).first()

            #user=db.session.query(User).all()

           
          
            historiques.append({"taille":lenAb.taille})


            retour={"code":200,"title":"La taille","contenu":historiques}
            #print(users[0])
            return make_response(jsonify(retour),200)



@app.route('/addNotification' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addNotification():
    if request.method=='POST':
            data = request.get_json()
            user_id=int(data["user_id"])
            
            type=data["type"]
            message=data["message"]

            now = datetime.now()

            # Convertir en string
            date_str = now.strftime("%Y-%m-%d %H:%M:%S")
                        
            created_at=date_str

            notif=Notification(message,type,user_id,created_at)
            db.session.add(notif)
            db.session.commit()
            abLen=db.session.query(NotificationLen).filter(NotificationLen.id==1).first()
            abLen.taille+=1
            db.session.add(abLen)
            db.session.commit()


            retour={"code":200,"title":"Creation d'un Notification","contenu":"Notification ajouté avec succes"}
            return make_response(jsonify(retour),200)
                
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/delete/notification' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_Notification():
    if request.method=='POST':
            
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Notification).filter(Notification.id==id).first()
            if user1:
                Notification.query.filter_by(id=id).delete()
                db.session.commit()
                abLen=db.session.query(NotificationLen).filter(NotificationLen.id==1).first()
                abLen.taille-=1
                db.session.add(abLen)
                db.session.commit()

                retour={"code":200,"title":"Suppression d'un Notification","contenu":"Notification supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Notification non trouvée"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/all/notifications' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getNotification():
    if request.method=='GET':
            notifications=[]
            notification = Notification.query.all()
            #user=db.session.query(User).all()

            for u in notification:

                employe=db.session.query(User).filter(User.id==u.user_id).first()
                

                
                notifications.append({"id":u.id,"date":u.created_at,"type":u.type,"message":u.message,"destinataire":employe.nom+" "+employe.prenom})


            retour={"code":200,"title":"Liste des Notificationss","contenu":notifications,"taille":len(notifications)}
            #print(users[0])
            return make_response(jsonify(retour),200)
    

@app.route('/notifications' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getNotificationParPage():
    if request.method=='GET':
            notifications=[]
           
            #user=db.session.query(User).all()
              

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=60, type=int)
            #cat = request.args.get('categorie', type=int)
            notification=Notification.query.paginate(page=page, per_page=per_page, error_out=False)
           

            for u in notification:

                employe=db.session.query(User).filter(User.id==u.user_id).first()
                

                
                notifications.append({"id":u.id,"date":u.created_at,"type":u.type,"message":u.message,"destinataire":employe.nom+" "+employe.prenom})

                


            retour={"code":200,"title":"Liste des Notificationss","contenu":notifications,"taille":len(notifications)}
            #print(users[0])
            return make_response(jsonify(retour),200)


@app.route('/notificationById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getNotificationById():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            u=db.session.query(Notification).filter(Notification.id==id).first()
            
            employe=db.session.query(User).filter(User.id==u.user_id).first()
            

            
            clients.append({"id":u.id,"date":u.created_at,"type":u.type,"message":u.message,"destinataire":employe.nom+" "+employe.prenom})

                

               
   

            retour={"code":200,"title":"Notification "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)




@app.route('/notificationByUser' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getNotificationByUser():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            user_id=int(data['user_id'])

            employe=db.session.query(User).filter(User.id==user_id).first()


            notifs=db.session.query(Notification).filter(Notification.user_id==user_id)
            for u in notifs:
                 
                clients.append({"id":u.id,"date":u.created_at,"type":u.type,"message":u.message,"destinataire":employe.nom+" "+employe.prenom})

                    

            
            retour={"code":200,"title":"Notification "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)



@app.route('/update/notification' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def updateNotification():
    if request.method=='POST':
            data = request.get_json()
            
            id = int(data['id'])
            user_id = int(data['user_id'])
            est_lue = bool(data['est_lue'])
            message=data["message"]
            type=data["type"]
            
            notif=db.session.query(Notification).filter(Notification.id==id).first()
            if notif:
                notif.message=message
                notif.type=type
                notif.user_id=user_id
                notif.est_lue=est_lue
                db.session.add(notif)
                db.session.commit()

                retour={"code":200,"title":"Modification d'un Notification","contenu":"Notification modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Notification non trouvé"}
                return make_response(jsonify(retour),401)

           
                 
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)







