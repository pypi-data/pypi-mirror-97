import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from json import load
import yahoofinancials as yf
from datetime import datetime

from quantifin.equity import Stock
from quantifin.equity.valuation import *
from quantifin.util import markets

@patch.object(yf.YahooFinancials, 'get_beta', return_value = 1.2)
class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).parent
        self.index_json = self.read_json(str(self.base_path) + "/resource/market_price.json")
    
    def read_json(self, file_path):
        with open (file_path) as f:
            json_dict = load(f)
        return json_dict

    def test_CAPM(self, MockGetBeta):
        req_rate_CAPM = CAPM(0.02, 0.1, 1.2)
        self.assertEqual(req_rate_CAPM, 0.116)
    
    #################
    #Dividend testing
    #################
    def test_get_FY_dividend_period(self, MockGetBeta):
        stock = Stock("AAPL")
        dec = datetime(2019, 12, 10)
        self.assertEqual(stock._get_FY_dividend_period(dec), [datetime(2019, 1, 1), dec])

        not_dec = datetime(2019, 11, 29)
        self.assertEqual(stock._get_FY_dividend_period(not_dec), [datetime(2018, 1, 1), datetime(2018, 12, 30)])
    

    def test_calculate_dividend(self, MockGetBeta):
        stock = Stock("D05.SI")

        dividend_resp = self.read_json(str(self.base_path) + "/resource/dividend/2020_dbs_dividend.json")
        
        self.assertEqual(stock._calculate_full_dividend(dividend_resp), 1.35)
        self.assertEqual(stock._calculate_full_dividend({"D05.SI": None}), 0)
        amzn = Stock("AMZN")
        dividend_resp = {'AMZN': None}
        self.assertEqual(amzn._calculate_full_dividend(dividend_resp), 0)

    @patch.object(yf.YahooFinancials, 'get_daily_dividend_data')
    def test_get_current_dividend(self, MockDividend, MockGetBeta):
            
        MockDividend.side_effect = self.get_dividend_side_effect
        stock = Stock("D05.SI")
        self.assertEqual(stock.full_year_dividend(), 1.35)
    
    #Payout Ratio tests
    @patch.object(yf.YahooFinancials, 'get_financial_stmts')
    def test_average_payout_ratio(self, MockGetFnStmts, MockGetBeta):
        MockGetFnStmts.side_effect = self.get_financial_stmts_side_effect
        stock = Stock("D05.SI")
        cf = stock.get_financial_stmts('annual', 'cash')
        correct = {'2020': 0.511, '2019': 0.615, '2018': 0.565, '2017': 0.315}
        self.assertEqual(stock.get_dividend_payout_ratio_history(), correct)
        self.assertEqual(stock.average_dividend_payout_ratio(stock.get_dividend_payout_ratio_history()), 0.501)
    
    @patch.object(Stock, 'get_financial_stmts')
    def test_payout_history_no_payout(self, MockCashFlow, MockGetBeta):
        MockCashFlow.side_effect = lambda p, s: self.read_json(str(self.base_path) + '/resource/financial_statements/AMZN_cash_flow_stmts.json')
        amzn = Stock("AMZN")
        self.assertEqual(amzn.get_dividend_payout_ratio_history(), {'2020': 0, "2019": 0, "2018": 0, "2017": 0})
    
    @patch.object(yf.YahooFinancials, "get_financial_stmts")
    def test_get_roe_history(self, MockGetFnStmts, MockGetBeta):
        MockGetFnStmts.side_effect = self.get_financial_stmts_side_effect

        stock = Stock("D05.SI")
        correct_result = {"2020": 0.086, "2019": 0.123, "2018": 0.112, "2017": 0.088}
        self.assertEqual(stock.get_roe_history(), correct_result)
    
    def test_calulate_roe(self, MockGetBeta):
        stock = Stock("D05.SI")
        self.assertRaises(ValueError, stock.calculate_roe, 100, 0)
        self.assertRaises(ValueError, stock.calculate_roe, 100, -100)
        self.assertEqual(stock.calculate_roe(50, 300), 0.167)
    
    @patch.object(yf.YahooFinancials, "get_financial_stmts")
    def test_get_average_roe(self, MockGetFnStmts, MockGetBeta):
        MockGetFnStmts.side_effect = self.get_financial_stmts_side_effect
        stock = Stock("D05.SI")
        roe = stock.get_roe_history()
        self.assertEqual(stock.average_roe(roe), 0.102)

    @patch.object(yf.YahooFinancials, "get_financial_stmts")
    def test_growth_rate(self, MockGetFnStmts, MockGetBeta):
        MockGetFnStmts.side_effect = self.get_financial_stmts_side_effect
        stock = Stock("D05.SI")
        self.assertEqual(stock.growth_rate(), 0.051)
         

    
    def get_dividend_side_effect(self, start_date, end_date):
        dividend_path = str(self.base_path) + "/resource/dividend/2020_dbs_dividend.json"
        return self.read_json(dividend_path)

    
    def get_financial_stmts_side_effect(self, period, stmt_type):
        if( stmt_type == "cash"):
            return(self.read_json(str(self.base_path) + '/resource/financial_statements/cash_flow_stmts.json'))
        if(stmt_type == "income"):
            return(self.read_json(str(self.base_path) + '/resource/financial_statements/income_stmts.json'))
        if(stmt_type == "balance"):
            return(self.read_json(str(self.base_path) + '/resource/financial_statements/balance_sheet_stmts.json'))