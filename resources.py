from flask_restful import Resource, reqparse
import models
from flask import request
import json
import uuid
import random
from datetime import datetime

def dateTruncate(dateString):
    return datetime(int(dateString[0:4]), int(dateString[5:7]), int(dateString[8:10]), int(dateString[11:13]), int(dateString[14:16]), int(dateString[17:19])).strftime("%Y-%m-%d %H:%M:%S.%f")

class Currencies(Resource):
    def get(self):
        # try:
        date = request.args.get('date')
        result = models.CurrencyValuationsModel.retrieve_currency(date = date)
        # print(result)
        i = 1
        res = {}
        for row in result:
            dicto = {}
            dicto['currencycode'] = row.CurrencyCode
            # dictionary need to be written
            # need to be transformed into a object
            dicto['symbol'] = "$"
            dicto['allowDecimal'] = True
            dicto['valueInUSD'] = str(row.ValueInUSD)
            res[i] = dicto
            i+=1
        return res, 200

        # except:
        #     return {'message':'error has occured'}, 201

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
        # data = request.form.to_dict()
        json_data = request.data
        data = json.loads(json_data)
        code = str(uuid.uuid4())
        name = data['companyname']
        date = data['date']
        dateO = dateTruncate(date)
        new_company = models.CompanyModel(CompanyCode = code, CompanyName = name, DateEnteredInSystem = dateO)
        new_company.save_to_db()
        #Logging the user action
        userAction = "User has inserted a new record in the Companies table with the code: " + code
        dateOfEvent = datetime.now()
        employeeid = 1 #placeholder for now
        new_event = models.EventLogModel(UserAction = userAction, DateOfEvent = dateOfEvent, EmployeeID = employeeid)
        new_event.save_to_db()
        return {'message': 'Company has been added'}, 201


    def patch(self):
        try:
            companyid = request.args.get('id')
            json_data = request.data
            data = json.loads(json_data)
            name = data['company'].name
            datefounded = data['company'].dateFounded
            models.CompanyModel.update_company(companycode=companyid, name=name, datefounded=datefounded)
            return "success", 200
        except:
            return "failure", 201

    def delete(self):
        companyid = request.args.get('id')
        try:
            models.CompanyModel.delete_company(companycode=companyid)
            return "success", 200
        except:
            return "failure", 201

class Products(Resource):
    def get(self):
        return request.args.get('date')
    def post(self):
        # data = request.form.to_dict()
        try:
            json_data = request.data
            data = json.loads(json_data)
            name = data['productname']
            value = data['value']
            companyCode = data['companycode']
            dateEnteredInSystem = datetime.now()
            #Adds the new product
            new_product = models.ProductModel(ProductName = name, DateEnteredInSystem = dateEnteredInSystem)
            new_productID = new_product.save_to_db()
            #Adds the new product seller
            new_product_seller = models.ProductSellersModel(ProductID = new_productID, CompanyCode = companyCode)
            new_product_seller.save_to_db()
            #Adds the new product valuation
            date = datetime.now()
            new_product_valuation = models.ProductValuationsModel(ProductID = new_productID, ProductPrice = value, DateOfValuation = date)
            new_product_valuation.save_to_db()
            #Logging the user action
            userAction = "User has inserted a new record in the Products table with the code: " + str(new_productID)
            dateOfEvent = datetime.now()
            employeeid = 1 #placeholder for testing
            new_event = models.EventLogModel(UserAction = userAction, DateOfEvent = dateOfEvent, EmployeeID = employeeid)
            new_event.save_to_db()
            return {'message': 'product has been added'}, 201
        except:
            return {'message': 'error occured'}, 202
        return 1
    def patch(self):
        return 1
    def delete(self):
        return 1

class Trades(Resource):
    def get(self):
        return 1
    def post(self):
        try:
            # data = request.form.to_dict()
            json_data = request.data
            data = json.loads(json_data)
            id = str(uuid.uuid4())
            # tradeObject = data['tradeObject']
            product = data['product']
            assetType = data['assettype']
            assetID = data['assetid'] #require an asset ID for front-end to link the trade to a particular stock or product depending on asset type
            quantity = data['quantity']
            buyingParty = data['buyingParty']
            sellingParty = data['sellingParty']
            notionalPrice = data['notionalPrice']
            notionalCurrency = data['notionalcurrency']
            underlyingPrice = data['underlyingPrice']
            underlyingCurrency = data['underlyingCurrency']
            strikePrice = data['strikePrice']
            maturityDate = data['maturityDate']
            DateOfTrade = datetime.now()
            DateLastModified = datetime.now()
            new_trade = models.DerivativeTradesModel(TradeID= id, 
            DateOfTrade= DateOfTrade, 
            AssetType= assetType,
            BuyingParty= buyingParty, 
            SellingParty= sellingParty,
            NotionalAmount= 0.00,
            NotionalPrice = notionalPrice,
            Quantity= quantity,
            NotionalCurrency = notionalCurrency,
            MaturityDate= maturityDate,
            UnderlyingPrice= underlyingCurrency,
            StrikePrice= strikePrice,
            LastUserID= 0,
            DateLastModified= DateLastModified)

            new_tradeID = new_trade.save_to_db()

            #Adding the trade ID to either StockTrades or ProductTrades depending on the type of the asset
            if AssetType == "Stock":
                new_stock_trade = models.StockTradesModel(TradeID = new_tradeID, StockID = assetID)
                new_stock_trade.save_to_db()
            else:
                new_product_trade = models.StockTradesModel(TradeID = new_tradeID, ProductID = assetID)
                new_product_trade.save_to_db()

            #Logging the user action
            userAction = "User has inserted a new record in the Trades table with the code: " + str(new_tradeID)
            dateOfEvent = datetime.now()
            employeeid = 1 #placeholder
            new_event = models.EventLogModel(UserAction = userAction, DateOfEvent = dateOfEvent, EmployeeID = employeeid)
            new_event.save_to_db()

            #Check if the added 
            return {'message': 'trade has been added'}, 201
        except:
            return {'message': 'error occured'}, 202
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