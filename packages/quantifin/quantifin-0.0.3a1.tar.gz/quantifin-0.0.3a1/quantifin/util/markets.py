import yahoofinancials as yf 
from datetime import datetime, timedelta
from enum import Enum

EXCHANGES = {"NasdaqGS": "^IXIC",
             "NYSE": "^NYA",
             "SES": "^STI",
             "S&P": "^GSPC",
             "DJI": "^DJI",
             "HKSE": "^HSI",
             "VIX": "^VIX"
            }

class Market(yf.YahooFinancials):
    def __init__(self, market_code):
        self.market_code = EXCHANGES[market_code]
        super().__init__(self.market_code)
    
    @staticmethod
    def get_market_price_list(index_json: dict):
        index_code = list(index_json.keys())[0]
        return index_json[index_code]['prices']

    @staticmethod
    def returns(market_price_list: list):
        start_price = market_price_list[0]['close']
        end_price = market_price_list[-1]['close']
        market_return = (end_price / start_price)
        return market_return

    @staticmethod
    def annualise(market_return: float, period: float):
        return (market_return **(1/period)) - 1

    def get_annualised_return(self, year):
        def format_date(date: datetime):
            return date.strftime("%Y-%m-%d")
        
        def period_price_list(year):
            current_date = datetime.now()
            start_date = current_date - timedelta(weeks= 52 * year)
            return self.get_historical_price_data(format_date(start_date), format_date(current_date), 'monthly')
        price_resp = period_price_list(year)
        return round(self.annualise(self.returns(self.get_market_price_list(price_resp)), year), 4)
        


