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
from models.roleModel import Role
from models.projetModel import Projet
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





@app.route('/addProjet' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addProjet():
    if request.method=='POST':
            data = request.get_json()
            nom=data['nom']
            description=data['description']
            date_debut=data['date_debut']
            date_fin_prevue=data['date_fin_prevue']
            statut=data['statut']
            responsable_id=int(data['responsable_id'])
            
                    
            proj=Projet(nom,description,date_debut,date_fin_prevue,statut,responsable_id)
           
            db.session.add(proj)
            db.session.commit()
            retour={"code":200,"Title":"Ajout d'un projet","contenu":"Projet ajouté avec succès"}
            return make_response(jsonify(retour),200)
    
           
                 
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/delete/projet' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_Projet():
    if request.method=='POST':
            
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Projet).filter(Projet.id==id).first()
            if user1:
                Projet.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression d'un Projet","contenu":"Projet supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Projet non trouvé"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/all/projets' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getProjet():
    if request.method=='GET':
            historiques=[]
            historique = Projet.query.all()
            #user=db.session.query(User).all()

            for u in historique:

                employe=db.session.query(User).filter(User.id==u.user_id).first()
                
                
                historiques.append({"date_fin_prevue":u.date_fin_prevue,"statut":u.statut,"id":u.id,"date_debut":u.date_debut,"nom":u.nom,"description":u.description,"responsable":employe.nom+" "+employe.prenom})


            retour={"code":200,"title":"Liste des projets","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)
    

@app.route('/projets' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getProjetParPage():
    if request.method=='GET':
            historiques=[]
           
            #user=db.session.query(User).all()
              

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=60, type=int)
            #cat = request.args.get('categorie', type=int)
            historique=Projet.query.paginate(page=page, per_page=per_page, error_out=False)
           

            for u in historique:


                employe=db.session.query(User).filter(User.id==u.user_id).first()
                
                
                historiques.append({"date_fin_prevue":u.date_fin_prevue,"statut":u.statut,"id":u.id,"date_debut":u.date_debut,"nom":u.nom,"description":u.description,"responsable":employe.nom+" "+employe.prenom})

            retour={"code":200,"title":"Liste des projets","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)


@app.route('/projetById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getProjetById():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            u=db.session.query(Projet).filter(Projet.id==id).first()
            employe=db.session.query(User).filter(User.id==u.user_id).first()
            
            clients.append({"date_fin_prevue":u.date_fin_prevue,"statut":u.statut,"id":u.id,"date_debut":u.date_debut,"nom":u.nom,"description":u.description,"responsable":employe.nom+" "+employe.prenom})


    
                #print(u.nom)


            retour={"code":200,"title":"Projet "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
    


@app.route('/projetByUser' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getProjetByUser():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            user_id=int(data['user_id'])

            proj=db.session.query(Projet).filter(Projet.user_id==user_id)
            employe=db.session.query(User).filter(User.id==user_id).first()

            for u in proj:
                 
            
                clients.append({"date_fin_prevue":u.date_fin_prevue,"statut":u.statut,"id":u.id,"date_debut":u.date_debut,"nom":u.nom,"description":u.description,"responsable":employe.nom+" "+employe.prenom})


    
                #print(u.nom)


            retour={"code":200,"title":"Projet "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
    

 

@app.route('/update/projet' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def update_Projet():
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])
            nom=data['nom']
            description=data['description']
            date_debut=data['date_debut']
            date_fin_prevue=data['date_fin_prevue']
            statut=data['statut']
            responsable_id=int(data['responsable_id'])

            user1=db.session.query(Projet).filter(Projet.id==id).first()
            
            if user1:
                user1.date_debut=date_debut
                user1.nom=nom
                user1.date_fin_prevue=date_fin_prevue
                user1.statut=statut
                user1.responsable_id=responsable_id
                user1.description=description
                db.session.add(user1)
                db.session.commit()
               
                

                retour={"code":200,"title":"Modification d'un Projet","contenu":"Projet modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Projet non trouvé"}
                return make_response(jsonify(retour),401)


