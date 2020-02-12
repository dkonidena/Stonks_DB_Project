from run import db
from datetime import datetime
from sqlalchemy import ForeignKey, join, func, or_, Date, cast, exc
import traceback
import sys
# expecting in YYYY-MM-DD HH:MM:SS
def dateTruncate(dateString):
    try:
        return datetime(int(dateString[0:4]), int(dateString[5:7]), int(dateString[8:10]), int(dateString[11:13]), int(dateString[14:16]), int(dateString[17:19])).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError
        print("Formatting of the String has caused an error")
        traceback.print_exc(file=sys.stdout)
    except:
        print("Unknown Error occurred")
        traceback.print_exc(file=sys.stdout)

def returnDatetime(dateString):
    return datetime(int(dateString[0:4]), int(dateString[5:7]), int(dateString[8:10])).strftime("%Y-%m-%d")

def get_date(dateString):
    return (dateString[0:4]) + '-' + (dateString[5:7]) + '-' + (dateString[8:10])


class CompanyModel(db.Model):
    __tablename__ = 'Companies'
    CompanyCode = db.Column(db.String(120), primary_key = True, nullable = False)
    CompanyName = db.Column(db.String(120), nullable = False)
    DateEnteredInSystem = db.Column(db.String(120))

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
            print("The Company couldn't be saved to the Database")
            traceback.print_exc(file=sys.stdout)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)
        except:
            print("Unknown Error occurred")
            traceback.print_exc(file=sys.stdout)
        

    @classmethod
    def retrieve_companies_before(cls, date):
        try:
            return cls.query.filter(func.DATE(CompanyModel.DateEnteredInSystem) <= returnDatetime(date))
        except exc.ProgrammingError:
            raise exc.ProgrammingError("","",1)
            print("The number of parameters passed might not have been correct, please retry")

    @classmethod
    def update_company(cls, companycode, name, datefounded):
        try:
            row = cls.query.filter_by(CompanyCode = companycode).first()
            row.CompanyName = name
            row.DateEnteredInSystem = datefounded
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
    @classmethod
    def delete_company(cls, companycode):
        try:
            cls.query.filter_by(CompanyCode = companycode).delete()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)

class CurrencyTypesModel(db.Model):
    __tablename__ = 'CurrencyTypes'
    CurrencyCode = db.Column(db.String(120), primary_key = True, nullable = False)
    CurrencyName = db.Column(db.String(120), nullable = False)
    Country = db.Column(db.String(120), nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

class CurrencyValuationsModel(db.Model):
    __tablename__ = 'CurrencyValuations'
    CurrencyCode = db.Column(db.String(120), primary_key = True, nullable = False)
    DateOfValuation = db.Column(db.String(120), primary_key = True, nullable = False)
    ValueInUSD = db.Column(db.Float, nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

    @classmethod
    def retrieve_currency(cls, date):
        try:
            print(get_date(date))
            return cls.query.join(CurrencyTypesModel, cls.CurrencyCode == CurrencyTypesModel.CurrencyCode).filter(cls.DateOfValuation.like(get_date(date)+"%")).all()
        except exc.ProgrammingError:
            raise exc.ProgrammingError("","",1)

class DerivativeTradesModel(db.Model):
    __tablename__ = 'DerivativeTrades'
    TradeID = db.Column(db.String(120), primary_key = True, nullable = False)
    DateOfTrade = db.Column(db.String(120), nullable = False)
    Product = db.Column(db.String(120), nullable = False)
    BuyingParty = db.Column(db.String(120), ForeignKey("Companies.CompanyCode"), nullable = False)
    SellingParty = db.Column(db.String(120), ForeignKey("Companies.CompanyCode"), nullable = False)
    NotionalValue = db.Column(db.Float, nullable = False)
    Quantity = db.Column(db.Integer, nullable = False)
    NotionalCurrency = db.Column(db.String(120), ForeignKey("CurrencyTypes.CurrencyCode"), nullable = False)
    MaturityDate = db.Column(db.String(120), nullable = False)
    UnderlyingValue = db.Column(db.Float, nullable = False)
    UnderlyingCurrency = db.Column(db.String(120), ForeignKey("CurrencyTypes.CurrencyCode"), nullable = False)
    StrikePrice = db.Column(db.Float, nullable = False)
    UserIDCreatedBy = db.Column(db.Integer, ForeignKey("Employees.EmployeeID"), nullable = False)
    # LastUserID = db.Column(db.Integer, nullable = False)
    # DateLastModified = db.Column(db.String(120), nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.TradeID
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

    @classmethod
    def get_trades_between(cls, startDate, endDate):
        try:
            return cls.query.filter(func.DATE(DerivativeTradesModel.DateOfTrade) >= returnDatetime(startDate), func.DATE(DerivativeTradesModel.DateOfTrade) <= returnDatetime(endDate))
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)
    @classmethod
    def get_trade_with_ID(cls, tradeID):
        try:
            return cls.query.filter(DerivativeTradesModel.TradeID == tradeID)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    @classmethod
    def get_trades_sold_by(cls, sellingParty):
        try:
            return cls.query.filter(DerivativeTradesModel.SellingParty == sellingParty)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)
    @classmethod
    def get_trades_bought_by(cls, buyingParty):
        try:
            return cls.query.filter(DerivativeTradesModel.BuyingParty == buyingParty)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    @classmethod
    def get_trade_by_product(cls, productName):
        try:
            return cls.query.filter(ProductModel.ProductName == productName, ProductModel.ProductID == ProductTradesModel.ProductID, ProductTradesModel.TradeID == cls.TradeID)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)
    @classmethod
    def get_trades_by_notional_currency(cls, notionalCurrency):
        try:
            return cls.query.filter(DerivativeTradesModel.NotionalCurrency == notionalCurrency)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)
    @classmethod
    def get_trade_by_underlying_currency(cls, underlyingCurrency):
        try:
            return cls.query.filter(DerivativeTradesModel.TradeID == underlyingCurrency)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)
    @classmethod
    def get_trades_by_user(cls, userID):
        try:
            return cls.query.filter(DerivativeTradesModel.UserIDCreatedBy == userID)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)
    @classmethod
    def update_trade(cls, tradeID, product, buyingParty, sellingParty, notionalValue, notionalCurrency, quantity, maturityDate, underlyingValue, underlyingCurrency, strikePrice):
        try:
            row = cls.query.filter_by(TradeID = tradeID).first()
            row.Product = product
            row.BuyingParty = buyingParty
            row.SellingParty = sellingParty
            row.NotionalValue = notionalValue
            row.NotionalCurrency = notionalCurrency
            row.Quantity = quantity
            row.MaturityDate = maturityDate
            row.UnderlyingValue = underlyingValue
            row.UnderlyingCurrency = underlyingCurrency
            row.StrikePrice = strikePrice
            db.session.commit()
        except exc.IntegrityError:
           raise exc.IntegrityError("", "", 1)


class EventLogModel(db.Model):
    __tablename__ = 'EventLog'
    EventID = db.Column(db.Integer, primary_key = True, nullable = False)
    UserAction = db.Column(db.String(120), nullable = False)
    DateOfEvent = db.Column(db.String(120), nullable = False)
    EmployeeID = db.Column(db.String(120), ForeignKey("Employees.EmployeeID"), nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

    @classmethod
    def get_events(cls, date): #gets all the events/actions made by users on a specific date
        try:
            return cls.query.filter(cls.DateOfEvent <= date).with_entities(EventLogModel.DateOfEvent, EventLogModel.UserAction)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)


class EmployeesModel(db.Model):
    __tablename__ = 'Employees'
    EmployeeID = db.Column(db.Integer, primary_key = True, nullable = False)
    FirstName = db.Column(db.String(120), nullable = False)
    LastName = db.Column(db.String(120), nullable = False)
    Email = db.Column(db.String(120), nullable = False)
    # Password = db.Column(db.String(120), nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

class ProductSellersModel(db.Model):
    __tablename__ = 'ProductSellers'
    ProductID = db.Column(db.Integer, primary_key = True,  nullable = False)
    CompanyCode = db.Column(db.String(120), primary_key = True,  nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

    @classmethod
    def getProductID(cls, productName, companyCode):
        try:
            return cls.query.filter(ProductSellersModel.CompanyCode == companyCode).filter(ProductSellersModel.ProductID == ProductModel.ProductID).filter(ProductModel.ProductName == productName).with_entities(ProductSellersModel.ProductID)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

class ProductTradesModel(db.Model):
    __tablename__ = 'ProductTrades'
    TradeID = db.Column(db.String(120), primary_key = True, nullable = False)
    ProductID = db.Column(db.Integer, primary_key = True,  nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

class ProductModel(db.Model):
    __tablename__ = 'Products'
    ProductID = db.Column(db.Integer, primary_key = True, nullable = False)
    ProductName = db.Column(db.String(120), nullable = False)
    DateEnteredInSystem = db.Column(db.String(120))

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.ProductID
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

    @classmethod
    def retrieve_products_on_date(cls, date):
        try:
            return cls.query.filter(cls.ProductID == ProductSellersModel.ProductID, ProductSellersModel.ProductID == ProductValuationsModel.ProductID, func.DATE(cls.DateEnteredInSystem) == returnDatetime(date)).\
            with_entities(ProductModel.ProductID, ProductModel.ProductName, ProductSellersModel.CompanyCode, ProductValuationsModel.ProductPrice)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

class ProductValuationsModel(db.Model):
    __tablename__ = 'ProductValuations'
    ProductID = db.Column(db.Integer, primary_key = True, nullable = False)
    ProductPrice = db.Column(db.Float, nullable = False)
    DateOfValuation = db.Column(db.String(120), primary_key = True, nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)
