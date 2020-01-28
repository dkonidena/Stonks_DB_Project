import os
import sys
import uuid
import json
import zipfile
from flask import Flask, request, abort, jsonify, send_from_directory, render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import datetime
import models, resources



app = Flask(__name__)
api = Api(app)

api.add_resource(resources.Currencies, '/api/currencies')
api.add_resource(resources.Companies, '/api/companies')
api.add_resource(resources.Products, '/api/products')
api.add_resource(resources.Trades, '/api/trades')
api.add_resource(resources.Reports, '/api/reports')
api.add_resource(resources.Rules, '/api/rules')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_cs261_2.0.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return jsonify({'message':'Welcome to Deustche Bank'})

if __name__=="__main__":
    app.run(debug=True,port=8002,host = '0.0.0.0')

