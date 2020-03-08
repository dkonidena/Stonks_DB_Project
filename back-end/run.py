import os
import sys
import uuid
import json
import zipfile
from flask import Flask, request, abort, jsonify, send_from_directory, render_template, redirect
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
app = Flask(__name__)
import models, resources
from concurrent.futures import ThreadPoolExecutor
from time import sleep

FULL_DATABASE = 'sqlite:///D:\\rohan\\Documents\\CS261 Coursework\\database_cs261_full.db'
PARTIAL_DATABASE = 'sqlite:///database_cs261_2.0/db'


app = Flask(__name__, static_url_path='', static_folder='../front-end')
api = Api(app)
CORS(app)

api.add_resource(resources.Currencies, '/api/currencies')
api.add_resource(resources.Companies, '/api/companies')
api.add_resource(resources.Products, '/api/products')
api.add_resource(resources.Trades, '/api/trades')
api.add_resource(resources.CheckTrade, '/api/check_trade')
api.add_resource(resources.Reports, '/api/reports')
api.add_resource(resources.Rules, '/api/rules')
api.add_resource(resources.Users, '/api/users')
api.add_resource(resources.Events, '/api/events')
api.add_resource(resources.Config, '/api/config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_cs261_2.0.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#executor = ThreadPoolExecutor(1)
#executor.submit(resources.run_cron_job)

@app.route('/')
def index():
    return redirect("/page-home/page-home.html", code=302)

if __name__=="__main__":
    port = 8002
    host = '0.0.0.0'
    print(f"\n\n > Address http://{host}:{port} <\n\n")
    app.run(debug=True,port=port,host=host)
