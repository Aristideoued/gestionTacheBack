
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
from models.adminLenModel import AdminLen
from models.adminModel import Admin
from api import app,db
from flask import make_response
from api import app,db,auth,authenticate



@app.route('/taille/admins' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getLenAdmin():
    if request.method=='GET':
            historiques=[]
            lenAb=db.session.query(AdminLen).filter(AdminLen.id==1).first()

            #user=db.session.query(User).all()

           
          
            historiques.append({"taille":lenAb.taille})


            retour={"code":200,"title":"La taille","contenu":historiques}
            #print(users[0])
            return make_response(jsonify(retour),200)


@app.route('/registerAdmin' ,methods=['GET','POST'])
@cross_origin(origin='*')
def registerAdmin():
    if request.method=='POST':
            test=False
            data = request.get_json()

            nom=data['nom']
            prenom=data['prenom']
            username=data['username']
            password=data['password']
            telephone=data['telephone']

           
            hashed_password = hashlib.sha256((password).encode("utf-8")).hexdigest()
            user1=db.session.query(Admin).filter(Admin.username==username).first()
            if user1:
                retour={"code":401,"title":"Echec de reation de compte","contenu":"Ce username est deja associé à un compte"}
                return make_response(jsonify(retour),401)
                

            else :
                user=Admin(nom,prenom,username,hashed_password,telephone)
                db.session.add(user)
                db.session.commit()
                abLen=db.session.query(AdminLen).filter(AdminLen.id==1).first()
                abLen.taille+=1
                db.session.add(abLen)
                db.session.commit()
                retour={"code":200,"title":"Creation de compte","contenu":"Compte crée avec succes"}
                return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/admins' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getAdmins():
    if request.method=='GET':
            admins=[]
            admin = Admin.query.all()
            #user=db.session.query(User).all()

            for f in admin:
                #print(u.nom)
                admins.append({"id":f.id,"nom":f.nom,"prenom":f.prenom,"username":f.username,"telephone":f.telephone})


            retour={"code":200,"title":"Liste des admins","contenu":admins,"taille":len(admins)}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)



@app.route('/loginAdmin' ,methods=['GET','POST','OPTIONS'])
@auth.login_required
@cross_origin(origin='*')
def loginAdmin():
    if request.method=='POST':
            #print(request.get_json())
            data = request.get_json()

            email=data['username']
            password=data['password']
            hashed_password = hashlib.sha256((password).encode("utf-8")).hexdigest()
            admin=db.session.query(Admin).filter(Admin.password==hashed_password).filter(Admin.username==email).first()
            #admin2=db.session.query(Client).filter(Client.telephone==telephone).first()
            if admin:
                retour={"code":200,"title":"Connexion","contenu":"Connexion reussie","nom":admin.nom,"prenom":admin.prenom,"id":admin.id,"username":admin.username,"telephone":admin.telephone}
                return make_response(jsonify(retour),200)
            else :
                retour={"code":401,"title":"Connexion","contenu":"Echec de connexion, identifiants incorrects"}
                return make_response(jsonify(retour),401)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/update/admin' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def updateAdmin():
    if request.method=='POST':
            test=False
            data = request.get_json()

            nom=data['nom']
            prenom=data['prenom']
            username=data['username']
            password=data['password']
            telephone=data["telephone"]
            id=int(data['id'])
            user1=db.session.query(Admin).filter(Admin.id==id).first()
            if user1:
                retour={"code":401,"title":"Echec de modification de compte","contenu":"Cet admin exist"}
                return make_response(jsonify(retour),401)
                

            else :
                user=Admin(nom,prenom,username,hashed_password,telephone)
                db.session.add(user)
                db.session.commit()
                retour={"code":200,"title":"Creation de compte","contenu":"Compte crée avec succes"}
                return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)

