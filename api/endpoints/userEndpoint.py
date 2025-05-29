

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

from models.userModel import User
from models.departementModel import Departement
from models.roleModel import Role
from models.tacheModel import Tache


UPLOAD_FOLDER = 'fichiers'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','pdf','mov', 'avi', 'mp4', 'flv', 'wmv', 'webm', 'mkv', 'svf','docx','xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MYDIR = os.path.dirname(__file__)


@app.route('/userRegister' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addUser():
    if request.method=='POST':

            data = request.get_json()
            nom=data["nom"]
            prenom=data["prenom"]
            
            departement_id=int(data['departement_id'])
            titre=data["titre"]
            
            phone=data["phone"]
            email=data['email']
            password=data['password']
            role_id=int(data['role_id'])

           
            hashed_password = hashlib.sha256((password).encode("utf-8")).hexdigest()

            user=db.session.query(User).filter(User.email==email).first()
            user2=db.session.query(User).filter(User.phone==phone).first()

            if user or user2:
                retour={"code":401,"title":"Ajout d'un utilisateur","contenu":"Utilisateur non ajouté , un compte avec cet email/telephone existe deja"}
                return make_response(jsonify(retour),401)
            else:

                
                user=User(nom,prenom,phone,email,hashed_password,role_id,departement_id,titre)
                db.session.add(user)
                db.session.commit()
                #retour={"code":200,"title":"Envoie de code au User","contenu":"Code envoyé avec succès"}
                #return make_response(jsonify(retour),200)
             

                retour={"code":200,"title":"Ajout d'un utilisateur","contenu":"Utilisateur ajouté avec succes","User":{"id":user.id,"firstname":user.firstname,"lastname":user.lastname}}
                return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/userByDepartement' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getUserByDepartement():
    if request.method=='POST':
            users=[]
            data = request.get_json()

            departement_id=int(data['departement_id'])

            user=db.session.query(User).filter(User.departement_id==departement_id)
            for f in user:

                statut=""
                if f:
                    if f.statut==1:
                        statut=="Actif"
                    else:
                        statut="Inactif"


                    role=db.session.query(Role).filter(Role.id==f.role_id).first()


                    users.append({"id":f.id,"statut":statut,"nom":f.nom,"prenom":f.prenom,"titre":f.titre,"phone":f.phone,"email":f.email,"role_id":f.role_id,"role":role.role,"permissions":role.permissions})

                    retour={"code":200,"title":"User "+str(id),"contenu":users}
                    #print(users[0])
                    return make_response(jsonify(retour),200)
                else:
                    retour={"code":404,"title":"User "+str(id),"contenu":"User non trouvé"}
                    #print(users[0])
                    return make_response(jsonify(retour),404)


    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)



@app.route('/userById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getUserById():
    if request.method=='POST':
            users=[]
            data = request.get_json()

            id=int(data['id'])

            f=db.session.query(User).filter(User.id==id).first()
            statut=""
            if f:
                if f.statut==1:
                    statut=="Actif"
                else:
                    statut="Inactif"


                role=db.session.query(Role).filter(Role.id==f.role_id).first()
                dep=db.session.query(Departement).filter(Departement.id==f.departement_id).first()


                users.append({"id":f.id,"statut":statut,"nom":f.nom,"prenom":f.prenom,"departement":dep.nom,"titre":f.titre,"phone":f.phone,"email":f.email,"role_id":f.role_id,"role":role.role,"permissions":role.permissions})

                retour={"code":200,"title":"User "+str(id),"contenu":users}
                #print(users[0])
                return make_response(jsonify(retour),200)
            else:
                retour={"code":404,"title":"User "+str(id),"contenu":"User non trouvé"}
                #print(users[0])
                return make_response(jsonify(retour),404)


    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)





@app.route('/delete/user' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_user():
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(User).filter(User.id==id).first()
            
            if user1:
                User.query.filter_by(id=id).delete()
                db.session.commit()
            
                retour={"code":200,"title":"Suppression de compte User","contenu":"Compte supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)


    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/getcode' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def find_user():
    if request.method=='POST':
            test=False
            data = request.get_json()

            email=data['email']

            user1=db.session.query(User).filter(User.email==email).first()
            if user1:
                code=str(random.randint(100000, 999999))
                destinataire=email
                expediteur= "contact@codingagain.com"
                sujet = "Code de Récupération de Compte eProfile"
                message = MIMEMultipart()
                message['From'] = expediteur
                message['To'] = destinataire
                message['Subject'] = sujet
                corps_du_message = "Cher utilisateur,\n\n\nNous avons reçu une demande de récupération de compte associé à cette adresse e-mail sur eProfile. Afin de garantir la sécurité de votre compte, veuillez utiliser le code de vérification ci-dessous pour confirmer votre demande de récupération :\n\n\nCode de vérification : "+code+" \n\n\nVeuillez entrer ce code sur la page de récupération de compte.\nAssurez vous de ne pas partager ce code avec quiconque. \nSi vous n'avez pas effectué cette demande, veuillez ignorer ce message\nSi vous avez des questions ou des préoccupations, n'hésitez pas à nous contacter à contact@codingagain.com.\n\n\nCordialement,\n\nL'équipe eProfile"
                message.attach(MIMEText(corps_du_message, 'plain'))
                serveur_smtp = "mail.codingagain.com"
                port_smtp = 465
                nom_utilisateur = "contact@codingagain.com"
                mot_de_passe = "2885351Aristide12@"
                s = smtplib.SMTP_SSL(host='mail.codingagain.com', port=465)
                s.login(nom_utilisateur, mot_de_passe)
                texte = message.as_string()
                s.sendmail(expediteur, destinataire, texte)
                s.quit()
                user1.code=code
                db.session.add(user1)
                db.session.commit()
                retour={"code":200,"title":"Envoie de code au User","contenu":"Code envoyé avec succès"}
                return make_response(jsonify(retour),200)
             

                    
           
               
            else :

                retour={"code":401,"title":"Echec","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/compte/validation' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def valide_user_by_code():
    if request.method=='POST':
           
            data = request.get_json()

            email=data['email']
            code=str(data['code'])
            #print(code)

            user1=db.session.query(User).filter(User.email==email).filter(User.code==code).first()
            if user1:
                moment=datetime.now()
        
                user1.code=None
                user1.is_active=1
                user1.verifyed_at=  moment 
                db.session.add(user1)
                db.session.commit()           
                retour={"code":200,"title":"Verification de code ","contenu":"Compte validé avec succès","User":user1.id}
                return make_response(jsonify(retour),200)
       
            else:
                retour={"code":401,"title":"Echec","contenu":"Code invalide, reesayer"}
                return make_response(jsonify(retour),401)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


@app.route('/validecode' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def find_user_by_code():
    if request.method=='POST':
           
            data = request.get_json()

            email=data['email']
            code=data['code']
            print(code)

            user1=db.session.query(User).filter(User.email==email).filter(User.code==code).first()
            if user1:              
                retour={"code":200,"title":"Verification de code du User","contenu":"Code valide","User":user1.id}
                return make_response(jsonify(retour),200)
       
            else:
                retour={"code":401,"title":"Echec","contenu":"Code invalide, reesayer"}
                return make_response(jsonify(retour),401)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


@app.route('/update/user/password' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def update_user_password():
    if request.method=='POST':
            
            data = request.get_json()

            id=int(data['id'])
            password=data['password']
            hashed_password = hashlib.sha256((password).encode("utf-8")).hexdigest()
            
            user1=db.session.query(User).filter(User.id==id).first()
            if user1:
                user1.code=None
                user1.password=hashed_password
                db.session.add(user1)
                db.session.commit()

                retour={"code":200,"title":"Modification de mot de passe","contenu":"Mot de passe modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/update/user' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def update_user():
    if request.method=='POST':
            
            data = request.get_json()
            nom=data["nom"]
            prenom=data["prenom"]
            
            departement_id=int(data['departement_id'])
            titre=data["titre"]
            
            phone=data["phone"]
            email=data['email']
            role_id=int(data['role_id'])
        
            id=int(data['id'])

            user1=db.session.query(User).filter(User.id==id).first()
            if user1:
                user1.nom=nom
                user1.prenom=prenom
                user1.phone=phone
                user1.email=email
                user1.titre=titre
                user1.departement_id=departement_id
                
                user1.role_id=role_id
                db.session.add(user1)
                db.session.commit()

                retour={"code":200,"title":"Modification de compte","contenu":"Compte modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


@app.route('/update/user/statut' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def update_user_statut():
    if request.method=='POST':
            
            data = request.get_json()
            
            statut=int(data['statut'])
        
            id=int(data['id'])

            user1=db.session.query(User).filter(User.id==id).first()
            if user1:
                user1.statut=statut
                
                db.session.add(user1)
                db.session.commit()

                retour={"code":200,"title":"Modification de compte","contenu":"Compte modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/all/users' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getUser():
    if request.method=='GET':
            users=[]
            user = User.query.all()
            #user=db.session.query(User).all()

            for f in user:
                statut=""

                if f.statut==1:
                    statut=="Actif"
                else:
                    statut="Inactif"
                #print(u.nom)
                role=db.session.query(Role).filter(Role.id==f.role_id).first()
                dep=db.session.query(Departement).filter(Departement.id==f.departement_id).first()

                users.append({"id":f.id,"statut":statut,"nom":f.nom,"prenom":f.prenom,"departement":dep.nom,"titre":f.titre,"phone":f.phone,"email":f.email,"role_id":f.role_id,"role":role.role,"permissions":role.permissions})
            retour={"code":200,"title":"Liste des users","contenu":users,"taille":len(users)}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)



@app.route('/users' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getUserPerPage():
    if request.method=='GET':
            users=[]
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=60, type=int)
            #cat = request.args.get('categorie', type=int)
            user=User.query.paginate(page=page, per_page=per_page, error_out=False)
           
            #user=db.session.query(User).all()

            for f in user:
                #print(u.nom)
                if f.statut==1:
                    statut=="Actif"
                else:
                    statut="Inactif"
                role=db.session.query(Role).filter(Role.id==f.role_id).first()
                dep=db.session.query(Departement).filter(Departement.id==f.departement_id).first()

                users.append({"id":f.id,"statut":statut,"nom":f.nom,"prenom":f.prenom,"departement":dep.nom,"titre":f.titre,"phone":f.phone,"email":f.email,"role_id":f.role_id,"role":role.role,"permissions":role.permissions})
            retour={"code":200,"title":"Liste des users","contenu":users,"taille":len(users)}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)


def ressetCode(c,d):
    c.code=None
    db.session.add(c)
    db.session.commit()
    print(d)



@app.route('/loginUser' ,methods=['GET','POST','OPTIONS'])
@auth.login_required
@cross_origin(origin='*')
def loginUser():
    if request.method=='POST':
            #print(request.get_json())
            data = request.get_json()

            email=data['email']
            password=data['password']
            hashed_password = hashlib.sha256((password).encode("utf-8")).hexdigest()
            admin=db.session.query(User).filter(User.password==hashed_password).filter(User.email==email).first()
            #admin2=db.session.query(User).filter(User.telephone==telephone).first()
            if admin:
                role=db.session.query(Role).filter(Role.id==admin.role_id).first()

                retour={"code":200,"title":"Connexion","contenu":"Connexion reussie","id":admin.id,"code_agent":admin.code_agent,"firstname":admin.firstname,"lastname":admin.lastname,"phone":admin.phone,"email":admin.email,"cnib_pasport":admin.cnib_pasport,"is_active":admin.is_active,"bithdate":admin.bithdate,"city":admin.city,"role_id":role.id,"role":role.role}
                
                #retour={"code":200,"title":"Connexion","contenu":"Connexion reussie","nom":admin.nom,"nbExperience":admin.prenom.split("@")[1],"prenom":admin.prenom.split("@")[0],"id":admin.id,"telephone":admin.telephone,"abonnement":admin.etatAbonnement,"dateAbonnement":admin.dateAbonnement,"disponibilite":admin.disponibilite,"description":admin.description,"photo":admin.photo,"recruteur":"non"}
                return make_response(jsonify(retour),200)
            else :
                retour={"code":401,"title":"Connexion","contenu":"Echec de connexion, identifiants incorrects"}
                return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




