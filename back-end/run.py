import os
import sys
import uuid
import json
import zipfile
from flask import Flask, request, abort, jsonify, send_from_directory, render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
import models, resources
from concurrent.futures import ThreadPoolExecutor
from time import sleep



app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(resources.Currencies, '/api/currencies')
api.add_resource(resources.Companies, '/api/companies')
api.add_resource(resources.Products, '/api/products')
api.add_resource(resources.Trades, '/api/trades')
api.add_resource(resources.Reports, '/api/reports')
api.add_resource(resources.Rules, '/api/rules')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_cs261_2.0.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

executor = ThreadPoolExecutor(1)

@app.route('/jobs')
def run_jobs():
    executor.submit(resources.run_cron_job)
    return 'Job was launched in background!'

@app.route('/')
def index():
    return jsonify({'message':'Welcome to Deustche Bank'})

if __name__=="__main__":
    app.run(debug=True,port=8002,host = '0.0.0.0')

