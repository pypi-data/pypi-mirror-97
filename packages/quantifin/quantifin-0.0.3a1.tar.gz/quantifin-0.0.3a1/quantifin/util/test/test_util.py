import unittest
from unittest.mock import patch
from pathlib import Path
import json
from yahoofinancials import YahooFinancials

from quantifin.util.markets import Market


class TestCase(unittest.TestCase):
    def setUp(self):
        #self.stock = Stock("AAPL")
        self.base_path = Path(__file__).parent
        self.index_json = self.read_json(str(self.base_path) + "/resource/market_price.json")
    
    def read_json(self, file_path):
        with open (file_path) as f:
            json_dict = json.load(f)
        return json_dict

    def test_get_market_price_list(self):
        index_price_list = Market.get_market_price_list(self.index_json)
        index_code = list(self.index_json.keys())[0]
        self.assertEqual(index_price_list, self.index_json[index_code]['prices']) 


    def test_get_market_return(self):
        annual_return = 13597.9658203125  / 7729.31982421875

        index_price_list = Market.get_market_price_list(self.index_json)
        self.assertAlmostEqual(Market.returns(index_price_list), annual_return, 3)
    
    def test_get_annualised_market_return(self):
        market_returns = Market.returns(Market.get_market_price_list(self.index_json))
        annualised_return = Market.annualise(market_returns, 2)
        self.assertEqual(annualised_return, (((13597.9658203125  / 7729.31982421875) ** (1/2)) - 1))
    
    @patch.object(YahooFinancials, "get_historical_price_data")
    def test_Market_obj_init(self, MockGetPrice):
        nasdaq = Market("NasdaqGS")
        self.assertTrue(nasdaq.market_code, "^IXIC")


    @patch.object(YahooFinancials, "get_historical_price_data")
    def test_Market_get_annualised_return(self, MockGetPrice):
        def get_price_side_effect(start, end, period):
            file_path = str(self.base_path) + "/resource/s&p_10_year_price.json"
            return self.read_json(file_path)

        MockGetPrice.side_effect = get_price_side_effect
        sp500 = Market("S&P")
        self.assertEqual(sp500.get_annualised_return(10), 0.1334)
