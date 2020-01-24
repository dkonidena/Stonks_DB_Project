from flask_restful import Resource, reqparse
import models
from flask import request
import json
import uuid
from datetime import datetime

def dateTruncate(dateString):
    return datetime(int(dateString[0:4]), int(dateString[5:7]), int(dateString[8:10]), int(dateString[11:13]), int(dateString[14:16]), int(dateString[17:19]))

class Currencies(Resource):
    def get(self):
        return request.args.get('date')

class Companies(Resource):
    def get(self):
        try:
            currentDate = request.args.get('date')
            result = models.CompanyModel.retrieve_companies_before(date = currentDate)
            i = 1
            res = {}
            for row in result:
                dicto = {}
                dicto['companycode'] = row.CompanyCode
                dicto['companyname'] = row.CompanyName
                res[i] = dicto
                i+=1
            return res, 201
        except:
            return {'message':'error occurred'}, 202
    def post(self):
        try:
            # data = request.form.to_dict()
            json_data = request.data
            data = json.loads(json_data)
            code = str(uuid.uuid4())
            name = data['companyname']
            date = data['date']
            dateO = dateTruncate(date)
            new_company = models.CompanyModel(CompanyCode = code, CompanyName = name, DateFounded = dateO)
            new_company.save_to_db()
            return {'message': 'Company has been added'}, 201
        except:
            return {'message': 'error has occurred'}, 202

    def patch(self):
        return 1
    def delete(self):
        return 1

class Products(Resource):
    def get(self):
        return request.args.get('date')
    def post(self):
        try:
            # data = request.form.to_dict()
            json_data = request.data
            data = json.loads(json_data)
            product = str(uuid.uuid4())
            name = data['productname']
            value = data['value']
            new_product = models.ProductModel(ProductName = name)
            new_product.save_to_db()
            return {'message': 'product has been added'}, 201
        except:
            return {'message': 'error has occurred'}, 202
        return 1
    def patch(self):
        return 1
    def delete(self):
        return 1

class Trades(Resource):
    def get(self):
        return 1
    def post(self):
        return 1
    def patch(self):
        return 1
    def delete(self):
        return 1

class Reports(Resource):
    def get(self):
        return 1

class Rules(Resource):
    def get(self):
        return 1
    def post(self):
        return 1
    def patch(self):
        return 1
    def delete(self):
        return 1

# redundant
class CheckTrade(Resource):
    def post(self):
        return 1