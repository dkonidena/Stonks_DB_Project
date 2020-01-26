from run import db
from datetime import datetime
from sqlalchemy import ForeignKey

# expecting in YYYY-MM-DD HH:MM:SS
def dateTruncate(dateString):
    return datetime(int(dateString[0:4]), int(dateString[5:7]), int(dateString[8:10]), int(dateString[11:13]), int(dateString[14:16]), int(dateString[17:19]))


class CompanyModel(db.Model):
    __tablename__ = 'Companies'
    CompanyCode = db.Column(db.String(120), primary_key = True, nullable = False)
    CompanyName = db.Column(db.String(120), nullable = False)
    DateFounded = db.Column(db.String(120))
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def retrieve_companies_before(cls, date):
        return cls.query.filter(CompanyModel.DateFounded <= dateTruncate(date))
    
    @classmethod
    def update_company(cls, companycode, name, datefounded):
        row = cls.query.filter_by(CompanyCode = companycode).first()
        row.CompanyName = name
        row.DateFounded = datefounded
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
    ValueInUSD = db.Column(db.Numeric(10), nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def retrieve_currency_values(cls, date):
        return cls.query.filter_by(DateOfValuation = dateTruncate(date))

class DerivativeTradesModel(db.Model):
    __tablename__ = 'DerivativeTrades'
    TradeID = db.Column(db.String(120), primary_key = True, nullable = False)
    DateOfTrade = db.Column(db.String(120), nullable = False)
    AssetType = db.Column(db.String(120), nullable = False)
    BuyingParty = db.Column(db.String(120), ForeignKey("Companies.CompanyCode"), nullable = False)
    SellingParty = db.Column(db.String(120), ForeignKey("Companies.CompanyCode"), nullable = False)
    NotionalValue = db.Column(db.Float, nullable = False)
    Quantity = db.Column(db.Integer, nullable = False)
    NotionalCurrency = db.Column(db.String(120), ForeignKey("CurrencyValues.CurrencyCode"), nullable = False)
    MaturityDate = db.Column(db.String(120), nullable = False)
    UnderlyingValue = db.Column(db.Float, nullable = False)
    UnderlyingCurrency = db.Column(db.String(120), ForeignKey("CurrencyValues.CurrencyCode"), nullable = False)
    StrikePrice = db.Column(db.Float, nullable = False)
    # LastUserID = db.Column(db.Integer, nullable = False)
    # DateLastModified = db.Column(db.String(120), nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class EventLogModel(db.Model):
    __tablename__ = 'EventLog'
    EventID = db.Column(db.Integer, primary_key = True, nullable = False)
    UserAction = db.Column(db.String(120), nullable = False)
    DateOfEvent = db.Column(db.String(120), nullable = False)
    EmployeeID = db.Column(db.String(120), ForeignKey("Employees.EmployeeID"), nullable = False)
    # Password = db.Column(db.String(120), nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

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

class ProductPricesModel(db.Model):
    __tablename__ = 'ProductPrices'
    ProductID = db.Column(db.Integer, primary_key = True, nullable = False)
    DateOfValuation = db.Column(db.String(120), primary_key = True,  nullable = False)
    MarketPrice = db.Column(db.Float, nullable = False)

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
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class ProductValuationsModel(db.Model):
    __tablename__ = 'ProductValuations'
    ProductID = db.Column(db.Integer, primary_key = True, nullable = False)
    ProductPrice = db.Column(db.Float, nullable = False)
    DateOfValuation = db.Column(db.String(120), primary_key = True, nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class StockValuationsModel(db.Model):
    __tablename__ = 'StockValuations'
    StockID = db.Column(db.Integer, primary_key = True, nullable = False)
    DateOfValuation = db.Column(db.String(120), primary_key = True, nullable = False)
    StockPrice = db.Column(db.Numeric(10), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class StocksModel(db.Model):
    __tablename__ = 'Stocks'
    StockID = db.Column(db.Integer, primary_key = True, nullable = False)
    CompanyID = db.Column(db.Integer, ForeignKey("Companies.CompanyCode"), nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class StockTradesModel(db.Model):
    __tablename__ = 'StockTrades'
    StockID = db.Column(db.Integer, primary_key = True, nullable = False)
    TradeID = db.Column(db.String(120), ForeignKey("Companies.CompanyCode"), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
