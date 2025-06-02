

from flask import Flask,request,jsonify,send_file
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
#from response import testpay_response
from PIL import Image
import glob
from flask_cors import cross_origin
import hashlib, uuid
import os
import random,requests
from datetime import datetime,timedelta
from api import app,db
from flask import make_response
from api import app,db,auth,authenticate
from threading import Timer


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from models.pieceLenModel import PieceLen
from models.userModel import User
from models.tacheModel import Tache
from models.pieceModel import Piece


UPLOAD_FOLDER = 'fichiers'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','pdf','mov', 'avi', 'mp4', 'flv', 'wmv', 'webm', 'mkv', 'svf','docx','xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MYDIR = os.path.dirname(__file__)






def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/taille/pieces' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getLenPiece():
    if request.method=='GET':
            historiques=[]
            lenAb=db.session.query(PieceLen).filter(PieceLen.id==1).first()

            #user=db.session.query(User).all()

           
          
            historiques.append({"taille":lenAb.taille})


            retour={"code":200,"title":"La taille","contenu":historiques}
            #print(users[0])
            return make_response(jsonify(retour),200)

@app.route('/saveFile/<user_id>/<tache_id>', methods=['GET', 'POST'])
@cross_origin(origin='*')
def upload_file(user_id,tache_id):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
             retour={"code":401,"title":"Fichier inconnu","contenu":"Fichier inconnu"}
             return make_response(jsonify(retour),401)

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
           retour={"code":401,"title":"Fichier non selectionné","contenu":"Fichier inconnu"}
           return make_response(jsonify(retour),401)

        if file and allowed_file(file.filename):
            print(file.filename)
            user=db.session.query(User).filter(User.id==user_id).first()
            if os.path.isdir("fichiers/"+user.nom+'_'+user.prenom +str(user.id)):
                
                
                file.save(os.path.join(MYDIR + "/fichiers/"+user.nom+'_'+user.prenom +str(user.id), file.filename))
                
                now = datetime.now()

                # Convertir en string
                date_str = now.strftime("%Y-%m-%d %H:%M:%S")
                            
                created_at=date_str
                piece=Piece(user_id,tache_id,file.filename,created_at)
                
                db.session.add(piece)
                db.session.commit()
                abLen=db.session.query(PieceLen).filter(PieceLen.id==1).first()
                abLen.taille+=1
                db.session.add(abLen)
                db.session.commit()
    
                retour={"code":200,"title":"Fichier chargé","contenu":"Fichier chargé"}
                return make_response(jsonify(retour),200)
                
            else:
                user_folder_path = os.path.join(MYDIR + "/fichiers/"+user.nom+'_'+user.prenom +str(user.id))
                os.makedirs(user_folder_path, exist_ok=True)
                #os.makedirs(app.config['UPLOAD_FOLDER']+ "/users/"+str(user1.email))
            #filename = secure_filename(file.filename)
                file.save(os.path.join(MYDIR + "/fichiers/"+user.nom+'_'+user.prenom +str(user.id), file.filename))
            #return redirect(url_for('download_file', name=filename))
                now = datetime.now()

                # Convertir en string
                date_str = now.strftime("%Y-%m-%d %H:%M:%S")
                            
                created_at=date_str
                piece=Piece(user_id,tache_id,file.filename,created_at)
                
                db.session.add(piece)
                db.session.commit()
    
                retour={"code":200,"title":"Fichier chargé","contenu":"Fichier chargé"}
                return make_response(jsonify(retour),200)



@app.route('/fileById/<id>' ,methods=['GET','POST'])
@cross_origin(origin='*')
def getFileById(id):
    if request.method=='GET':

            piece=db.session.query(Piece).filter(Piece.id==id).first()
            if piece :
                user=db.session.query(User).filter(User.id==piece.user_id).first()


                send_file(MYDIR+"/fichiers"+user.nom+'_'+user.prenom +str(user.id)+"/"+piece.nom, as_attachment=True)
                

            else:
                retour={"code":404,"title":"NotFound","contenu":"Piece non trouvée"}
                return make_response(jsonify(retour),404)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode get"}
      return make_response(jsonify(retour),403)




@app.route('/getFile/<tache_id>/' ,methods=['GET','POST'])
@cross_origin(origin='*')
def getTacheFile(tache_id):
    if request.method=='GET':
            tache=db.session.query(Tache).filter(Tache.id==tache_id).first()
            files=[]

            if tache :
                piece=db.session.query(Piece).filter(Piece.tache_id==tache_id)
                for p in piece:
                    files.append({"url":"http://localhost:5500/fileById/"+str(p.id)})


                retour={"code":200,"title":"Fichiers","contenu":"Les fichiers joins à la tache "+tache.titre}
                return make_response(jsonify(retour),404)
            else:
                retour={"code":404,"title":"NotFound","contenu":"Tache non trouvée"}
                return make_response(jsonify(retour),404)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode get"}
      return make_response(jsonify(retour),403)




