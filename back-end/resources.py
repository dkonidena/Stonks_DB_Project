from flask_restful import Resource, reqparse
import models
from flask import request
import json
import uuid
import random
from datetime import datetime
import traceback
from sqlalchemy import exc
import sys

# use models.date... instead of redefining date methods in here

def returnCurrencySymbol(currencyCode):
    currencyDict = {"USD": "$", "GBP": "£", "RWF": "RF"}
    return currencyDict[currencyCode]


class Currencies(Resource):

    def get(self):
        try:
            date = request.args.get('date')
            isDryRun = request.args.get('isDryRun')
            if isDryRun == "true":
                #fetch the no. of values in the currencies table with the date argument
                results = models.CurrencyValuationsModel.retrieve_currency(date)
                message = {'noOfMatches' : len(results)}
                i = 1
                res = {}
                for row in results:
                    dicto = {}
                    dicto['currencycode'] = row.CurrencyCode
                    # dictionary need to be written
                    # need to be transformed into a object
                    symbol = returnCurrencySymbol(row.CurrencyCode)
                    dicto['symbol'] = symbol
                    dicto['allowDecimal'] = True
                    dicto['valueInUSD'] = str(row.ValueInUSD)
                    res[i] = dicto
                    i+=1
                message['matches'] = res
                return message, 201
            else:
                result = models.CurrencyValuationsModel.retrieve_currency(date)
                # print(result)
                i = 1
                res = {}
                for row in result:
                    dicto = {}
                    dicto['currencycode'] = row.CurrencyCode
                    # dictionary need to be written
                    # need to be transformed into a object
                    dicto['symbol'] = returnCurrencySymbol(row.currencyCode)
                    dicto['allowDecimal'] = True
                    dicto['valueInUSD'] = str(row.ValueInUSD)
                    res[i] = dicto
                    i+=1
                return res, 200
        except exc.IntegrityError:
            return {'message': "An error has occured pertaining to Integrity issues. Please re-enter the parameters"}, 500


class Companies(Resource):

    def get(self):
        try:
            currentDate = request.args.get('date')
            result = models.CompanyModel.retrieve_companies_before(currentDate)
            i = 1
            res = {}
            for row in result:
                dicto = {}
                dicto['companycode'] = row.CompanyCode
                dicto['companyname'] = row.CompanyName
                res[i] = dicto
                i+=1
            return res, 201
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message':'error occurred'}, 202

    def post(self):
        try:
            # data = request.form.to_dict()
            json_data = request.data
            data = json.loads(json_data)
            code = str(uuid.uuid4())
            name = data['companyname']
            date = data['date']
            dateO = models.formatDate(date)
            new_company = models.CompanyModel(code, name, dateO)
            new_company.save_to_db()
            #Logging the user action
            userAction = "User has inserted a new record in the Companies table with the code: " + code
            dateOfEvent = datetime.now()
            employeeid = 1 #placeholder for now
            new_event = models.EventLogModel(userAction, dateOfEvent, employeeid)
            new_event.save_to_db()
            return {'message': 'Company has been added'}, 201
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500
        except exc.InterfaceError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Interface Error occurred, please re-try entering the parameters'}, 500

    def patch(self):
        try:
            companyid = request.args.get('id')
            json_data = request.data
            data = json.loads(json_data)
            name = data['name']
            datefounded = data['dateFounded']
            models.CompanyModel.update_company(companyid, name, datefounded)
            return "success", 200
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500

    def delete(self):
        companyid = request.args.get('id')
        try:
            models.CompanyModel.delete_company(companyid)
            return "success", 200
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500


class Products(Resource):

    def get(self):
        try:
            date =  request.args.get('date')
            isDryRun = request.args.get('isDryRun')
            if isDryRun == "true":
                result = models.ProductModel.retrieve_products_on_date(date)
                message = {"noOfMatches" : result.count()}
                i = 1
                res = {}
                for row in result:
                    dicto = {}
                    dicto['productid'] = row.ProductID
                    dicto['productName'] = row.ProductName
                    dicto['companycode'] = row.CompanyCode
                    dicto['value'] = str(row.ProductPrice)
                    res[i] = dicto
                    i += 1
                message['matches'] = res
                return message, 201
            else:
                result = models.ProductModel.retrieve_products_on_date(date)
                i = 1
                res = {}
                for row in result:
                    dicto = {}
                    dicto['productid'] = row.ProductID
                    dicto['productName'] = row.ProductName
                    dicto['companycode'] = row.CompanyCode
                    dicto['value'] = str(row.ProductPrice)
                    res[i] = dicto
                    i += 1
                return res, 201
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'error occurred'}, 202

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
            new_product = models.ProductModel(name, dateEnteredInSystem)
            new_productID = new_product.save_to_db()
            #Adds the new product seller
            new_product_seller = models.ProductSellersModel(new_productID, companyCode)
            new_product_seller.save_to_db()
            #Adds the new product valuation
            date = datetime.now()
            new_product_valuation = models.ProductValuationsModel(new_productID, value, date)
            new_product_valuation.save_to_db()
            #Logging the user action
            userAction = "User has inserted a new record in the Products table with the code: " + str(new_productID)
            dateOfEvent = datetime.now()
            employeeid = 1 #placeholder for testing
            new_event = models.EventLogModel(userAction, dateOfEvent, employeeid)
            new_event.save_to_db()
            return {'message': 'product has been added'}, 201
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'error occured'}, 202
        except exc.InterfaceError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'error occured'}, 202
        return 1
    def patch(self):
        return 1
    def delete(self):
        return 1

class Trades(Resource):

    def get(self):
        try:
            try:
                filter = json.loads(request.args.get('filter'))
            except json.JSONDecodeError:
                return {'message': 'malformed filter'}, 400

            # this needs error checking
            isDryRun = request.args.get('isDryRun')

            results = list() # stores results for each query/filter that is applied by the user
            if 'dateCreated' in filter:
                results.append(models.DerivativeTradesModel.get_trades_between(filter['dateCreated'][0], filter['dateCreated'][1]))

            # TODO add dateModified filter
            # TODO all these loops assumes filter[param] is a list, which may not be true if the input is malformed

            if 'tradeID' in filter:
                for id in filter['tradeID']:
                    results.append(models.DerivativeTradesModel.get_trade_with_ID(id))

            if 'buyingParty' in filter:
                for id in filter['buyingParty']:
                    results.append(models.DerivativeTradesModel.get_trades_bought_by(id))

            if 'sellingParty' in filter:
                for id in filter['sellingParty']:
                    results.append(models.DerivativeTradesModel.get_trades_sold_by(id))

            if 'product' in filter:
                for id in filter['product']:
                    results.append(models.DerivativeTradesModel.get_trade_by_product(id))

            if 'notionalCurrency' in filter:
                for id in filter['notionalCurrency']:
                    results.append(models.DerivativeTradesModel.get_trades_by_notional_currency(id))

            if 'underlyingCurrency' in filter:
                for id in filter['underlyingCurrency']:
                    results.append(models.DerivativeTradesModel.get_trade_by_underlying_currency(id))

            if 'userIDcreatedBy' in filter:
                for id in filter['userIDcreatedBy']:
                    results.append(models.DerivativeTradesModel.get_trades_by_user(id))

            #performs intersections on each result set from each query to find the filtered results
            final_results = None
            for each in results:
                if final_results is None:
                    final_results = each
                else:
                    final_results = final_results.intersect(each)

            message = {}
            if isDryRun == "true":
                message['noOfMatches'] = final_results.count()

            i = 1
            res = {}
            for row in final_results:
                dicto = {}
                dicto['product'] = row.Product
                dicto['quantity'] = row.Quantity
                dicto['buyingparty'] = row.BuyingParty
                dicto['sellingparty'] = row.SellingParty
                dicto['notionalvalue'] = row.NotionalValue
                dicto['notionalcurrency'] = row.NotionalCurrency
                dicto['underlyingvalue'] = row.UnderlyingValue
                dicto['underlyingcurrency'] = row.UnderlyingCurrency
                dicto['maturitydate'] = row.MaturityDate
                dicto['strikeprice'] = row.StrikePrice
                dicto['useridcreatedby'] = row.UserIDCreatedBy
                res[i] = dicto
                i += 1

            message['matches'] = res
            return message, 201
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500

    def post(self):
        try:
            # data = request.form.to_dict()
            json_data = request.data
            data = json.loads(json_data)
            id = str(uuid.uuid4())
            # tradeObject = data['tradeObject']
            product = data['product']
            quantity = data['quantity']
            buyingParty = data['buyingParty']
            sellingParty = data['sellingParty']
            notionalValue = data['notionalValue']
            notionalCurrency = data['notionalCurrency']
            underlyingValue = data['underlyingValue']
            underlyingCurrency = data['underlyingCurrency']
            strikePrice = data['strikePrice']
            maturityDate = data['maturityDate']
            DateOfTrade = datetime.now()
            userIDcreatedBy = data['useridcreatedby']
            new_trade = models.DerivativeTradesModel(id, DateOfTrade, product, buyingParty, sellingParty, notionalValue, quantity, notionalCurrency, maturityDate, underlyingValue, underlyingCurrency, strikePrice, userIDcreatedBy)

            #make a query to check if the product exists
            result = models.ProductSellersModel.getProductID(product, sellingParty)
            if result.count() == 0:
                print("Product does not exist")
                return {'message' : 'not found'}, 404
            #If a the product or stock which the trade is linked to is found, then the trade
            new_tradeID = new_trade.save_to_db()
            assetIDs = [value for value, in result] #results returns a result set object - need to format this // formatted into a list to get the product id // there should only be 1 product id
            new_product_trade = models.ProductTradesModel(new_tradeID, assetIDs[0])
            new_product_trade.save_to_db()

            #Logging the user action
            userAction = "User has inserted a new record in the Trades table with the code: " + str(new_tradeID)
            dateOfEvent = datetime.now()
            employeeid = 1 #placeholder
            new_event = models.EventLogModel(userAction, dateOfEvent, employeeid)
            new_event.save_to_db()

            #Check if the added
            return {'message': 'trade has been added'}, 201
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500
        except exc.InterfaceError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500

    def patch(self):

        try:
            tradeID = request.args.get('id')

            json_data = request.data

            data = json.loads(json_data)


            product = data['product']
            quantity = data['quantity']
            buyingParty = data['buyingParty']
            sellingParty = data['sellingParty']
            notionalValue = data['notionalValue']
            notionalCurrency = data['notionalCurrency']
            underlyingValue = data['underlyingValue']
            underlyingCurrency = data['underlyingCurrency']
            maturityDate = data['maturityDate']
            strikePrice = data['strikePrice']

            models.DerivativeTradesModel.update_trade(tradeID, product, buyingParty, sellingParty, notionalValue, notionalCurrency, quantity, maturityDate, underlyingValue, underlyingCurrency, strikePrice)
            return "success", 200
        except exc.IntegrityError:
            return {'message': "error occurred"}, 201

    def delete(self):
        return 1


class Reports(Resource):
    def get(self):
        try:
            dateCreated = request.args.getlist('date')
            tradeID = request.args.get('tradeid')
            buyingParty = request.args.get('buyingparty')
            sellingParty = request.args.get('sellingparty')
            product = request.args.get('product')
            notionalCurrency = request.args.get('notionalcurrency')
            underlyingCurrency = request.args.get('underlyingcurrency')
            userIDcreatedBy = request.args.get('useridcreatedby')
            isDryRun = request.args.get('isDryRun')

            results = list() #stores results for each query/filter that is applied by the user
            if len(dateCreated) > 0:
                results.append(models.DerivativeTradesModel.get_trades_between(dateCreated[0], dateCreated[1]))

            if tradeID is not None:
                results.append(models.DerivativeTradesModel.get_trade_with_id(tradeID))

            if buyingParty is not None:
                results.append(models.DerivativeTradesModel.get_trades_bought_by(buyingParty))

            if sellingParty is not None:
                results.append(models.DerivativeTradesModel.get_trades_sold_by(sellingParty))

            if product is not None:
                results.append(models.DerivativeTradesModel.get_trade_by_product(product))

            if notionalCurrency is not None:
                results.append(models.DerivativeTradesModel.get_trades_by_notional_currency(notionalCurrency))

            if underlyingCurrency is not None:
                results.append(models.DerivativeTradesModel.get_trade_by_underlying_currency(underlyingCurrency))

            if userIDcreatedBy is not None:
                results.append(models.DerivativeTradesModel.get_trades_by_user(userIDcreatedBy))

            return {'message' : 'need to finish'}, 201
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occured'}, 202


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
