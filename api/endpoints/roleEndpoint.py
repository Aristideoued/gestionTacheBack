

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
from models.adminModel import Admin
from models.roleModel import Role

from api import app,db
from flask import make_response
from api import app,db,auth,authenticate

UPLOAD_FOLDER = 'types'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MYDIR = os.path.dirname(__file__)




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/addRole' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addRole():
    if request.method=='POST':

            data = request.get_json()

            libele=data['role']
            permissions=data['permissions']
            role=db.session.query(Role).filter(Role.role==libele).first()
            if role:
                retour={"code":401,"title":"Echec d'ajout de role","contenu":"Role existant avec ce libele"}
                return make_response(jsonify(retour),401)
            else:
                newRole=Role(libele,permissions)
                db.session.add(newRole)
                db.session.commit()
                retour={"code":200,"title":"Ajout d'un role","contenu":"Role ajouté avec succes"}
                return make_response(jsonify(retour),200)
                
            
            

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)

@app.route('/roleById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getRoleById():
    if request.method=='POST':
            roles=[]
            data = request.get_json()

            id=int(data['id'])

            role=db.session.query(Role).filter(Role.id==id).first()

         
            roles.append({"id":role.id,"role":role.role,"permissions":role.permissions})


            retour={"code":200,"title":"Role "+str(id),"contenu":roles}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)



@app.route('/roles' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getRole():
    if request.method=='GET':
            roles=[]
            role = Role.query.all()
            #user=db.session.query(User).all()

            for f in role:
                #print(u.nom)
                roles.append({"id":f.id,"roles":f.role,"permissions":f.permissions})


            retour={"code":200,"title":"Liste des Roles","contenu":roles,"taille":len(roles)}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)


@app.route('/delete/role' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_Role():
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            role=db.session.query(Role).filter(Role.id==id).first()
            if role:
               # prod=db.session.query(Produit).filter(Produit.Role==id)
                #for produit in prod:
                 #   produit.query.filter_by(Role=id).delete()
                  # db.session.commit()

                Role.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression d'un Role","contenu":"Role supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Role non trouvé"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/update/role' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def update_Role():
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])
            libele=data['role']
            permissions=data['permissions']
            



            role=db.session.query(Role).filter(Role.id==id).first()
            if role:
                role.role=libele
                role.permissions=permissions
                db.session.add(role)
                db.session.commit()

                retour={"code":200,"title":"Modification d'un Role","contenu":"Role modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Role non trouvé"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)







