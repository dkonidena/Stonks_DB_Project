# CS261 Software Engineering | Group 32: Back-End

This file will explain the purposes of each of the database schema defined in the .db file

DerivativeTrades:
Contains all the information on all trades made by a buying party, what type of asset is being purchased, the notional value and its currency, the underlying value and its currency, the strike price in the underlying currency, the date of when the purchase can be made, and the quantity of assets bought.
* TradeID
* DateOfTrade
* AssetType
* BuyingParty
* SellingParty
* NotionalValue
* NotionalCurrency
* Quantity
* MaturityDate
* UnderlyingValue
* UnderlyingCurrency
* StrikePrice

CurrencyTypes:
Defines all the available currency in the world or exchanged in the simulated market. Each currency has a:
* Currency Code (Unique ID)
* Currency Name
* Country of Origin

CurrencyValuations:
Stores all the valuations given to a specific currency type for different dates.
* CurrencyCode
* DateOfValuation
* ValueInUSD (Amount of currency that can be bought for 1 USD)

Products:
Details all the products available
* ProductID
* ProductName

ProductSellers:
* ProductID
* CompanyCode

ProductValuations:
Stores all the valuations of each product for each specified date, giving the value in USD
* ProductID
* DateOfValuation
* MarketPrice

ProductTrades:
Provides all the trades that involve purchasing a product as the asset type
* ProductID
* TradeID

Stocks:
Provides all the stocks available for purchase, and the company that provides the stocks.
* StockID
* CompanyCode

StockValuations:
Stores all the valuations of a specific stock at a specific date - the valuation is the cost of a single stock in USD.
* StockID
* DateOfValuation
* StockPrice

StockTrades:
Stores all trades that are purchasing a stock asset, and the respective stock that is being purchased
* StockID
* TradeID

Employees:
Details of the employees working on the system are stored
* EmployeeID
* FirstName
* LastName
* Email
* Password

EventLog:
Any time a modification is made in the database by the user, a new record is stored in the EventLog table which outlines what the action was: adding a record, updating, deleting. Also, the date of the event is kept, and the user who performed this action. New records can be added via a trigger, or by a separate call to an SQL function to insert a new record into the table.
* EventID
* UserAction (the action taken by the user on the schema: SELECT, UPDATE, INSERT, DELETE)
* DateOfEvent
* EmployeeID
