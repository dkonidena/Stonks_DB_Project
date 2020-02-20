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
                                results.append(models.DerivativeTradesModel.get_trades_after(filter['dateModified']['after']))
                            else:
                                results.append(models.DerivativeTradesModel.get_trades_before(filter['dateModified']['before']))
                        else:  
                            results.append(models.DerivativeTradesModel.get_trades_between(filter['dateModified']['after'], filter['dateModified']['before']))

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
        test_data = {
            "matches" : [{
                    "date": "2020-02-18T00:28:38.365Z",
                    "content": """dateOfTrade,tradeID,product,buyingParty,sellingParty,notionalAmount,notionalCurrency,quantity,maturityDate,underlyingPrice,underlyingCurrency,strikePrice
01/04/2010 00:00,ACCKXNIA50698568,Scope Lens,AWYB85,UACN81,18120.0,USD,800,07/04/2011,22.65,USD,20.89
01/04/2010 00:00,TFVNUIEV14019758,Stocks,IJPI82,BBAX06,3733800.0,USD,70000,10/07/2013,53.34,USD,57.62
01/04/2010 00:38,SFKFEMNI33385795,Stocks,AMRO66,TGZI54,203496.08,KWD,100,31/01/2012,279.47,USD,2173.46
01/04/2010 00:39,NFPPXKJO32502934,Premium Nanotech,EDYH00,DREA89,920080.0,USD,4000,31/10/2011,230.02,USD,197.94
01/04/2010 00:39,WLLMPGMU67753060,Stocks,NQJL85,BDBU00,563545.77,KZT,900,28/07/2012,158.88,USD,632.4
01/04/2010 00:40,VQYITYKX67468667,Black Materia Orbs,EWUY52,VCSF07,492600.0,USD,60000,02/04/2013,8.21,USD,8.72
01/04/2010 00:40,MVWWGUEO36009262,Stocks,TBVE46,QLMY86,13120100.0,USD,70000,14/04/2011,187.43,USD,205.65"""
                },
                {
                    "date": "2020-02-17T00:28:38.365Z",
                    "content": """dateOfTrade,tradeID,product,buyingParty,sellingParty,notionalAmount,notionalCurrency,quantity,maturityDate,underlyingPrice,underlyingCurrency,strikePrice
01/04/2010 00:12,XNTJSSWX82102942,Stocks,KKGY69,SFZS08,14978600.0,USD,70000,19/06/2013,213.98,USD,236.56
01/04/2010 00:12,SRAKJKES56980699,Stocks,BBJG05,KKZA87,74360.0,USD,2000,05/04/2014,37.18,USD,42.13
01/04/2010 00:16,SHUUQNAF89208519,Stocks,KUWI70,IIZF28,47470.0,USD,500,19/09/2011,94.94,USD,82.87
01/04/2010 00:16,OXXDOFBX41047829,Stocks,SUOX82,FAWI50,19980111.75,HRK,700,27/05/2011,260.54,USD,25251.2
01/04/2010 00:16,LWAKBSFC76100584,Stocks,CMZC67,LBKT00,5691.0,USD,700,05/03/2011,8.13,USD,8.58
01/04/2010 00:17,NAFWJEQM83465255,Muscle Bands,GZED20,EDYH00,2813580.0,USD,9000,26/07/2012,312.62,USD,341.29
01/04/2010 00:17,MNPRZYBF65527748,Stocks,HFLM11,YLGZ72,5832000.0,USD,80000,11/11/2011,72.9,USD,64.03"""
                }
            ]
        }

        #return test_data, 200
        
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
                # find the dates trades are made between these dates
                tradeDates = models.DerivativeTradesModel.get_trade_dates_between(filter['dateCreated'][0], filter['dateCreated'][1])
                for each in tradeDates:
                    results.append(models.DerivativeTradesModel.get_trades_between(each.DateOfTrade, each.DateOfTrade))
                noOfMatches = len(results) # gives the no. of reports available
            else:
                tradeDates = models.DerivativeTradesModel.get_all_trade_dates()
                for each in tradeDates:
                    results.append(models.DerivativeTradesModel.get_trades_between(each.DateOfTrade, each.DateOfTrade))
                noOfMatches = len(results)

            if isDryRun == 'true':
                return {'noOfMatches' : noOfMatches}
            elif isDryRun == 'false':
                message = {'matches' : []}
                i = 0
                while i < len(results):
                    report = {'date': None, 'content': None}
                    content = """Date Of Trade,Trade ID,Product,Buying Party,Selling Party,Notional Value,Notional Currency,Quantity,MaturityDate,Underlying Value,Underlying Currency,Strike Price\n"""
                    for row in results[i]:
                        content += str(row.DateOfTrade) + "," + str(row.TradeID) + "," + str(row.ProductID) + "," + str(row.BuyingParty) + "," + str(row.SellingParty) + "," + str(row.NotionalValue) + "," + str(row.NotionalCurrency) + "," + str(row.Quantity) + "," + str(row.MaturityDate) + "," + str(row.UnderlyingValue) + "," + str(row.UnderlyingCurrency) + "," + str(row.StrikePrice) + "\n"                        
                    report['date'] = tradeDates[i].DateOfTrade
                    report['content'] = content
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
