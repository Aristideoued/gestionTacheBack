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
from models.departementModel import Transaction
from models.projetModel import TransactionType
from models.userModel import User
from models.tacheModel import Wallet
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from models.adminModel import Admin
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





@app.route('/addTransaction' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def addTransaction():
    if request.method=='POST':
            data = request.get_json()
            
            emitter = int(data['emitter'])
            amount = float(data['amount'])

            emitter_compte=db.session.query(User).filter(User.id==emitter).first()
            emitter_wallet=db.session.query(Wallet).filter(Wallet.user_id==emitter_compte.id).first()
            
            transaction_type_id = int(data['transaction_type_id'])
            transaction_type= db.session.query(TransactionType).filter(TransactionType.id==transaction_type_id).first()


            if transaction_type.type=="Transfert d'argent":
                receiver = data['receiver']
                moment=datetime.now()
                receiver_compte=db.session.query(User).filter(User.phone==str(receiver)).first()
                receiver_wallet=db.session.query(Wallet).filter(Wallet.user_id==receiver_compte.id).first()
                if emitter_wallet.balance<amount:
                    retour={"code":401,"Title":"Transfert d'argent","contenu":"Echec de transfert, solde insuffisant"}
                    return make_response(jsonify(retour),401)
                else:  
                    receiver_wallet.balance=receiver_wallet.balance+amount
                    emitter_wallet.balance=emitter_wallet.balance-amount
                    trans=Transaction(receiver_compte.id,emitter_compte.id,amount,transaction_type_id,moment)
                    db.session.add(receiver_wallet)
                    db.session.add(emitter_wallet)
                    db.session.add(trans)
                    db.session.commit()
                    retour={"code":200,"Title":"Transfert d'argent","contenu":"Transfert effectué avec succès"}
                    return make_response(jsonify(retour),200)
            
            elif transaction_type.type=="Dépot d'argent":
                receiver = data['receiver']
                #code_agent = int(data['code_agent'])

                moment=datetime.now()
                role=db.session.query(Role).filter(Role.id==emitter_compte.role_id).first()
                print("Role==> ",role.role)
                if role.role=="admin":
                    receiver_compte=db.session.query(User).filter(User.code_agent==int(receiver)).first()
                    receiver_wallet=db.session.query(Wallet).filter(Wallet.user_id==receiver_compte.id).first()
            
                    receiver_wallet.balance=receiver_wallet.balance+amount
                    #emitter_wallet.balance=emitter_wallet.balance-amount
                    trans=Transaction(receiver_compte.id,emitter_compte.id,amount,transaction_type_id,moment)
                    db.session.add(receiver_wallet)
                    #db.session.add(emitter_wallet)
                    db.session.add(trans)
                    db.session.commit()
                    retour={"code":200,"Title":"Dépot d'argent","contenu":"Dépot effectué avec succès"}
                    return make_response(jsonify(retour),200)

                
                elif role.role=="agent":
                    if emitter_wallet.balance<amount:
                        retour={"code":401,"Title":"Depot d'argent","contenu":"Echec de depot, solde insuffisant"}
                        return make_response(jsonify(retour),401)
                    else:
                        receiver_compte=db.session.query(User).filter(User.phone==str(receiver)).first()
                        receiver_wallet=db.session.query(Wallet).filter(Wallet.user_id==receiver_compte.id).first()
                
                        receiver_wallet.balance=receiver_wallet.balance+amount
                        emitter_wallet.balance=emitter_wallet.balance-amount
                        trans=Transaction(receiver_compte.id,emitter_compte.id,amount,transaction_type_id,moment)
                        db.session.add(receiver_wallet)
                        db.session.add(emitter_wallet)
                        db.session.add(trans)
                        db.session.commit()
                        retour={"code":200,"Title":"Dépot d'argent","contenu":"Dépot effectué avec succès"}
                        return make_response(jsonify(retour),200)
                else:
                    print("Le role ",role)
                    retour={"code":401,"Title":"Depot d'argent","contenu":"Echec de depot, opération non autorisée"}
                    return make_response(jsonify(retour),401)

                   
            

            elif transaction_type.type=="Retrait d'argent":
                receiver = int(data['receiver'])
                #code_agent = int(data['code_agent'])
                
                moment=datetime.now()
                receiver_compte=db.session.query(User).filter(User.code_agent==receiver).first()
                receiver_wallet=db.session.query(Wallet).filter(Wallet.user_id==receiver_compte.id).first()
                if emitter_wallet.balance<amount:
                    retour={"code":401,"Title":"Retrait d'argent","contenu":"Echec de retrait, solde insuffisant"}
                    return make_response(jsonify(retour),401)
                else:
                    receiver_wallet.balance=receiver_wallet.balance+amount
                    emitter_wallet.balance=emitter_wallet.balance-amount
                    trans=Transaction(receiver_compte.id,emitter_compte.id,amount,transaction_type_id,moment)
                    db.session.add(receiver_wallet)
                    db.session.add(emitter_wallet)
                    db.session.add(trans)
                    db.session.commit()
                    retour={"code":200,"Title":"Retrait d'argent","contenu":"Retrait effectué avec succès"}
                    return make_response(jsonify(retour),200)
                 
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/delete/transaction' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_Transaction():
    if request.method=='POST':
            
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Transaction).filter(Transaction.id==id).first()
            if user1:
                Transaction.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression d'une Transaction","contenu":"Transaction supprimée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Transaction non trouvée"}
                return make_response(jsonify(retour),401)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/transactions' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getTransaction():
    if request.method=='GET':
            historiques=[]
            historique = Transaction.query.all()
            #user=db.session.query(User).all()

            for u in historique:
                #print(u.nom)
                transactionType=db.session.query(TransactionType).filter(TransactionType.id==u.transaction_type_id).first()
                receiver=db.session.query(User).filter(User.id==u.receiver).first()
                emitter=db.session.query(User).filter(User.id==u.emitter).first()

                historiques.append({"id":u.id,"receiver_id":receiver.id,"emitter_id":emitter.id,"receiver":receiver.firstname+" "+receiver.lastname,"emitter":emitter.firstname+" "+emitter.lastname,"receiver_phone":receiver.phone,"emitter_phone":emitter.phone,"transaction_type":transactionType.type,"amount":u.amount,"date":u.created_at})


            retour={"code":200,"title":"Liste des Transactions","contenu":historiques,"taille":len(historiques)}
            #print(users[0])
            return make_response(jsonify(retour),200)
    


@app.route('/transactionById' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getTransactionById():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            u=db.session.query(Transaction).filter(Transaction.id==id).first()
            transactionType=db.session.query(TransactionType).filter(TransactionType.id==u.transaction_type_id).first()
            receiver=db.session.query(User).filter(User.id==u.receiver).first()
            emitter=db.session.query(User).filter(User.id==u.emitter).first()

            clients.append({"id":u.id,"receiver_id":receiver.id,"emitter_id":emitter.id,"receiver":receiver.firstname+" "+receiver.lastname,"emitter":emitter.firstname+" "+emitter.lastname,"receiver_phone":receiver.phone,"emitter_phone":emitter.phone,"transaction_type":transactionType.type,"amount":u.amount,"date":u.created_at})


    
                #print(u.nom)


            retour={"code":200,"title":"Transaction "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
    


@app.route('/transaction/emitter' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getTransactionEmitter():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            user=int(data['user'])

            client=db.session.query(Transaction).filter(Transaction.emitter==user)
            

            for u in client:
                #print(u.nom)
                transactionType=db.session.query(TransactionType).filter(TransactionType.id==u.transaction_type_id).first()
                receiver=db.session.query(User).filter(User.id==u.receiver).first()
                emitter=db.session.query(User).filter(User.id==u.emitter).first()

                clients.append({"id":u.id,"receiver_id":receiver.id,"emitter_id":emitter.id,"receiver":receiver.firstname+" "+receiver.lastname,"emitter":emitter.firstname+" "+emitter.lastname,"receiver_phone":receiver.phone,"emitter_phone":emitter.phone,"transaction_type":transactionType.type,"amount":u.amount,"date":u.created_at})


            retour={"code":200,"title":"Transaction du user "+str(user),"contenu":clients,"taille":len(clients)}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
    


@app.route('/transaction/receiver' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def getTransactionReceiver():
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            user=int(data['user'])

            client=db.session.query(Transaction).filter(Transaction.receiver==user)
            

            for u in client:
                #print(u.nom)
                transactionType=db.session.query(TransactionType).filter(TransactionType.id==u.transaction_type_id).first()
                receiver=db.session.query(User).filter(User.id==u.receiver).first()
                emitter=db.session.query(User).filter(User.id==u.emitter).first()

                clients.append({"id":u.id,"receiver_id":receiver.id,"emitter_id":emitter.id,"receiver":receiver.firstname+" "+receiver.lastname,"emitter":emitter.firstname+" "+emitter.lastname,"receiver_phone":receiver.phone,"emitter_phone":emitter.phone,"transaction_type":transactionType.type,"amount":u.amount,"date":u.created_at})


            retour={"code":200,"title":"Transaction du user "+str(user),"contenu":clients,"taille":len(clients)}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
    

@app.route('/delete/transaction' ,methods=['GET','POST'])
@auth.login_required
@cross_origin(origin='*')
def delete_transaction():
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Transaction).filter(Transaction.id==id).first()
            
            if user1:
                Transaction.query.filter_by(id=id).delete()
                db.session.commit()
               
                

                retour={"code":200,"title":"Suppression d'une transaction","contenu":"Transaction supprimée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Transaction non trouvée"}
                return make_response(jsonify(retour),401)


