from flask_restful import Resource, reqparse
import models
from flask import request
import json
import uuid
import random
import traceback
from sqlalchemy import exc
import sys
from datetime import date as date_func
from random import choice
from string import ascii_uppercase

# use models.date... instead of redefining date methods in here

def returnCurrencySymbol(currencyCode):
    currencyDict = {"USD": "$", "GBP": "£", "RWF": "RF", "AFN": "؋", "XOF" : "CFA", "INR" : "₹", "IDR":"Rp", "JPY":"¥", "QAR":"ر.ق"}
    return currencyDict[currencyCode]


class Currencies(Resource):

    def get(self):
        message = {}
        try:
            date = request.args.get('date')
            if 'isDryRun' not in request.args:
                return {'message': 'Request malformed'}, 400
            isDryRun = request.args.get('isDryRun')
            if isDryRun == "true":
                results = models.CurrencyValuationsModel.retrieve_currency(date)
                message['noOfMatches'] = len(results)
                return message, 200
            elif isDryRun == "false":
                result = models.CurrencyValuationsModel.retrieve_currency(date)
                i = 1
                res = []
                for row in result:
                    dicto = {}
                    dicto['code'] = row.CurrencyCode
                    # brokem until all currencies added
                    dicto['symbol'] = returnCurrencySymbol(row.CurrencyCode)
                    dicto['allowDecimal'] = True
                    dicto['valueInUSD'] = str(row.ValueInUSD)
                    res.append(dicto)
                message['matches'] = res
                return message, 200
            else:
                return {'message': 'Request malformed'}, 400
        except ValueError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'Date invalid'}, 400
        except exc.IntegrityError:
            return {'message': "An error has occured pertaining to Integrity issues. Please re-enter the parameters"}, 500


class Companies(Resource):

    def get(self):
        message = {}
        try:
            date = request.args.get('date')
            if 'isDryRun' not in request.args:
                return {'message': 'Request malformed'}, 400
            isDryRun = request.args.get('isDryRun')
            if isDryRun == "true":
                if date is None:
                    results = models.CompanyModel.retrieve_all_companies()
                    noOfMatches = len(results)
                else:
                    results = models.CompanyModel.retrieve_companies_before(date)
                    noOfMatches = results.count()
                message['noOfMatches'] = noOfMatches
                return message, 200
            elif isDryRun == "false":
                # check if the date parameter is passed
                if date is None:
                    # if not, return all companies
                    result = models.CompanyModel.retrieve_all_companies()
                else:
                    # if so, return all companies that existed on or before the date
                    result = models.CompanyModel.retrieve_companies_before(date)
                i = 1
                res = []
                for row in result:
                    dicto = {}
                    dicto['id'] = row.CompanyCode
                    dicto['name'] = row.CompanyName
                    dicto['dateEnteredIntoSystem'] = row.DateEnteredInSystem
                    # dicto['userIDcreatedBy'] = row.UserIDCreatedBy
                    res.append(dicto)
                message['matches'] = res
                return message, 200
            else:
                return {'message': 'Request malformed'}, 400
        except ValueError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'Date invalid'}, 400
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message':'error occurred'}, 500

    def post(self):
        # needs error checking
        try:
            json_data = request.data
            data = json.loads(json_data)
            code = ''.join(choice(ascii_uppercase) for i in range(12))
            name = data['name']
            userID = 1 # placeholder
            date_entered = str(date_func.today())
            new_company = models.CompanyModel(CompanyCode = code, CompanyName = name, DateEnteredInSystem = date_entered, UserIDCreatedBy = userID) # should have more parameters, user_ID
            new_company.save_to_db()
            eventDescription = "User has inserted a new record in the Companies table with the ID: " + code
            new_event = models.EventLogModel(EventDescription = eventDescription, DateOfEvent = date_entered, Table = "Companies", TypeOfAction = "Insert", ReferenceID = code, EmployeeID = userID)
            new_event.save_to_db()
            return {'message': 'Company has been added'}, 201
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500
        except exc.InterfaceError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Interface Error occurred, please re-try entering the parameters'}, 500

    def patch(self):
        # needs error checking
        try:
            company_ID = request.args.get('id')
            json_data = request.data
            data = json.loads(json_data)
            name = data['name']
            dateEnteredIntoSystem = data['dateEnteredIntoSystem']
            userID = 1 # placeholder
            models.CompanyModel.update_company(company_ID, name, dateEnteredIntoSystem)
            userAction = "User has updated a record in the Companies table with the ID: " + company_ID
            date_now = str(date_func.today())
            new_event = models.EventLogModel(EventDescription = userAction, DateOfEvent = date_now, Table = "Companies", TypeOfAction = "Update", ReferenceID = company_ID, EmployeeID = userID)
            new_event.save_to_db()
            return "success", 200
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500

    def delete(self):
        try:
            company_ID = request.args.get('id')
            if 'id' not in request.args:
                return {'message': 'Request malformed'}, 400
            date_now = str(date_func.today())
            models.CompanyModel.update_date_deleted(company_ID, date_now)
            user_ID = 1 # placeholder
            userAction = "User has deleted a record in the Companies table with the ID: " + company_ID
            new_event = models.EventLogModel(EventDescription = userAction, DateOfEvent = date_now, Table = "Companies", TypeOfAction = "Deletion", ReferenceID = company_ID, EmployeeID = user_ID)
            new_event.save_to_db()
            return "success", 200
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500


class Products(Resource):

    def get(self):
        message = {}
        try:
            date = request.args.get('date')
            if date is None:
                # TODO return all products when the date is not specifed, as per API spec
                isDryRun = request.args.get('isDryRun')
                if 'isDryRun' not in request.args:
                    return {'message': 'Request malformed'}, 400
                if isDryRun == "true":
                    # need error handling to deal with ValueError raised
                    result = models.ProductModel.retrieve_products()
                    message = {"noOfMatches" : result.count()}
                    return message, 201
                elif isDryRun == "false":
                    result = models.ProductModel.retrieve_products()
                    i = 1
                    res = []
                    for row in result:
                        dicto = {}
                        dicto['id'] = str(row.ProductID)
                        dicto['name'] = row.ProductName
                        dicto['companyID'] = row.CompanyCode
                        dicto['valueInUSD'] = str(row.ProductPrice)
                        dicto['dateEnteredIntoSystem'] = row.DateEnteredInSystem
                        # dicto['userIDcreatedBy'] = row.UserIDCreatedBy
                        res.append(dicto)
                    message['matches'] = res
                    return message, 201
                else:
                    return {'message': 'Request malformed'}, 400
            else:
                isDryRun = request.args.get('isDryRun')
                if 'isDryRun' not in request.args:
                    return {'message': 'Request malformed'}, 400
                if isDryRun == "true":
                    # need error handling to deal with ValueError raised
                    result = models.ProductModel.retrieve_products_on_date(date)
                    message = {"noOfMatches" : result.count()}
                    return message, 201
                elif isDryRun == "false":
                    result = models.ProductModel.retrieve_products_on_date(date)
                    i = 1
                    res = []
                    for row in result:
                        dicto = {}
                        dicto['id'] = str(row.ProductID)
                        dicto['name'] = row.ProductName
                        dicto['companyID'] = row.CompanyCode
                        dicto['valueInUSD'] = str(row.ProductPrice)
                        dicto['dateEnteredIntoSystem'] = row.DateEnteredInSystem
                        # dicto['userIDcreatedBy'] = row.UserIDCreatedBy
                        res.append(dicto)
                    message['matches'] = res
                    return message, 201
                else:
                    return {'message': 'Request malformed'}, 400
        except ValueError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'Date invalid'}, 400
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'error occurred'}, 500

    def post(self):
        # needs error checking
        try:
            # get the name, value, and company ID from request
            json_data = request.data
            data = json.loads(json_data)
            name = data['name']
            value = data['valueInUSD']
            companyCode = data['companyID']
            userID = 1 # placeholder
            # then create the date now
            date_now = str(date_func.today())
            # add to product table, date_now used as dateEnteredIntoSystem
            new_product = models.ProductModel(ProductName = name, DateEnteredInSystem = date_now, UserIDCreatedBy = userID)
            new_productID = new_product.save_to_db()
            # add to the product seller table
            new_product_seller = models.ProductSellersModel(ProductID = new_productID, CompanyCode = companyCode)
            new_product_seller.save_to_db()
            # add to the product valuation table, date_used as DateOfValuation
            new_product_valuation = models.ProductValuationsModel(ProductID = new_productID, ProductPrice = value, DateOfValuation = date_now)
            new_product_valuation.save_to_db()
            # log the action
            userAction = "User has inserted a new record in the Products table with the ID: " + str(new_productID)
            new_event = models.EventLogModel(EventDescription = userAction, DateOfEvent = date_now, Table = "Products", TypeOfAction = "Insert", ReferenceID = new_productID, EmployeeID = userID)
            new_event.save_to_db()
            return {'message': 'product has been added'}, 201
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'error occured'}, 500
        except exc.InterfaceError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'error occured'}, 500

    def patch(self):
        # needs error checking
        try:
            product_ID = request.args.get('id')
            json_data = request.data
            data = json.loads(json_data)
            name = data['name']
            value_in_USD = data['valueInUSD']
            company_ID = data['companyID']
            user_ID = 1 # placeholder
            date_now = str(date_func.today())
            models.ProductModel.update_product(product_ID, name)
            models.ProductModel.update_product_sellers(product_ID, company_ID)
            models.ProductModel.update_product_valuations(product_ID, value_in_USD, date_now)
            userAction = "User has updated a record in the Products table with the ID: " + product_ID
            new_event = models.EventLogModel(EventDescription = userAction, DateOfEvent = date_now, Table = "Products", TypeOfAction = "Update", ReferenceID = product_ID, EmployeeID = user_ID)
            new_event.save_to_db()
            userAction = "A product update has cascaded to the ProductSellers table with the ID: " + product_ID
            new_event = models.EventLogModel(EventDescription = userAction, DateOfEvent = date_now, Table = "ProductSellers", TypeOfAction = "Update", ReferenceID = product_ID, EmployeeID = user_ID)
            new_event.save_to_db()
            userAction = "A product update has cascaded to the ProductValuations table with the ID: " + product_ID
            new_event = models.EventLogModel(EventDescription = userAction, DateOfEvent = date_now, Table = "ProductValuations", TypeOfAction = "Update", ReferenceID = product_ID, EmployeeID = user_ID)
            new_event.save_to_db()
            return "success", 200
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500

    def delete(self):
        try:
            product_ID = request.args.get('id')
            if 'id' not in request.args:
                return {'message': 'Request malformed'}, 400
            date_now = str(date_func.today())
            models.ProductModel.update_date_deleted(product_ID, date_now) # instead of deletion, the dateDeleted attribute is updated
            user_ID = 1 # placeholder
            userAction = "User has deleted a record in the Products table with the ID: " + product_ID
            new_event = models.EventLogModel(EventDescription = userAction, DateOfEvent = date_now, Table = "Products", TypeOfAction = "Deletion", ReferenceID = product_ID, EmployeeID = user_ID)
            new_event.save_to_db()
            return "success", 200
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500

class Trades(Resource):

    def get(self):
        try:
            try:
                if 'filter' not in request.args:
                    return {'message': 'malformed filter'}, 400
                filter = json.loads(request.args.get('filter'))
            except json.JSONDecodeError:
                return {'message': 'malformed filter'}, 400

            if 'isDryRun' not in request.args:
                return {'message': 'malformed filter'}, 400
            isDryRun = request.args.get('isDryRun')

            results = list() # stores results for each query/filter that is applied by the user

            # TODO add dateModified filter
            # TODO all these loops assumes filter[param] is a list, which may not be true if the input is malformed

            # if the filter is empty then return all the trades
            if filter == {}:
                results.append(models.DerivativeTradesModel.get_trades_all())
            else:
                try:
                    if 'dateCreated' in filter:
                        # if str(filter['dateCreated'][1]) == "0000-12-31T00:01:15.000Z":
                        #     results.append(models.DerivativeTradesModel.get_trades_between(filter['dateCreated'][0]))
                        # elif if str(filter['dateCreated'][1]) == null end date:
                        #     results.append(models.DerivativeTradesModel.get_trades_between(filter['dateCreated'][1]))
                        # else:
                        results.append(models.DerivativeTradesModel.get_trades_between(filter['dateCreated'][0], filter['dateCreated'][1]))

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
                except:
                    return {'message': 'malformed filter'}, 400

            #performs intersections on each result set from each query to find the filtered results
            final_results = None

            for each in results:
                if final_results is None:
                    final_results = each
                else:
                    final_results = final_results.intersect(each)

            if isDryRun == "true":
                if filter == {}:
                    noOfMatches = len(final_results)
                else:
                    noOfMatches = final_results.count()
                message = {"noOfMatches" : noOfMatches}
                return message, 200
            elif isDryRun == "false":
                i = 1
                res = []
                for row in final_results:
                    dicto = {}
                    dicto['tradeID'] = row.TradeID
                    dicto['product'] = str(row.ProductID)
                    dicto['quantity'] = row.Quantity
                    dicto['buyingParty'] = row.BuyingParty
                    dicto['sellingParty'] = row.SellingParty
                    dicto['notionalPrice'] = row.NotionalValue
                    dicto['notionalCurrency'] = row.NotionalCurrency
                    dicto['underlyingPrice'] = row.UnderlyingValue
                    dicto['underlyingCurrency'] = row.UnderlyingCurrency
                    dicto['strikePrice'] = str(row.StrikePrice)
                    dicto['maturityDate'] = row.MaturityDate
                    dicto['tradeDate'] = row.DateOfTrade
                    dicto['userIDcreatedBy'] = str(row.UserIDCreatedBy)
                    dicto['lastModifiedDate'] = row.DateOfTrade # need to be changed to the event log date
                    res.append(dicto)
                message = {'matches' : res}
                return message, 200
            else:
                return {'message': 'Request malformed'}, 400
        except ValueError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'Date invalid'}, 400
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500

    def post(self):
        # needs error checking
        try:
            json_data = request.data
            data = json.loads(json_data)
            id = ''.join(choice(ascii_uppercase) for i in range(12))
            product = data['product']
            quantity = data['quantity']
            buyingParty = data['buyingParty']
            sellingParty = data['sellingParty']
            notionalValue = data['notionalPrice']
            notionalCurrency = data['notionalCurrency']
            underlyingValue = data['underlyingPrice']
            underlyingCurrency = data['underlyingCurrency']
            strikePrice = data['strikePrice']
            maturityDate = models.parse_iso_date(str(data['maturityDate']))
            date_now = str(date_func.today())
            userID = 1 # placeholder

            #make a query to check if the product exists
            result = models.ProductSellersModel.getProductID(product, sellingParty)
            if result.count() == 0:
                print("Product does not exist")
                return {'message' : 'product not found'}, 404
            assetIDs = [value for value, in result] #results returns a result set object - need to format this // formatted into a list to get the product id // there should only be 1 product id

            new_trade = models.DerivativeTradesModel(TradeID = id, DateOfTrade = date_now, ProductID = assetIDs[0], BuyingParty = buyingParty, SellingParty = sellingParty, OriginalNotionalValue = notionalValue, NotionalValue = notionalValue, OriginalQuantity = quantity, Quantity = quantity, NotionalCurrency = notionalCurrency, MaturityDate = maturityDate, UnderlyingValue = underlyingValue, UnderlyingCurrency = underlyingCurrency, StrikePrice = strikePrice, UserIDCreatedBy = userID)


            # need to implement checking if the currencies exist

            #If a the product or stock which the trade is linked to is found, then the trade
            new_tradeID = new_trade.save_to_db()
            new_product_trade = models.ProductTradesModel(TradeID = new_tradeID, ProductID = assetIDs[0])
            new_product_trade.save_to_db()

            #Logging the user action
            userAction = "User has inserted a new record in the Trades table with the ID: " + str(new_tradeID)
            new_event = models.EventLogModel(EventDescription = userAction, DateOfEvent = date_now, Table = "DerivativeTrades", TypeOfAction = "Insert", ReferenceID = new_tradeID, EmployeeID = userID)
            new_event.save_to_db()
            return {'message': 'trade has been added'}, 201
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500
        except exc.InterfaceError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500

    def patch(self):
        # needs error checking
        try:
            trade_ID = request.args.get('id')
            json_data = request.data
            data = json.loads(json_data)
            product = data['product']
            quantity = data['quantity']
            buyingParty = data['buyingParty']
            sellingParty = data['sellingParty']
            notionalValue = data['notionalPrice']
            notionalCurrency = data['notionalCurrency']
            underlyingValue = data['underlyingPrice']
            underlyingCurrency = data['underlyingCurrency']
            maturityDate = data['maturityDate']
            strikePrice = data['strikePrice']

            models.DerivativeTradesModel.update_trade(trade_ID, product, buyingParty, sellingParty, notionalValue, notionalCurrency, quantity, maturityDate, underlyingValue, underlyingCurrency, strikePrice)

            #Logging the user action
            userAction = "User has updated a record in the Trades table with the ID: " + trade_ID
            dateOfEvent = str(date_func.today())
            userID = 1 # placeholder
            new_event = models.EventLogModel(EventDescription = userAction, DateOfEvent = dateOfEvent, Table = "Trades", TypeOfAction = "Update", ReferenceID = trade_ID, EmployeeID = userID)
            new_event.save_to_db()

            return "success", 200

        except exc.IntegrityError:
            return {'message': "error occurred"}, 500

    def delete(self):
        try:
            trade_ID = request.args.get('id')
            if 'id' not in request.args:
                return {'message': 'Request malformed'}, 400
            models.DerivativeTradesModel.delete_product(trade_ID)
            userID = 1 # placeholder
            userAction = "User has deleted a record in the Trades table with the ID: " + trade_ID
            date_now = str(date_func.today())
            new_event = models.EventLogModel(EventDescription = userAction, DateOfEvent = date_now, Table = "Trades", TypeOfAction = "Deletion", ReferenceID = trade_ID, EmployeeID = userID)
            new_event.save_to_db()
            return "success", 200
        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'Integrity Error occurred, please re-try entering the parameters'}, 500


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

            return {'message' : 'need to finish'}, 200
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occured'}, 500


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
