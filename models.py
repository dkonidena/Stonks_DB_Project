from run import db
from datetime import datetime
from sqlalchemy import ForeignKey, join, func, or_

# expecting in YYYY-MM-DD HH:MM:SS
def dateTruncate(dateString):
    return datetime(int(dateString[0:4]), int(dateString[5:7]), int(dateString[8:10]), int(dateString[11:13]), int(dateString[14:16]), int(dateString[17:19])).strftime("%Y-%m-%d %H:%M:%S")

def get_date(dateString):
    return (dateString[0:4]) + '-' + (dateString[5:7]) + '-' + (dateString[8:10])


class CompanyModel(db.Model):
    __tablename__ = 'Companies'
    CompanyCode = db.Column(db.String(120), primary_key = True, nullable = False)
    CompanyName = db.Column(db.String(120), nullable = False)
    DateEnteredInSystem = db.Column(db.String(120))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def retrieve_companies_before(cls, date):
        return cls.query.filter(CompanyModel.DateEnteredInSystem <= dateTruncate(date))
    
    @classmethod
    def update_company(cls, companycode, name, datefounded):
        row = cls.query.filter_by(CompanyCode = companycode).first()
        row.CompanyName = name
        row.DateEnteredInSystem = datefounded
        db.session.commit()

    @classmethod
    def delete_company(cls, companycode):
        cls.query.filter_by(CompanyCode = companycode).delete()

class CurrencyTypesModel(db.Model):
    __tablename__ = 'CurrencyTypes'
    CurrencyCode = db.Column(db.String(120), primary_key = True, nullable = False)
    CurrencyName = db.Column(db.String(120), nullable = False)
    Country = db.Column(db.String(120), nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class CurrencyValuationsModel(db.Model):
    __tablename__ = 'CurrencyValuations'
    CurrencyCode = db.Column(db.String(120), primary_key = True, nullable = False)
    DateOfValuation = db.Column(db.String(120), primary_key = True, nullable = False)
    ValueInUSD = db.Column(db.Float, nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def retrieve_currency(cls, date):
        print(get_date(date))
        return cls.query.join(CurrencyTypesModel, cls.CurrencyCode == CurrencyTypesModel.CurrencyCode).filter(cls.DateOfValuation.like(get_date(date)+"%")).all()


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
        db.session.add(self)
        db.session.commit()
        return self.TradeID

    @classmethod
    def get_trades_between(cls, startDate, endDate):
        return cls.query.filter(DerivativeTradesModel.DateOfTrade >= startDate, DerivativeTradesModel.DateOfTrade <= endDate)
    
    @classmethod
    def get_trade_with_ID(cls, tradeID):
        return cls.query.filter(DerivativeTradesModel.TradeID == tradeID)
    
    @classmethod
    def get_trades_sold_by(cls, sellingParty):
        return cls.query.filter(DerivativeTradesModel.SellingParty == sellingParty)

    @classmethod
    def get_trades_bought_by(cls, buyingParty):
        return cls.query.filter(DerivativeTradesModel.BuyingParty == buyingParty)

    @classmethod
    def get_trade_by_product(cls, productName):
        return cls.query.filter(ProductModel.ProductName == productName, ProductModel.ProductID == ProductTradesModel.ProductID, ProductTradesModel.TradeID == cls.TradeID)

    @classmethod
    def get_trades_by_notional_currency(cls, notionalCurrency):
        return cls.query.filter(DerivativeTradesModel.NotionalCurrency == notionalCurrency)

    @classmethod
    def get_trade_by_underlying_currency(cls, underlyingCurrency):
        return cls.query.filter(DerivativeTradesModel.TradeID == underlyingCurrency)

    @classmethod
    def get_trades_by_user(cls, userID):
        return cls.query.filter(DerivativeTradesModel.UserIDCreatedBy == userID)

class EventLogModel(db.Model):
    __tablename__ = 'EventLog'
    EventID = db.Column(db.Integer, primary_key = True, nullable = False)
    UserAction = db.Column(db.String(120), nullable = False)
    DateOfEvent = db.Column(db.String(120), nullable = False)
    EmployeeID = db.Column(db.String(120), ForeignKey("Employees.EmployeeID"), nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_events(cls, date): #gets all the events/actions made by users on a specific date
        return cls.query.filter(cls.DateOfEvent <= date).with_entities(EventLogModel.DateOfEvent, EventLogModel.UserAction)

class EmployeesModel(db.Model):
    __tablename__ = 'Employees'
    EmployeeID = db.Column(db.Integer, primary_key = True, nullable = False)
    FirstName = db.Column(db.String(120), nullable = False)
    LastName = db.Column(db.String(120), nullable = False)
    Email = db.Column(db.String(120), nullable = False)
    # Password = db.Column(db.String(120), nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class ProductSellersModel(db.Model):
    __tablename__ = 'ProductSellers'
    ProductID = db.Column(db.Integer, primary_key = True,  nullable = False)
    CompanyCode = db.Column(db.String(120), primary_key = True,  nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getProductID(cls, productName, companyCode):
        print(cls.query.filter(ProductSellersModel.CompanyCode == companyCode).filter(ProductSellersModel.ProductID == ProductModel.ProductID).filter(ProductModel.ProductName == productName).with_entities(ProductSellersModel.ProductID))
        return cls.query.filter(ProductSellersModel.CompanyCode == companyCode).filter(ProductSellersModel.ProductID == ProductModel.ProductID).filter(ProductModel.ProductName == productName).with_entities(ProductSellersModel.ProductID)

class ProductTradesModel(db.Model):
    __tablename__ = 'ProductTrades'
    TradeID = db.Column(db.String(120), primary_key = True, nullable = False)
    ProductID = db.Column(db.Integer, primary_key = True,  nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class ProductModel(db.Model):
    __tablename__ = 'Products'
    ProductID = db.Column(db.Integer, primary_key = True, nullable = False)
    ProductName = db.Column(db.String(120), nullable = False)
    DateEnteredInSystem = db.Column(db.String(120))
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.ProductID
    
    @classmethod
    def retrieve_products_before(cls, date):
        return cls.query.filter(cls.ProductID == ProductSellersModel.ProductID, ProductSellersModel.ProductID == ProductValuationsModel.ProductID, cls.DateEnteredInSystem == date).\
            with_entities(ProductModel.ProductID, ProductModel.ProductName, ProductSellersModel.CompanyCode, ProductValuationsModel.ProductPrice)

class ProductValuationsModel(db.Model):
    __tablename__ = 'ProductValuations'
    ProductID = db.Column(db.Integer, primary_key = True, nullable = False)
    ProductPrice = db.Column(db.Float, nullable = False)
    DateOfValuation = db.Column(db.String(120), primary_key = True, nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
