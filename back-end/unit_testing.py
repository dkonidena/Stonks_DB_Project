import unittest
import json 
from run import app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_cs261_2.0.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class MyTestClass(unittest.TestCase): 
    
    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass 

    # clean up logic for the test suite declared in the test module
    # code that is executed after all tests in one test run
    @classmethod
    def tearDownClass(cls):
        pass 

    # initialization logic
    # code that is executed before each test
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 
    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass 

    # test method
    #def test_equal_numbers(self):
    #    self.assertEqual(2, 2) 
    #
    #def test_home_status_code(self):
    #    # sends HTTP GET request to the application
    #    # on the specified path
    #    result = self.app.get('/') 
    #
    #    # assert the status code of the response
    #    self.assertEqual(result.status_code, 200)

class CurrencyTests(unittest.TestCase):
    # initialization logic
    # code that is executed before each test
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass 

    # test to check the correct number of matches are found when a specific date is chosen
    def test_num_returned_currencies(self):
        date = "2019-12-01"
        response = self.app.get('/api/currencies', query_string=dict(isDryRun = 'true', date = date))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['noOfMatches'], 8)
    
    # test to check if the system handles missing isDryRun data
    def test_no_dry_run_currencies(self):
        response = self.app.get('api/currencies', query_string=dict(date = None))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("Request malformed", data['message'])

    # TODO: Handling a case where a date isn't returned
    # def test_no_date_currencies(self):
    #     response = self.app.get('api/currencies', query_string=dict(date = 'ababa', isDryRun = 'false'))
    #     self.assertEqual(response.status_code, 400)
    #     data = json.loads(response.get_data(as_text=True))
    #     self.assertEqual("Date invalid", data['message'])

class CompanyTests(unittest.TestCase):
    # initialization logic
    # code that is executed before each test
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass 

    def test_no_dry_run_companies(self):
        response = self.app.get('api/companies', query_string=dict(date = None))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("Request malformed", data['message'])

    def test_no_date_companies(self):
        response = self.app.get('api/companies', query_string=dict(date = 'ababa', isDryRun = 'false'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("Date invalid", data['message'])

    def test_num_returned_companies(self):
        date = "2020-02-12"
        response = self.app.get('/api/companies', query_string=dict(isDryRun = 'true', date = date))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['noOfMatches'], 202)

    # tests whether a company name is blank when inserting a new company
    def test_company_name_empty_post(self):
        response = self.app.post('api/companies', data=json.dumps(dict(name='')), headers={'userID':'1'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("company name is empty", data['message'])

    # test to see if a user ID does not exist
    def test_no_userID_company_post(self):
        response = self.app.post('api/companies', data=dict(name=''), headers={'userID':'9999'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("user not present", data['message'])
    
    def test_no_id_delete_company(self):
        id = 'P'
        response = self.app.delete('/api/companies', query_string=dict(id = id), headers = {'userID':'1'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("Cannot delete a non-existant company", data['message'])


class TradeTests(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass

    def test_no_dry_run_trades(self):
        response = self.app.get('api/trades', query_string=dict(filter = {}))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("malformed filter", data['message'])

    def test_no_filter_trades(self):
        response = self.app.get('api/trades', query_string=dict(isDryRun = 'false'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("malformed filter", data['message'])

    def test_num_returned_trades(self):
        response = self.app.get('/api/trades', query_string=dict(isDryRun = 'true', filter = {}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['noOfMatches'], 2908) 

    # test to see if a user ID does not exist
    def test_no_userID_trades_post(self):
        response = self.app.post('api/trades', data=dict(product='74', quantity='2', buyingParty='DDIB11', sellingParty ='UFAY59', notionalPrice ='1', notionalCurrency ='USD', underlyingPrice = '2', underlyingCurrency = 'USD', strikePrice = '3', maturityDate='2024-07-13'), headers={'userID':'9999'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("user not present", data['message'])

    #TODO: Edit DELETE trades to use .count() to check for any returned results
    def test_no_id_delete_trades(self):
        tradeID = 'P'
        response = self.app.delete('/api/trades', query_string=dict(id = tradeID), headers = {'userID':'1'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("Trade id not present", data['message'])
        
    def test_no_product_trades_post(self):
        response = self.app.post('api/trades', data=json.dumps(dict(product='99999', quantity='2', buyingParty='DDIB11', sellingParty ='UFAY59', notionalPrice ='1', notionalCurrency ='USD', underlyingPrice = '2', underlyingCurrency = 'USD', strikePrice = '3', maturityDate='2024-07-13')), headers={'userID':'1'})
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("product not found", data['message'])

class ProductTests(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass 

    def test_no_dry_run_products(self):
        response = self.app.get('api/products', query_string=dict(date = None))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("Request malformed", data['message'])

    def test_no_date_products(self):
        response = self.app.get('api/products', query_string=dict(date = 'ababa', isDryRun = 'false'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("Date invalid", data['message'])

    #TODO: Need to return products that existed on or after the date, whilst also returning the most recent valuation.
    def test_num_returned_products(self):
        TOTAL_PRODUCTS_IN_DB = 303
        response = self.app.get('/api/products', query_string=dict(isDryRun = 'true'))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['noOfMatches'], TOTAL_PRODUCTS_IN_DB)

    # tests whether a product name is blank when inserting a new product
    def test_product_name_empty_post(self):
        response = self.app.post('api/products', data=json.dumps(dict(name='', companyID='', valueInUSD='')), headers={'userID':'1'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        print("Data: ", data['message'])
        self.assertEqual("product name is empty", data['message'])
    
    # test to see if a user ID does not exist
    def test_no_userID_product_post(self):
        response = self.app.post('api/products', data=dict(name='', valueInUSD=None, companyID=''), headers={'userID':'9999'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("user not present", data['message'])

    #TODO: Check the product ID before deletion
    def test_no_id_delete_product(self):
        id = 0
        response = self.app.delete('/api/products', query_string=dict(id = id), headers = {'userID':'1'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("Cannot delete a non-existant product", data['message'])

class UserTests(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass 

    def test_num_returned_users(self):
        TOTAL_NUM_USERS = 4
        response = self.app.get('/api/users', query_string=dict(isDryRun = 'true'))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['noOfMatches'], TOTAL_NUM_USERS)

class ReportTests(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass 

    def test_no_filter_reports(self):
        response = self.app.get('api/reports', query_string=dict(isDryRun = 'false'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("filter not present", data['message']) 

    def test_no_dry_run_reports(self):
        response = self.app.get('api/products', query_string=dict(filter={}))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual("Request malformed", data['message'])
    
    def test_num_returned_reports(self):
        response = self.app.get('/api/reports', query_string=dict(isDryRun = 'true', filter={}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['noOfMatches'], 22)

# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()