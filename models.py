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
    def update_company(cls, companycode, name):
        row = cls.query.filter_by(CompanyCode = companycode).first()
        row.CompanyName = name
        db.session.commit()
    @classmethod
    def update_company(cls, companycode, datefounded):
        row = cls.query.filter_by(CompanyCode = companycode).first()
        row.DateFounded = datefounded
        db.session.commit()
    @classmethod
    def update_company(cls, companycode, code):
        row = cls.query.filter_by(CompanyCode = companycode).first()
        row.CompanyCode = code
        db.session.commit()
    @classmethod
    def update_company(cls, companycode, name, code):
        row = cls.query.filter_by(CompanyCode = companycode).first()
        row.CompanyName = name
        row.CompanyCode = code
        db.session.commit()
    @classmethod
    def update_company(cls, companycode, name, datefounded):
        row = cls.query.filter_by(CompanyCode = companycode).first()
        row.CompanyName = name
        row.DateFounded = datefounded
        db.session.commit()
    @classmethod
    def update_company(cls, companycode, datefounded, code):
        row = cls.query.filter_by(CompanyCode = companycode).first()
        row.DateFounded = datefounded
        row.CompanyCode = code
        db.session.commit()
    @classmethod
    def update_company(cls, companycode, name, datefounded, code):
        row = cls.query.filter_by(CompanyCode = companycode).first()
        row.CompanyName = name
        row.DateFounded = datefounded
        row.CompanyCode = code
        db.session.commit()

class CurrencyModel(db.Model):
    __tablename__ = 'CurrencyValues'
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
    BuyingParty = db.Column(db.String(120), nullable = False)
    SellingParty = db.Column(db.String(120), nullable = False)
    NotionalAmount = db.Column(db.Float, nullable = False)
    Quantity = db.Column(db.Integer, nullable = False)
    NotionalCurrency = db.Column(db.String(120), ForeignKey("CurrencyValues.CurrencyCode"), nullable = False)
    MaturityDate = db.Column(db.String(120), nullable = False)
    UnderlyingPrice = db.Column(db.Float, nullable = False)
    UnderlyingCurrency = db.Column(db.String(120), ForeignKey("CurrencyValues.CurrencyCode"), nullable = False)
    StrikePrice = db.Column(db.Float, nullable = False)
    LastUserID = db.Column(db.Integer, nullable = False)
    DateLastModified = db.Column(db.String(120), nullable = False)

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
    CompanyCode = db.Column(db.String(120), primary_key = True,  nullable = False)
    ProductID = db.Column(db.Integer, primary_key = True,  nullable = False)
    
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

class StockPricesModel(db.Model):
    __tablename__ = 'StockPrices'
    StockID = db.Column(db.Integer, primary_key = True, nullable = False)
    DateOfValuation = db.Column(db.String(120), primary_key = True, nullable = False)
    StockPrice = db.Column(db.Numeric(10), nullable = False)
    CompanyCode = db.Column(db.String(120), ForeignKey("Companies.CompanyCode"), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class StockTradesModel(db.Model):
    __tablename__ = 'StockTrades'
    StockID = db.Column(db.Integer, primary_key = True, nullable = False)
    TradeID = db.Column(db.String(120), primary_key = True, nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()