import os
import sqlite3
import csv

def convertDate(date):
    newDate = date[6:10] + '-' + date[3:5] + '-' +date[0:2]
    return newDate

years = ['2019']
months = ['December']

try:
    con = sqlite3.connect("database_cs261_2.0.db")
except sqlite3.Error:
    print("Couldn't connect to the DB")

path = 'C:\\Users\\rohan\\OneDrive\\Documents\\WARWICK 2019-20\\CS261\\Coursework\\Coursework Dummy Data\\derivativeTrades'
# check for every year specified
for year in years:
    # check for every month specified
    for month in months:
        dPath = path + "\\" + year + "\\" + month # directory path

        # find all .csv files
        # for each file, get all the values in each row and insert them
        for entry in os.listdir(dPath):
            if os.path.isfile(os.path.join(dPath, entry)):
                filePath = dPath + '\\' + entry
                #print(entry)
                with open(filePath,'r') as fin: # `with` statement available in 2.5+
                    # csv.DictReader uses first line in file for column headings by default
                    dr = csv.DictReader(fin) # comma is default delimiter
                    for row in dr:
                        dateOfTrade = convertDate(row['dateOfTrade'])
                        tradeID = row['tradeID']
                        productName = row['product']
                        buyingParty = row['buyingParty']
                        sellingParty = row['sellingParty']
                        notionalValue = float(row['notionalAmount'])
                        notionalCurrency = str(row['notionalCurrency'])
                        quantity = row['quantity']
                        maturityDate = convertDate(row['maturityDate'])
                        underlyingValue = float(row['underlyingPrice'])
                        underlyingCurrency = str(row['underlyingCurrency'])
                        strikePrice = float(row['strikePrice'])
                        userIDcreatedBy = 1
                    
                        try:
                            cur = con.cursor()
                            cur.execute("SELECT CurrencyCode FROM CurrencyTypes WHERE CurrencyCode = ? AND CurrencyCode = ?", (notionalCurrency, underlyingCurrency))
                            rows = cur.fetchall()
                            if len(rows) == 0:
                                continue
                        except sqlite3.DatabaseError:
                                raise sqlite3.DatabaseError
                        finally:
                            cur.close()

                        try:
                            cur = con.cursor()
                            cur.execute("SELECT Products.ProductID FROM Products, ProductSellers WHERE ProductName = ? AND Products.ProductID = ProductSellers.ProductID AND ProductSellers.CompanyCode = ?", (productName, sellingParty,))
                            rows = cur.fetchall()
                            if len(rows) == 0:
                                continue
                        except sqlite3.DatabaseError:
                            continue
                        finally:
                            cur.close()

                        for row in rows:
                            productID = row[0]


                        try:
                            #print(tradeID)
                            cur = con.cursor()
                            cur.execute("INSERT INTO DerivativeTrades (DateOfTrade, TradeID, ProductID, BuyingParty, SellingParty, OriginalNotionalValue, NotionalValue, NotionalCurrency, OriginalQuantity, Quantity, MaturityDate, UnderlyingValue, UnderlyingCurrency, StrikePrice, UserIDCreatedBy) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (dateOfTrade, tradeID, productID, buyingParty, sellingParty, notionalValue, notionalValue, notionalCurrency, quantity, quantity, maturityDate, underlyingValue, underlyingCurrency, strikePrice, userIDcreatedBy,))
                            con.commit()
                        except sqlite3.IntegrityError:
                            exit(0)
                            con.rollback()
                            print("Problem with DerivativeTrades")
                            raise sqlite3.DatabaseError
                        finally:
                            cur.close()

                        try:
                            cur = con.cursor()
                            cur.execute("INSERT INTO ProductTrades (ProductID, TradeID) VALUES (?,?)", (productID, tradeID,))
                            con.commit()
                        except sqlite3.DatabaseError:
                            con.rollback()
                            print("Problem with ProductTrades")
                            raise sqlite3.DatabaseError
                        finally:
                            cur.close()


con.close()
