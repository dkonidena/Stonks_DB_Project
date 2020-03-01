from flask_restful import Resource, reqparse
import models
from flask import request
import json
import uuid
import random
import traceback
import base64
import tempfile
import os
from sqlalchemy import exc
import sys
from datetime import date as date_func
from random import choice
from string import ascii_uppercase
import ML.main as ml
from ML.tradeObj import trade
import ML.cron
import schedule

#for PDF report generation
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak, Table, TableStyle

# use models.date... instead of redefining date methods in here

# class Machine(Resource):
def returnCurrencySymbol(currencyCode):
    currencyDict = {"USD": "$", "GBP": "£", "RWF": "RF", "AFN": "؋", "XOF" : "CFA", "INR" : "₹", "IDR":"Rp", "JPY":"¥", "QAR":"ر.ق"}
    return currencyDict[currencyCode]

def get_trade_objects():
    trades = models.DerivativeTradesModel.get_trades_all()
    trade_object_list = []
    for t in trades:
        trade0 = trade(t.OriginalNotionalValue, t.NotionalValue, t.OriginalQuantity, t.Quantity)
        trade_object_list.append(trade0)
    return trade_object_list

def run_cron_job():
    all_trades = get_trade_objects()
    ML.cron.job(all_trades, 7, 100)

# run this in seperate thread?
# or if we just have a call at the start of the program, then we can show that
# the machine learning algorithm learns from previous trades by running the
# program, adding a bunch of trades with the same mistake, and then closing
# and reloading the program and adding a trade with the same error
# this trade should be flagged by the algorithm

# schedule.every().day.at("16:00").do(run_cron_job)

# while True:
#     schedule.run_pending()
#     time.sleep(86400)

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
            userID = request.headers.get('userID')
            if models.EmployeesModel.retrieve_by_user_id(userID) == None:
                return {'message':'user not present'}, 401
            json_data = request.data
            data = json.loads(json_data)
            code = ''.join(choice(ascii_uppercase) for i in range(12))
            name = data['name']
            if len(name) == 0:
                return {'message':'company name is empty'}, 400
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
            userID = request.headers.get('userID')
            if models.EmployeesModel.retrieve_by_user_id(userID) == None:
                return {'message':'user not present'}, 401
            company_ID = request.args.get('id')
            json_data = request.data
            data = json.loads(json_data)
            name = data['name']
            if len(name) == 0:
                return {'message':'company name is empty'}, 400
            models.CompanyModel.update_company(company_ID, name)
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
            userID = request.headers.get('userID')
            if models.EmployeesModel.retrieve_by_user_id(userID) == None:
                return {'message':'user not present'}, 401
            company_ID = request.args.get('id')
            date_now = str(date_func.today())
            # check to see if the company exists today
            # return the tuple of the company wanting to be deleted
            specificCompany = models.CompanyModel.retrieve_company_by_code(company_ID)
            # returns tuples of companies that exist currently
            existingCompanies = models.CompanyModel.retrieve_companies_before(date_now)
            # intersection to see if the desired company exists or not
            deletedCompany = existingCompanies.intersect(specificCompany)
            if deletedCompany.count() == 0:
                return {'message':'Cannot delete a non-existant company'}, 400
            if 'id' not in request.args:
                return {'message': 'Request malformed'}, 400
            models.CompanyModel.update_date_deleted(company_ID, date_now)
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
            userID = request.headers.get('userID')
            if models.EmployeesModel.retrieve_by_user_id(userID) == None:
                return {'message':'user not present'}, 401
            # get the name, value, and company ID from request
            json_data = request.data
            data = json.loads(json_data)
            name = data['name']
            value = data['valueInUSD']
            companyCode = data['companyID']
            if len(name) == 0:
                return {'message':'product name is empty'}, 400
            if len(value) == 0:
                return {'message':'product value is empty'}, 400
            if len(companyCode) == 0:
                return {'message':'company code is empty'}, 400
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
            userID = request.headers.get('userID')
            if models.EmployeesModel.retrieve_by_user_id(userID) == None:
                return {'message':'user not present'}, 401
            product_ID = request.args.get('id')
            json_data = request.data
            data = json.loads(json_data)
            name = data['name']
            value_in_USD = data['valueInUSD']
            company_ID = data['companyID']
            if len(name) == 0:
                return {'message':'product name is empty'}, 400
            if len(value) == 0:
                return {'message':'product value is empty'}, 400
            if len(companyCode) == 0:
                return {'message':'company code is empty'}, 400
            date_now = str(date_func.today())
            models.ProductModel.update_product(product_ID, name)
            models.ProductSellersModel.update_product_sellers(product_ID, company_ID)
            models.ProductValuationsModel.update_product_valuations(product_ID, value_in_USD, date_now)
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
            userID = request.headers.get('userID')
            if models.EmployeesModel.retrieve_by_user_id(userID) == None:
                return {'message':'user not present'}, 401
            product_ID = request.args.get('id')
            if 'id' not in request.args:
                return {'message': 'Request malformed'}, 400
            date_now = str(date_func.today())
            models.ProductModel.update_date_deleted(product_ID, date_now) # instead of deletion, the dateDeleted attribute is updated
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
                        if len(filter['dateCreated']) == 1:
                            if 'after' in filter['dateCreated']:
                                results.append(models.DerivativeTradesModel.get_trades_after(filter['dateCreated']['after']))
                            else:
                                results.append(models.DerivativeTradesModel.get_trades_before(filter['dateCreated']['before']))
                        else:
                            results.append(models.DerivativeTradesModel.get_trades_between(filter['dateCreated']['after'], filter['dateCreated']['before']))
                    if 'dateModified' in filter:
                        if len(filter['dateModified']) == 1:
                            if 'after' in filter['dateModified']:
                                results.append(models.DerivativeTradesModel.get_trades_modified_after(filter['dateModified']['after']))
                            else:
                                results.append(models.DerivativeTradesModel.get_trades_modified_before(filter['dateModified']['before']))
                        else:
                            results.append(models.DerivativeTradesModel.get_trades_modified_between(filter['dateModified']['after'], filter['dateModified']['before']))

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
            userID = request.headers.get('userID')
            if models.EmployeesModel.retrieve_by_user_id(userID) == None:
                return {'message':'user not present'}, 401
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
            if len(product) == 0:
                return {'message':'product name is empty'}, 400
            if len(quantity) == 0:
                return {'message':'product value is empty'}, 400
            if len(buyingParty) == 0:
                return {'message':'buying party is empty'}, 400
            if len(sellingParty) == 0:
                return {'message':'selling party is empty'}, 400
            if len(notionalValue) == 0:
                return {'message':'notionalValue is empty'}, 400
            if len(notionalCurrency) == 0:
                return {'message':'notionalCurrency is empty'}, 400
            if len(underlyingValue) == 0:
                return {'message':'underlyingValue is empty'}, 400
            if len(underlyingCurrency) == 0:
                return {'message':'underlyingCurrency is empty'}, 400
            if len(strikePrice) == 0:
                return {'message':'strikePrice is empty'}, 400
            if len(maturityDate) == 0:
                return {'message':'maturityDate is empty'}, 400
            date_now = str(date_func.today())

            #make a query to check if the product exists
            result = models.ProductSellersModel.getProductID(product, sellingParty)
            if len(result) == 0:
                print("Product does not exist")
                return {'message' : 'product not found'}, 404
            new_trade = models.DerivativeTradesModel(TradeID = id, DateOfTrade = date_now, ProductID = result[0].ProductID, BuyingParty = buyingParty, SellingParty = sellingParty, OriginalNotionalValue = notionalValue, NotionalValue = notionalValue, OriginalQuantity = quantity, Quantity = quantity, NotionalCurrency = notionalCurrency, MaturityDate = models.parse_iso_date(maturityDate), UnderlyingValue = underlyingValue, UnderlyingCurrency = underlyingCurrency, StrikePrice = strikePrice, LastModifiedDate = date_now, UserIDCreatedBy = userID)


            # need to implement checking if the currencies exist

            #If a the product or stock which the trade is linked to is found, then the trade
            new_trade = models.DerivativeTradesModel(TradeID = id, DateOfTrade = date_now, ProductID = result[0].ProductID, BuyingParty = buyingParty, SellingParty = sellingParty, OriginalNotionalValue = notionalValue, NotionalValue = notionalValue, OriginalQuantity = quantity, Quantity = quantity, NotionalCurrency = notionalCurrency, MaturityDate = maturityDate, UnderlyingValue = underlyingValue, UnderlyingCurrency = underlyingCurrency, StrikePrice = strikePrice, UserIDCreatedBy = userID)
            new_tradeID = new_trade.save_to_db()
            new_product_trade = models.ProductTradesModel(TradeID = new_tradeID, ProductID = result[0].ProductID)
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
            userID = request.headers.get('userID')
            if models.EmployeesModel.retrieve_by_user_id(userID) == None:
                return {'message':'user not present'}, 401
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
            if len(product) == 0:
                return {'message':'product name is empty'}, 400
            if len(quantity) == 0:
                return {'message':'product value is empty'}, 400
            if len(buyingParty) == 0:
                return {'message':'buying party is empty'}, 400
            if len(sellingParty) == 0:
                return {'message':'selling party is empty'}, 400
            if len(notionalValue) == 0:
                return {'message':'notionalValue is empty'}, 400
            if len(notionalCurrency) == 0:
                return {'message':'notionalCurrency is empty'}, 400
            if len(underlyingValue) == 0:
                return {'message':'underlyingValue is empty'}, 400
            if len(underlyingCurrency) == 0:
                return {'message':'underlyingCurrency is empty'}, 400
            if len(strikePrice) == 0:
                return {'message':'strikePrice is empty'}, 400
            if len(maturityDate) == 0:
                return {'message':'maturityDate is empty'}, 400
            models.DerivativeTradesModel.update_trade(trade_ID, product, buyingParty, sellingParty, notionalValue, notionalCurrency, quantity, maturityDate, underlyingValue, underlyingCurrency, strikePrice)
            result = models.ProductSellersModel.getProductID(product, sellingParty)
            if len(result) == 0:
                print("Product does not exist")
                return {'message' : 'product not found'}, 404
            #Logging the user action
            userAction = "User has updated a record in the Trades table with the ID: " + trade_ID
            dateOfEvent = str(date_func.today())
            new_event = models.EventLogModel(EventDescription = userAction, DateOfEvent = dateOfEvent, Table = "Trades", TypeOfAction = "Update", ReferenceID = trade_ID, EmployeeID = userID)
            new_event.save_to_db()

            return "success", 200

        except exc.IntegrityError:
            return {'message': "error occurred"}, 500

    def delete(self):
        try:
            userID = request.headers.get('userID')
            if models.EmployeesModel.retrieve_by_user_id(userID) == None:
                return {'message':'user not present'}, 401
            trade_ID = request.args.get('id')
            if 'id' not in request.args:
                return {'message': 'Request malformed'}, 400
            models.DerivativeTradesModel.delete_product(trade_ID)
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
            try:
                filter = json.loads(request.args.get('filter'))
            except json.JSONDecodeError:
                return {'message': 'malformed filter'}, 400

            # this needs error checking
            isDryRun = request.args.get('isDryRun')

            # TODO add dateModified filter
            # TODO all these loops assumes filter[param] is a list, which may not be true if the input is malformed

            results = list()

            # either dateCreated will be passed or nothing will be passed
            if 'dateCreated' in filter:
                if len(filter['dateCreated']) == 1:
                    if 'after' in filter['dateCreated']:
                        tradeDates = models.DerivativeTradesModel.get_trade_dates_after(filter['dateCreated']['after'])
                    else:
                        tradeDates = models.DerivativeTradesModel.get_trade_dates_before(filter['dateCreated']['before'])
                elif len(filter['dateCreated']) == 2:
                    tradeDates = models.DerivativeTradesModel.get_trade_dates_between(filter['dateCreated']['after'], filter['dateCreated']['before'])
                else:
                    tradeDates = models.DerivativeTradesModel.get_all_trade_dates()
            else:
                tradeDates = models.DerivativeTradesModel.get_all_trade_dates()

            for each in tradeDates:
                result = models.DerivativeTradesModel.get_trades_between(each.DateOfTrade, each.DateOfTrade)
                results.append(result)
            noOfMatches = len(results)

            # contents for the pdf file
            story = [] # all relevant data for the pdf
            styles = getSampleStyleSheet() # defining the styles/text style for the trades table in the pdf
            styleB = styles['BodyText']
            styleB.fontSize = 8
            styleB.wordWrap = 'CJK' # adding text wrapping for the table cells in the pdf

            if isDryRun == 'true':
                return {'noOfMatches' : noOfMatches}
            elif isDryRun == 'false':
                message = {'matches' : []}
                i = 0
                while i < len(results):
                    handle, fn = tempfile.mkstemp(suffix='.csv')
                    with os.fdopen(handle, "w", encoding='utf8', newline='') as f:
                        report = {'date': None, 'content': None}
                        # data that will be contained in the pdf table
                        tableData = [['Date Of Trade', 'Trade ID', 'Product', 'Buying Party', 'Selling Party', 'Notional Value', 'Notional Currency', 'Quantity', 'Maturity Date', 'Underlying Value', Paragraph('Underlying Currency', styleB), 'Strike Price']]
                        content = """Date Of Trade,Trade ID,Product,Buying Party,Selling Party,Notional Value,Notional Currency,Quantity,Maturity Date,Underlying Value,Underlying Currency,Strike Price\n"""
                        for row in results[i]:
                            # adding rows to the pdf table
                            tableData.append([str(row.DateOfTrade), Paragraph(str(row.TradeID), styleB), str(row.ProductID), str(row.BuyingParty), str(row.SellingParty), str(row.NotionalValue), str(row.NotionalCurrency), str(row.Quantity), str(row.MaturityDate), str(row.UnderlyingValue), str(row.UnderlyingCurrency), str(row.StrikePrice)])
                            content += str(row.DateOfTrade) + "," + str(row.TradeID) + "," + str(row.ProductID) + "," + str(row.BuyingParty) + "," + str(row.SellingParty) + "," + str(row.NotionalValue) + "," + str(row.NotionalCurrency) + "," + str(row.Quantity) + "," + str(row.MaturityDate) + "," + str(row.UnderlyingValue) + "," + str(row.UnderlyingCurrency) + "," + str(row.StrikePrice) + "\n"
                        report['date'] = tradeDates[i].DateOfTrade
                        report['content'] = content
                        # adding the whole table for the single date into its own pdf file
                        story.append(Table(tableData,colWidths=65, rowHeights=30, repeatRows=0, splitByRow=1, style=TableStyle([('FONTSIZE', (0,0), (-1,-1), 8)])))
                        doc = SimpleDocTemplate('output.pdf', pagesize = landscape(A4), title = "Report")
                        doc.build(story)
                        encodedPDF = base64.b64encode(open("output.pdf", "rb").read()).decode()
                        report['pdfFile'] = encodedPDF
                        message['matches'].append(report)
                        i += 1
                return message, 200
            else:
                return {'message' : 'Request Malformed'}, 400

        except ValueError:
            traceback.print_exc(file=sys.stdout)
            return {'message': 'Date invalid'}, 400
        except exc.ProgrammingError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500

class Users(Resource):
    def get(self):
        try:
            isDryRun = request.args['isDryRun']
        except KeyError:
            return {'message': 'isDryRun paramater missing'}, 400

        matches = models.EmployeesModel.retrieve_all()
        noOfMatches = len(matches)

        user_objects = []

        for match in matches:
            user_objects.append({
                "id": str(match.EmployeeID),
                "name": f"{match.FirstName} {match.LastName}"
            })

        if isDryRun == "true":
            return {'noOfMatches' : noOfMatches}, 200
        elif isDryRun == "false":
            return {'matches' : user_objects}, 200
        else:
            return {'message': 'isDryRun must be \'true\' or \'false\''}, 400

class Rules(Resource):
    def get(self):
        return 1
    def post(self):
        return 1
    def patch(self):
        return 1
    def delete(self):
        return 1

class CheckTrade(Resource):
    def post(self):
        # needs error checking
        try:
            userID = request.headers.get('userID')
            if models.EmployeesModel.retrieve_by_user_id(userID) == None:
                return {'message':'user not present'}, 401
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

            #make a query to check if the product exists
            result = models.ProductSellersModel.getProductID(product, sellingParty)
            if len(result) == 0:
                print("Product does not exist")
                return {'message' : 'product not found'}, 404

            # before adding a trade call the machine learning algorithm to suggest corrections
            # first parse the relevant data into a trade object

            input_trade = ML.tradeObj.trade(notionalValue, None, quantity, None)

            returned_trade = ml.suggestChange(input_trade)

            return {
                'product': product,
                'quantity': str(returned_trade.getCurrentQuantity()),
                'buyingParty': buyingParty,
                'sellingParty': sellingParty,
                'notionalPrice': str(returned_trade.getCurrentNotional()),
                'notionalCurrency': notionalCurrency,
                'underlyingPrice': underlyingValue,
                'underlyingCurrency': underlyingCurrency,
                'strikePrice': strikePrice,
                'maturityDate': maturityDate,
                'tradeID': id,
                'tradeDate': date_now,
                'userIDcreatedBy': userID
                }, 200

        except exc.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500
        except exc.InterfaceError:
            traceback.print_exc(file=sys.stdout)
            return {'message' : 'error occurred'}, 500
