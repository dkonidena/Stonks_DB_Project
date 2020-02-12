BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Products";
CREATE TABLE IF NOT EXISTS "Products" (
	"ProductID"	INTEGER NOT NULL,
	"ProductName"	TEXT NOT NULL,
	"DateEnteredInSystem"	TEXT NOT NULL,
	PRIMARY KEY("ProductID")
);
DROP TABLE IF EXISTS "Employees";
CREATE TABLE IF NOT EXISTS "Employees" (
	"EmployeeID"	INTEGER NOT NULL,
	"FirstName"	TEXT NOT NULL,
	"LastName"	TEXT NOT NULL,
	"Email"	TEXT NOT NULL,
	"Password"	TEXT NOT NULL,
	PRIMARY KEY("EmployeeID")
);
DROP TABLE IF EXISTS "EventLog";
CREATE TABLE IF NOT EXISTS "EventLog" (
	"EventID"	INTEGER NOT NULL,
	"UserAction"	TEXT NOT NULL,
	"DateOfEvent"	TEXT NOT NULL,
	"EmployeeID"	INTEGER NOT NULL,
	PRIMARY KEY("EventID"),
	FOREIGN KEY("EmployeeID") REFERENCES "Employees"("EmployeeID") ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS "Stocks";
CREATE TABLE IF NOT EXISTS "Stocks" (
	"StockID"	INTEGER NOT NULL,
	"CompanyCode"	TEXT NOT NULL,
	PRIMARY KEY("StockID"),
	FOREIGN KEY("CompanyCode") REFERENCES "Companies"("CompanyCode") ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS "DerivativeTrades";
CREATE TABLE IF NOT EXISTS "DerivativeTrades" (
	"TradeID"	TEXT,
	"DateOfTrade"	TEXT,
	"AssetType"	TEXT,
	"BuyingParty"	TEXT NOT NULL,
	"SellingParty"	TEXT NOT NULL,
	"NotionalValue"	REAL,
	"NotionalCurrency"	REAL,
	"Quantity"	INTEGER NOT NULL,
	"MaturityDate"	TEXT NOT NULL,
	"UnderlyingValue"	REAL NOT NULL,
	"UnderlyingCurrency"	TEXT NOT NULL,
	"StrikePrice"	REAL NOT NULL,
	PRIMARY KEY("TradeID"),
	FOREIGN KEY("SellingParty") REFERENCES "Companies"("CompanyCode") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("UnderlyingCurrency") REFERENCES "CurrencyTypes"("CurrencyCode") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("BuyingParty") REFERENCES "Companies"("CompanyCode") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("NotionalCurrency") REFERENCES "CurrencyTypes"("CurrencyCode") ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS "ProductSellers";
CREATE TABLE IF NOT EXISTS "ProductSellers" (
	"ProductID"	INTEGER NOT NULL,
	"CompanyCode"	TEXT NOT NULL,
	FOREIGN KEY("CompanyCode") REFERENCES "Companies"("CompanyCode") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("ProductID") REFERENCES "Products"("ProductID") ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY("ProductID","CompanyCode")
);
DROP TABLE IF EXISTS "ProductTrades";
CREATE TABLE IF NOT EXISTS "ProductTrades" (
	"ProductID"	INTEGER NOT NULL,
	"TradeID"	TEXT NOT NULL,
	PRIMARY KEY("ProductID","TradeID"),
	FOREIGN KEY("ProductID") REFERENCES "Products"("ProductID") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("TradeID") REFERENCES "DerivativeTrades"("TradeID") ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS "ProductValuations";
CREATE TABLE IF NOT EXISTS "ProductValuations" (
	"DateOfValuation"	TEXT NOT NULL,
	"ProductID"	INTEGER NOT NULL,
	"ProductPrice"	REAL NOT NULL,
	PRIMARY KEY("DateOfValuation","ProductID"),
	FOREIGN KEY("ProductID") REFERENCES "Products"("ProductID") ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS "StockValuations";
CREATE TABLE IF NOT EXISTS "StockValuations" (
	"DateOfValuation"	TEXT NOT NULL,
	"StockID"	INTEGER NOT NULL,
	"StockPrice"	REAL NOT NULL,
	FOREIGN KEY("StockID") REFERENCES "Stocks"("StockID") ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY("DateOfValuation","StockID")
);
DROP TABLE IF EXISTS "StockTrades";
CREATE TABLE IF NOT EXISTS "StockTrades" (
	"StockID"	INTEGER NOT NULL,
	"TradeID"	TEXT NOT NULL,
	FOREIGN KEY("StockID") REFERENCES "Stocks"("StockID") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("TradeID") REFERENCES "DerivativeTrades"("TradeID") ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY("StockID","TradeID")
);
DROP TABLE IF EXISTS "Companies";
CREATE TABLE IF NOT EXISTS "Companies" (
	"CompanyCode"	TEXT NOT NULL,
	"CompanyName"	TEXT,
	"DateEnteredInSystem"	TEXT,
	PRIMARY KEY("CompanyCode")
);
DROP TABLE IF EXISTS "CurrencyValuations";
CREATE TABLE IF NOT EXISTS "CurrencyValuations" (
	"DateOfValuation"	TEXT NOT NULL,
	"CurrencyCode"	TEXT NOT NULL,
	"ValueInUSD"	REAL NOT NULL,
	PRIMARY KEY("DateOfValuation","CurrencyCode"),
	FOREIGN KEY("CurrencyCode") REFERENCES "CurrencyTypes"("CurrencyCode") ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS "CurrencyTypes";
CREATE TABLE IF NOT EXISTS "CurrencyTypes" (
	"CurrencyCode"	TEXT NOT NULL UNIQUE,
	"CurrencyName"	TEXT NOT NULL,
	"Country"	TEXT NOT NULL,
	PRIMARY KEY("CurrencyCode")
);
COMMIT;

CREATE OR REPLACE TRIGGER idnull
	BEFORE INSERT ON "Products"
	FOR EACH ROW
	DECLARE
	c INTEGER;
	BEGIN
		c := 1;
		IF (:new.ProductID is null) OR (checkProductID(:new.ProductID) = 1)