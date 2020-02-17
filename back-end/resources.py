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
                results = models.CurrencyValuationsModel.retrieve_currency(date)
                message = {'noOfMatches' : len(results)}
                return message, 201
            else:
                result = models.CurrencyValuationsModel.retrieve_currency(date)
                i = 1
                res = {}
                for row in result:
                    dicto = {}
                    dicto['code'] = row.CurrencyCode
                    # brokem until all currencies added
                    # dicto['symbol'] = returnCurrencySymbol(row.CurrencyCode)
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
            date = request.args.get('date')
            isDryRun = request.args.get('isDryRun')
            if isDryRun == "true":
                results = models.CompanyModel.retrieve_companies_before(date)
                message = {'noOfMatches' : results.count()}
                return message, 201
            else:
                date = request.args.get('date')
                result = models.CompanyModel.retrieve_companies_before(date)
                i = 1
                res = {}
                for row in result:
                    dicto = {}
                    dicto['id'] = row.CompanyCode
                    dicto['name'] = row.CompanyName
                    dicto['dateEnteredIntoSystem'] = row.DateEnteredInSystem
                    # dicto['dateFounded'] = row.DateFounded
                    # dicto['userIDcreatedBy'] = row.UserIDCreatedBy
                    res[i] = dicto
                    i+=1
                return res, 201
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message':'error occurred'}, 202

    def post(self):
        try:
            json_data = request.data
            data = json.loads(json_data)
            code = str(uuid.uuid4())
            name = data['companyname']
            user_ID = 1 # placeholder
            # dateFounded = data['dateFounded']
            date_entered = models.formatDate(datetime.now())
            new_company = models.CompanyModel(code, name, date_entered) # should have more parameters, user_ID and date_entered
            new_company.save_to_db()
            userAction = "User has inserted a new record in the Companies table with the ID: " + code
            new_event = models.EventLogModel(userAction, date_entered, user_ID)
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
            company_ID = request.args.get('id')
            json_data = request.data
            data = json.loads(json_data)
            name = data['name']
            date_founded = data['dateFounded']
            user_ID = 1 # placeholder
            models.CompanyModel.update_company(company_ID, name, date_founded)
            userAction = "User has updated a record in the Companies table with the ID: " + company_ID
            date_now = models.formatDate(datetime.now())
            new_event = models.EventLogModel(userAction, date_now, user_ID)
            new_event.save_to_db()
            return "success", 200
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500

    def delete(self):
        try:
            company_ID = request.args.get('id')
            models.CompanyModel.delete_company(company_ID)
            user_ID = 1 # placeholder
            userAction = "User has deleted a record in the Companies table with the ID: " + company_ID
            date_now = models.formatDate(datetime.now())
            new_event = models.EventLogModel(userAction, date_now, user_ID)
            new_event.save_to_db()
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
                message = {"noOfMatches" : len(result)}
                return message, 201
            else:
                result = models.ProductModel.retrieve_products_on_date(date)
                i = 1
                res = {}
                for row in result:
                    dicto = {}
                    dicto['id'] = row.ProductID
                    dicto['name'] = row.ProductName
                    dicto['companyID'] = row.CompanyCode
                    dicto['valueInUSD'] = str(row.ProductPrice)
                    # dicto['dateEnteredIntoSystem'] = row.DateEnteredInSystem
                    # dicto['userIDcreatedBy'] = row.UserIDCreatedBy
                    res[i] = dicto
                    i += 1
                return res, 201
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'error occurred'}, 202

    def post(self):
        try:
            # get the name, value, and company ID from request
            json_data = request.data
            data = json.loads(json_data)
            name = data['name']
            value = data['valueInUSD']
            companyCode = data['companyID']
            # then create the date now
            date_now = models.formatDate(datetime.now())
            # add to product table, date_now used as dateEnteredIntoSystem
            new_product = models.ProductModel(name, date_now)
            new_productID = new_product.save_to_db()
            # add to the product seller table
            new_product_seller = models.ProductSellersModel(new_productID, companyCode)
            new_product_seller.save_to_db()
            # add to the product valuation table, date_used as DateOfValuation
            new_product_valuation = models.ProductValuationsModel(new_productID, value, date_now)
            new_product_valuation.save_to_db()
            # log the action
            userAction = "User has inserted a new record in the Products table with the ID: " + str(new_productID)
            user_ID = 1 # placeholder
            new_event = models.EventLogModel(userAction, date_now, user_ID)
            new_event.save_to_db()
            return {'message': 'product has been added'}, 201
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'error occured'}, 202
        except exc.InterfaceError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'error occured'}, 202

    def patch(self):
        try:
            product_ID = request.args.get('id')
            json_data = request.data
            data = json.loads(json_data)
            name = data['name']
            value_in_USD = data['valueInUSD']
            company_ID = data['companyID']
            user_ID = 1 # placeholder
            date_now = models.formatDate(datetime.now())
            models.ProductModel.update_product(product_ID, name)
            models.ProductModel.update_product_sellers(product_ID, company_ID)
            models.ProductModel.update_product_valuations(product_ID, value_in_USD, date_now)
            userAction = "User has updated a record in the Products table with the ID: " + product_ID
            new_event = models.EventLogModel(userAction, date_now, user_ID)
            new_event.save_to_db()
            userAction = "User has updated a record in the ProductSellers table with the ID: " + product_ID
            new_event = models.EventLogModel(userAction, date_now, user_ID)
            new_event.save_to_db()
            userAction = "User has updated a record in the ProductValuations table with the ID: " + product_ID
            new_event = models.EventLogModel(userAction, date_now, user_ID)
            new_event.save_to_db()
            return "success", 200
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500

    def delete(self):
        try:
            product_ID = request.args.get('id')
            models.ProductModel.delete_product(product_ID)
            user_ID = 1 # placeholder
            userAction = "User has deleted a record in the Products table with the ID: " + product_ID
            date_now = models.formatDate(datetime.now())
            new_event = models.EventLogModel(userAction, date_now, user_ID)
            new_event.save_to_db()
            return "success", 200
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500

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

            # TODO add dateModified filter
            # TODO all these loops assumes filter[param] is a list, which may not be true if the input is malformed

            if 'dateCreated' in filter:
                results.append(models.DerivativeTradesModel.get_trades_between(filter['dateCreated'][0], filter['dateCreated'][1]))

            if 'tradeID' in filter:

                    id = filter['tradeID']
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
                message = {"noOfMatches" : len(final_results)}
                return message, 201
            else:
                i = 1
                res = []
                for row in final_results:
                    dicto = {}
                    dicto['tradeID'] = row.TradeID
                    dicto['product'] = row.Product
                    dicto['quantity'] = row.Quantity
                    dicto['buyingParty'] = row.BuyingParty
                    dicto['sellingParty'] = row.SellingParty
                    dicto['notionalValue'] = row.NotionalValue
                    dicto['notionalCurrency'] = row.NotionalCurrency
                    dicto['underlyingValue'] = row.UnderlyingValue
                    dicto['underlyingCurrency'] = row.UnderlyingCurrency
                    dicto['strikePrice'] = row.StrikePrice
                    dicto['maturityDate'] = row.MaturityDate
                    # dicto['tradeDate'] = row.TradeDate
                    dicto['userIDcreatedBy'] = row.UserIDCreatedBy
                    # dicto['lastModifiedDate'] = row.LastModifiedDate
                    res.append(dicto)
                    i += 1

                message['matches'] = res
                return message, 201
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500

    def post(self):
        try:
            json_data = request.data
            data = json.loads(json_data)
            id = str(uuid.uuid4())
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
            DateOfTrade = models.dateFormat(datetime.now())
            user_ID = 1 # placeholder
            new_trade = models.DerivativeTradesModel(id, DateOfTrade, product, buyingParty, sellingParty, notionalValue, quantity, notionalCurrency, maturityDate, underlyingValue, underlyingCurrency, strikePrice, user_ID)

            #make a query to check if the product exists
            result = models.ProductSellersModel.getProductID(product, sellingParty)
            if len(result) == 0:
                print("Product does not exist")
                return {'message' : 'product not found'}, 404

            # need to implement checking if the currencies exist

            #If a the product or stock which the trade is linked to is found, then the trade
            new_tradeID = new_trade.save_to_db()
            assetIDs = [value for value, in result] #results returns a result set object - need to format this // formatted into a list to get the product id // there should only be 1 product id
            new_product_trade = models.ProductTradesModel(new_tradeID, assetIDs[0])
            new_product_trade.save_to_db()

            #Logging the user action
            userAction = "User has inserted a new record in the Trades table with the ID: " + str(new_tradeID)
            dateOfEvent = models.dateFormat(datetime.now())
            new_event = models.EventLogModel(userAction, dateOfEvent, user_ID)
            new_event.save_to_db()
            return {'message': 'trade has been added'}, 201
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500
        except exc.InterfaceError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500

    def patch(self):

        try:
            trade_ID = request.args.get('id')
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

            #Logging the user action
            userAction = "User has updated a record in the Trades table with the ID: " + trade_ID
            dateOfEvent = models.dateFormat(datetime.now())
            user_ID = 1 # placeholder
            new_event = models.EventLogModel(userAction, dateOfEvent, user_ID)
            new_event.save_to_db()

            return "success", 200

        except exc.IntegrityError:
            return {'message': "error occurred"}, 201

    def delete(self):
        try:
            trade_ID = request.args.get('id')
            models.DerivativeTradesModel.delete_product(trade_ID)
            user_ID = 1 # placeholder
            userAction = "User has deleted a record in the Trades table with the ID: " + trade_ID
            date_now = models.formatDate(datetime.now())
            new_event = models.EventLogModel(userAction, date_now, user_ID)
            new_event.save_to_db()
            return "success", 200
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500


class Reports(Resource):

    def get(self):
        # delete below?

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
