#! /usr/bin/env python

import os



from api.endpoints import *
from flask import Flask,request,jsonify,send_file
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import glob
from flask_cors import cross_origin
import hashlib, uuid
import os
from datetime import datetime
from api import app,db


@app.route('/createTable',methods=['GET'])
def create_table():
    db.create_all()
    return "Tables created...."


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
