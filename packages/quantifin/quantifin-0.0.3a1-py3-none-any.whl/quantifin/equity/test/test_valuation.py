import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from json import load
import yahoofinancials as yf
from datetime import datetime

from quantifin.equity import Stock, valuation
from quantifin.util.markets import Market

@patch.object(yf.YahooFinancials, 'get_beta', return_value = 1.2)
class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).parent
        self.index_json = self.read_json(str(self.base_path) + "/resource/market_price.json")
    
    def read_json(self, file_path):
        with open (file_path) as f:
            json_dict = load(f)
        return json_dict

    def get_financial_stmts_side_effect(self, period, stmt_type):
        if( stmt_type == "cash"):
            return(self.read_json(str(self.base_path) + '/resource/financial_statements/cash_flow_stmts.json'))
        if(stmt_type == "income"):
            return(self.read_json(str(self.base_path) + '/resource/financial_statements/income_stmts.json'))
        if(stmt_type == "balance"):
            return(self.read_json(str(self.base_path) + '/resource/financial_statements/balance_sheet_stmts.json'))
    
    @patch.object(yf.YahooFinancials, "get_financial_stmts")
    def test_forward_pe(self, MockGetFnStmts, MockGetBeta):
        MockGetFnStmts.side_effect = self.get_financial_stmts_side_effect
        stock = Stock("D05.SI")
        sti = Market("SES")
        payout_history = stock.get_dividend_payout_ratio_history()
        payout = stock.average_dividend_payout_ratio(payout_history)
        growth = stock.growth_rate()
        req_rate = 0.1334
        forward_eps = 10
        self.assertEqual(valuation.forward_pe(payout, growth, req_rate, forward_eps), 63.902)
        self.assertRaises(Warning, valuation.forward_pe, payout, growth,req_rate, -10)
        
    @patch.object(yf.YahooFinancials, "get_financial_stmts")
    def test_forward_pe_no_payout(self, MockCashFlow, MockGetBeta):
        MockCashFlow.side_effect = lambda p, s: self.read_json(str(self.base_path) + '/resource/financial_statements/AMZN_cash_flow_stmts.json')
        amzn = Stock("AMZN")
        payout_history = amzn.get_dividend_payout_ratio_history()
        payout = amzn.average_dividend_payout_ratio(payout_history)
        self.assertEqual(payout, 0)
        self.assertRaises(ValueError, valuation.forward_pe, payout, 0.05, 0.1, 20)


    @patch.object(yf.YahooFinancials, 'get_daily_dividend_data')
    @patch.object(yf.YahooFinancials, "get_financial_stmts")
    def test_gordon_growth_valuation(self, MockGetFnStmts, MockDividend, MockGetBeta):
        MockDividend.side_effect = self.get_dividend_side_effect
        MockGetFnStmts.side_effect = self.get_financial_stmts_side_effect
        stock = Stock('D05.SI')
        current_dividend = stock.full_year_dividend()
        req_rate = valuation.CAPM(0.02, 0.10, 1.2)
        growth_rate = stock.growth_rate()
        self.assertRaises(ValueError, valuation.gordon_growth_valuation, -2, req_rate, growth_rate)
        self.assertRaises(ValueError, valuation.gordon_growth_valuation, current_dividend, -0.116, growth_rate)
        self.assertEqual(valuation.gordon_growth_valuation(current_dividend, req_rate, growth_rate), 21.828)

    @patch.object(Stock, "get_daily_dividend_data")
    def test_multistage_growth_valuation(self, MockDividend, MockGetBeta):
        MockDividend.side_effect = self.get_dividend_side_effect

        stock = Stock("D05.SI")
        current_dividend = stock.full_year_dividend()
        req_rate  =valuation.CAPM(0.02, 0.1, stock.beta)
        growth_trajectory = [(3, 0.1), (3, 0.05), (None, 0.01)]

        self.assertRaises(ValueError, valuation.multistage_growth, current_dividend, req_rate, [(2, 0.1), (2, 0.05), (2, 0.02)]) #No terminal value
        self.assertEqual(valuation.multistage_growth(current_dividend, req_rate, growth_trajectory), 17.631)


    
    @patch.object(yf.YahooFinancials, 'get_daily_dividend_data', return_value={'AMZN': None})
    def test_gordon_growth_no_dividend_error(self,MockDividend, MockGetBeta):
        amzn = Stock("AMZN")
        current_dividend = amzn.full_year_dividend()
        self.assertRaises(ValueError, valuation.gordon_growth_valuation, current_dividend, 0.12, 0.05)
    
    def get_dividend_side_effect(self, start_date, end_date):
        dividend_path = str(self.base_path) + "/resource/dividend/2020_dbs_dividend.json"
        return self.read_json(dividend_path)