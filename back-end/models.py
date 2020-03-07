from run import db
from datetime import datetime
from sqlalchemy import ForeignKey, join, func, or_, Date, cast, exc
import traceback
import sys
from datetime import date as date_func

def parse_iso_date(date_string):
    # this function takes an iso8601 string and converts it into a YYYY-MM-DD string
    date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    return date.strftime('%Y-%m-%d')

class CompanyModel(db.Model):
    __tablename__ = 'Companies'
    CompanyCode = db.Column(db.String(120), primary_key = True, nullable = False)
    CompanyName = db.Column(db.String(120), nullable = False)
    DateEnteredInSystem = db.Column(db.String(120), nullable = False)
    DateDeleted = db.Column(db.String(120), nullable = False)
    UserIDCreatedBy = db.Column(db.String(120))

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
            traceback.print_exc(file=sys.stdout)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)
        except:
            print("Unknown Error occurred")

    # gets all companies that existed before a date (serves get?)
    # should this be existed ON that date? something could've existed and closed
    @classmethod
    def retrieve_companies_before(cls, date):
        try:
            return cls.query.filter(func.DATE(CompanyModel.DateEnteredInSystem) <= parse_iso_date(date), or_(parse_iso_date(date) < cls.DateDeleted, cls.DateDeleted == None))
        except exc.ProgrammingError:
            raise exc.ProgrammingError("","",1)

    @classmethod
    def retrieve_company_by_code(cls, code):
        try:
            return cls.query.filter(cls.CompanyCode == code)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("","",1)
    
    @classmethod
    def retrieve_company_by_name(cls, name):
        try:
            return cls.query.filter(cls.CompanyName == name)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("","",1)

    # gets all companies that existed before a date (serves get?)
    # should this be existed ON that date? something could've existed and closed
    @classmethod
    def retrieve_all_companies(cls):
        try:
            return cls.query.all()
        except exc.ProgrammingError:
            raise exc.ProgrammingError("","",1)

    # serves the company patch request
    @classmethod
    def update_company(cls, companycode, name):
        try:
            row = cls.query.filter_by(CompanyCode = companycode).first()
            row.CompanyName = name
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)

    @classmethod
    def update_date_deleted(cls, companycode, date):
        try:
            row = cls.query.filter_by(CompanyCode = companycode).first()
            row.DateDeleted = date
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("", "", 1)

    # serves the comapany delete request
    @classmethod
    def delete_company(cls, companycode):
        try:
            cls.query.filter_by(CompanyCode = companycode).delete()
            db.session.commit()
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
            print("The currency couldn't be saved to the database")
            traceback.print_exc(file=sys.stdout)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)
        except:
            print("Unknown Error occurred")

    @classmethod
    def retrieve_all_currencies(cls):
        return cls.query.all()


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
            print("The currency couldn't be saved to the database")
            traceback.print_exc(file=sys.stdout)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)
        except:
            print("Unknown Error occurred")

    # serves the currecny get
    # gets all valuations on a certain date
    @classmethod
    def retrieve_currency(cls, date):
        try:
            return cls.query.filter(func.DATE(cls.DateOfValuation) <= parse_iso_date(date)).with_entities(cls.CurrencyCode, func.max(cls.DateOfValuation).label('MaxDate'), cls.ValueInUSD).group_by(cls.CurrencyCode)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("","",1)


class DerivativeTradesModel(db.Model):
    __tablename__ = 'DerivativeTrades'
    TradeID = db.Column(db.String(120), primary_key = True, nullable = False)
    DateOfTrade = db.Column(db.String(120), nullable = False)
    ProductID = db.Column(db.Integer, nullable = False)
    BuyingParty = db.Column(db.String(120), ForeignKey("Companies.CompanyCode"), nullable = False)
    SellingParty = db.Column(db.String(120), ForeignKey("Companies.CompanyCode"), nullable = False)
    OriginalNotionalValue = db.Column(db.Float, nullable = False)
    NotionalValue = db.Column(db.Float, nullable = False)
    OriginalQuantity = db.Column(db.Integer, nullable = False)
    Quantity = db.Column(db.Integer, nullable = False)
    NotionalCurrency = db.Column(db.String(120), ForeignKey("CurrencyTypes.CurrencyCode"), nullable = False)
    MaturityDate = db.Column(db.String(120), nullable = False)
    UnderlyingValue = db.Column(db.Float, nullable = False)
    UnderlyingCurrency = db.Column(db.String(120), ForeignKey("CurrencyTypes.CurrencyCode"), nullable = False)
    StrikePrice = db.Column(db.Float, nullable = False)
    LastModifiedDate = db.Column(db.String(120), nullable = False)
    UserIDCreatedBy = db.Column(db.Integer, ForeignKey("Employees.EmployeeID"), nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.TradeID
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

    # serves the get request for a filtered date
    @classmethod
    def get_trades_after(cls, startDate, offset):
        try:
            return cls.query.filter(func.DATE(DerivativeTradesModel.DateOfTrade) >= parse_iso_date(startDate)).offset(offset).limit(1000)
        except exc.ProgrammingError:
            # is there a reason it's "", "" not "",""?
            raise exc.ProgrammingError("", "", 1)
    @classmethod
    def get_trades_before(cls, endDate, offset):
        try:
            return cls.query.filter(func.DATE(DerivativeTradesModel.DateOfTrade) <= parse_iso_date(endDate)).offset(offset).limit(1000)
        except exc.ProgrammingError:
            # is there a reason it's "", "" not "",""?
            raise exc.ProgrammingError("", "", 1)
    @classmethod
    def get_trades_between(cls, startDate, endDate, offset):
        try:
            return cls.query.filter(func.DATE(DerivativeTradesModel.DateOfTrade) >= parse_iso_date(startDate), func.DATE(DerivativeTradesModel.DateOfTrade) <= parse_iso_date(endDate)).offset(offset).limit(1000)
        except exc.ProgrammingError:
            # is there a reason it's "", "" not "",""?
            raise exc.ProgrammingError("", "", 1)

    # serves the get request for a filtered date
    @classmethod
    def get_trades_modified_after(cls, startDate, offset):
        try:
            return cls.query.filter(func.DATE(DerivativeTradesModel.LastModifiedDate) >= parse_iso_date(startDate)).offset(offset).limit(1000)
        except exc.ProgrammingError:
            # is there a reason it's "", "" not "",""?
            raise exc.ProgrammingError("", "", 1)
    @classmethod
    def get_trades_modified_before(cls, endDate, offset):
        try:
            return cls.query.filter(func.DATE(DerivativeTradesModel.LastModifiedDate) <= parse_iso_date(endDate)).offset(offset).limit(1000)
        except exc.ProgrammingError:
            # is there a reason it's "", "" not "",""?
            raise exc.ProgrammingError("", "", 1)
    @classmethod
    def get_trades_modified_between(cls, startDate, endDate, offset):
        try:
            return cls.query.filter(func.DATE(DerivativeTradesModel.LastModifiedDate) >= parse_iso_date(startDate), func.DATE(DerivativeTradesModel.LastModifiedDate) <= parse_iso_date(endDate)).offset(offset).limit(1000)
        except exc.ProgrammingError:
            # is there a reason it's "", "" not "",""?
            raise exc.ProgrammingError("", "", 1)

    # serves the get request for a filtered trade ID
    @classmethod
    def get_trade_with_ID(cls, tradeID, offset):
        try:
            return cls.query.filter(DerivativeTradesModel.TradeID == tradeID).offset(offset).limit(1000)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    # serves the get request for a filtered selling party
    @classmethod
    def get_trades_sold_by(cls, sellingParty, offset):
        try:
            return cls.query.filter(DerivativeTradesModel.SellingParty == sellingParty).offset(offset).limit(1000)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    # serves the get request for a filtered buying party
    @classmethod
    def get_trades_bought_by(cls, buyingParty, offset):
        try:
            return cls.query.filter(DerivativeTradesModel.BuyingParty == buyingParty).offset(offset).limit(1000)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    # serves the get request for a filtered product name
    @classmethod
    def get_trade_by_product(cls, productID, offset):
        try:
            return cls.query.filter(cls.ProductID == productID).offset(offset).limit(1000)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    # serves the get request for a filtered notional currency
    @classmethod
    def get_trades_by_notional_currency(cls, notionalCurrency, offset):
        try:
            return cls.query.filter(DerivativeTradesModel.NotionalCurrency == notionalCurrency).offset(offset).limit(1000)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    # serves the get request for a filtered underlying currency
    @classmethod
    def get_trade_by_underlying_currency(cls, underlyingCurrency, offset):
        try:
            return cls.query.filter(DerivativeTradesModel.TradeID == underlyingCurrency).offset(offset).limit(1000)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    # serves the get request for a filtered user ID
    @classmethod
    def get_trades_by_user(cls, userID, offset):
        try:
            return cls.query.filter(DerivativeTradesModel.UserIDCreatedBy == userID).offset(offset).limit(1000)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)
    @classmethod
    def get_trades_all(cls, offset):
        try:
            return cls.query.offset(offset).limit(1000).all()
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)


    # returns all dates the trades were made on
    @classmethod
    def get_all_trade_dates(cls, offset):
        try:
            return cls.query.distinct(cls.DateOfTrade).group_by(cls.DateOfTrade).offset(offset).limit(1000)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    @classmethod
    def get_trade_dates_after(cls, startDate, offset):
        try:
            return cls.query.filter(parse_iso_date(startDate) <= func.DATE(cls.DateOfTrade)).distinct(cls.DateOfTrade).group_by(cls.DateOfTrade).offset(offset).limit(1000)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)
    
    @classmethod
    def get_trade_dates_before(cls, endDate, offset):
        try:
            return cls.query.filter(parse_iso_date(endDate) >= func.DATE(cls.DateOfTrade)).distinct(cls.DateOfTrade).group_by(cls.DateOfTrade).offset(offset).limit(1000)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    # returns all dates trades happen between a certain start and end date -> used for reports generation
    @classmethod
    def get_trade_dates_between(cls, startDate, endDate, offset):
        try:
            return cls.query.filter(parse_iso_date(startDate) <= func.DATE(cls.DateOfTrade), func.DATE(cls.DateOfTrade) <= parse_iso_date(endDate)).distinct(cls.DateOfTrade).group_by(cls.DateOfTrade).offset(offset).limit(1000)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    @classmethod
    def get_trade_date_by_id(cls, id, offset):
        try:
            return cls.query.filter(cls.TradeID == id).with_entities(cls.DateOfTrade).first()
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    # serves the trade patch request
    @classmethod
    def update_trade(cls, tradeID, product, buyingParty, sellingParty, notionalValue, notionalCurrency, quantity, maturityDate, underlyingValue, underlyingCurrency, strikePrice):
        try:
            row = cls.query.filter_by(TradeID = tradeID).first()
            row.ProductID = product
            row.BuyingParty = buyingParty
            row.SellingParty = sellingParty
            row.NotionalValue = notionalValue
            row.NotionalCurrency = notionalCurrency
            row.Quantity = quantity
            row.MaturityDate = maturityDate
            row.UnderlyingValue = underlyingValue
            row.UnderlyingCurrency = underlyingCurrency
            row.StrikePrice = strikePrice
            row.LastModifiedDate = date_now = str(date_func.today())
            db.session.commit()
        except exc.IntegrityError:
           raise exc.IntegrityError("", "", 1)

    # serves the trades delete request
    @classmethod
    def delete_trade(cls, trade_id):
        try:
            cls.query.filter_by(TradeID = trade_id).delete()
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)

class EventLogModel(db.Model):
    __tablename__ = 'EventLog'
    EventID = db.Column(db.Integer, primary_key = True, nullable = False)
    EventDescription = db.Column(db.String(120), nullable = False)
    DateOfEvent = db.Column(db.String(120), nullable = False)
    Table = db.Column(db.String(120), nullable = False)
    TypeOfAction = db.Column(db.String(120), nullable = False)
    ReferenceID = db.Column(db.String(120), nullable = False)
    EmployeeID = db.Column(db.String(120), ForeignKey("Employees.EmployeeID"), nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

    # gets all events logges for a certain day
    @classmethod
    def get_events(cls, date):
        try:
            return cls.query.filter(cls.DateOfEvent <= date).with_entities(EventLogModel.DateOfEvent, EventLogModel.UserAction)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)
    
    @classmethod
    def get_actions_by_user(cls, id):
        try:
            return cls.query.filter(cls.EmployeeID == id)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

class EmployeesModel(db.Model):
    __tablename__ = 'Employees'
    EmployeeID = db.Column(db.Integer, primary_key = True, nullable = False)
    FirstName = db.Column(db.String(120), nullable = False)
    LastName = db.Column(db.String(120), nullable = False)
    Email = db.Column(db.String(120), nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

    @classmethod
    def retrieve_all(cls):
        try:
            return cls.query.all()
        except exc.ProgrammingError:
            raise exc.ProgrammingError("","",1)

    @classmethod
    def retrieve_by_user_id(cls, id):
        try:
            return cls.query.filter_by(EmployeeID = id).first()
        except exc.ProgrammingError:
            raise exc.ProgrammingError("","",1)


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

    # serves the product patch request
    @classmethod
    def update_product_sellers(cls, product_id, company_ID):
        try:
            row = cls.query.filter_by(ProductID = product_id).first()
            row.CompanyCode = company_ID
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)

    # unsure what this does
    # maybe checks if a comapny sells that product
    @classmethod
    def getProductID(cls, productID, companyCode):
        try:
            return cls.query.filter(ProductSellersModel.CompanyCode == companyCode).filter(ProductSellersModel.ProductID == productID).all()
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)


class ProductModel(db.Model):
    __tablename__ = 'Products'
    ProductID = db.Column(db.Integer, primary_key = True, nullable = False)
    ProductName = db.Column(db.String(120), nullable = False)
    DateEnteredInSystem = db.Column(db.String(120), nullable = False)
    DateDeleted = db.Column(db.String(120))
    UserIDCreatedBy = db.Column(db.String(120), nullable = False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.ProductID
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
        except exc.InterfaceError:
            raise exc.InterfaceError("","", 1)

    # serves the product patch request
    @classmethod
    def update_product(cls, product_id, name):
        try:
            row = cls.query.filter_by(ProductID = product_id).first()
            row.ProductName = name
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)

    @classmethod
    def update_date_deleted(cls, product_id, date):
        try:
            row = cls.query.filter_by(ProductID = product_id).first()
            row.DateDeleted = date
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("", "", 1)

    # serves the product delete request
    @classmethod
    def delete_product(cls, product_id):
        try:
            cls.query.filter_by(ProductID = product_id).delete()
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)

    # serves the product get request for a certain date
    @classmethod
    def retrieve_products_on_date(cls, date):
        try:
            return cls.query.filter(cls.ProductID == ProductSellersModel.ProductID, ProductSellersModel.ProductID == ProductValuationsModel.ProductID, func.DATE(cls.DateEnteredInSystem) <= parse_iso_date(date), or_(parse_iso_date(date) < func.DATE(cls.DateDeleted), cls.DateDeleted == None)).\
            with_entities(cls.ProductID, cls.ProductName, ProductSellersModel.CompanyCode, ProductValuationsModel.ProductPrice, cls.DateEnteredInSystem)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    @classmethod
    def retrieve_products(cls):
        try:
            return cls.query.filter(cls.ProductID == ProductSellersModel.ProductID, ProductSellersModel.ProductID == ProductValuationsModel.ProductID).\
            with_entities(ProductModel.ProductID, ProductModel.ProductName, ProductSellersModel.CompanyCode, ProductValuationsModel.ProductPrice, ProductModel.DateEnteredInSystem)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)

    @classmethod
    def retrieve_all_products(cls):
        try:
            return cls.query.all()
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)
    
    @classmethod
    def retrieve_all_product_company_info(cls):
        try:
            return cls.query.filter(cls.ProductID == ProductSellersModel.ProductID).\
            with_entities(cls.ProductID, ProductSellersModel.CompanyCode, cls.ProductName, cls.DateEnteredInSystem)
        except exc.ProgrammingError:
            raise exc.ProgrammingError("", "", 1)
    
    @classmethod
    def retrieve_product_by_id(cls, id):
        try:
            return cls.query.filter(cls.ProductID == id, cls.ProductID == ProductSellersModel.ProductID).\
                with_entities(cls.ProductID, ProductSellersModel.CompanyCode, cls.ProductName, cls.DateEnteredInSystem)
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

    # serves the product patch request
    @classmethod
    def update_product_valuations(cls, product_id, price, date_entered):
        try:
            row = cls.query.filter_by(ProductID = product_id).first()
            row.ProductPrice = price
            row.DateOfValuation = date_entered
            db.session.commit()
        except exc.IntegrityError:
            raise exc.IntegrityError("","",1)
