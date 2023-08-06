import yahoofinancials as yf
import datetime
class Stock(yf.YahooFinancials):
    def __init__(self, stock_code):
        self.stock_code = stock_code
        super().__init__(stock_code)
        self.__beta = None 
        self.__cash_flow = None
        self.__income = None
        self.__balance_sheets = None
        self.__key_stats = None

    @staticmethod
    def get_date_key(input_dict: dict):
        return (list(input_dict.keys())[0])

    @property
    def beta(self):
        if self.__beta == None:
            self.__beta = self.get_beta()
        return self.__beta
    
    @property
    def trailing_eps(self):
        try:
            return self.key_stats['trailingEps']
        except KeyError:
            return None 
    
    @property
    def forward_eps(self):
        try:
            return self.key_stats['forwardEps']
        except KeyError:
            return None

    @property
    def key_stats(self):
        if self.__key_stats is None:
            self.__key_stats = self.get_key_statistics_data()[self.stock_code]
        return self.__key_stats

    @property
    def cash_flow_stmts(self):
        if self.__cash_flow == None:
            self.__cash_flow =  self.get_financial_stmts("annual", "cash")['cashflowStatementHistory'][self.stock_code]
        return self.__cash_flow
    
    @property
    def income_stmts(self):
        if self.__income == None:
            self.__income = self.get_financial_stmts("annual", "income")['incomeStatementHistory'][self.stock_code]
        return self.__income
    
    @property
    def balance_sheet_stmts(self):
        if self.__balance_sheets == None:
            self.__balance_sheets = self.get_financial_stmts("annual", "balance")['balanceSheetHistory'][self.stock_code]
        return self.__balance_sheets


    def full_year_dividend(self):
        now_date = datetime.datetime.now()
        start_of_year, end_of_year = self._get_FY_dividend_period(now_date)
        dividend_resp = self.get_daily_dividend_data(start_of_year.strftime("%Y-%m-%d"), end_of_year.strftime("%Y-%m-%d"))
        return self._calculate_full_dividend(dividend_resp)
    
    def _get_FY_dividend_period(self, now: datetime.datetime):
        def current_year(now: datetime.datetime):
            this_year = now.year
            return [datetime.datetime(this_year, 1, 1), now]
        
        def previous_year(now: datetime.datetime):
            year = now.year - 1
            return [datetime.datetime(year, 1, 1), datetime.datetime(year, 12, 30)]

        if (now.month == 12):
            return current_year(now) 
        return previous_year(now)

    def _calculate_full_dividend(self, dividend_resp: dict):
        if dividend_resp[self.stock_code] is None:
            return 0
        dividends = [payout['amount'] for payout in dividend_resp[self.stock_code]]
        return round(sum(dividends), 3)

    def get_dividend_payout_ratio_history(self):
        ###Helper functions
        
        def calculate_payout(cash_flow):
            try:
                div_payout = abs(int(cash_flow['dividendsPaid']))
            except KeyError:
                return 0
            net_income = int(cash_flow['netIncome'])
            if net_income < 0:
                return 0
            return round(div_payout/net_income, 3)

        def get_payout_ratios(cf_stmts_list):
            result = {}
            for cash_flow in self.cash_flow_stmts:
                date_key = Stock.get_date_key(cash_flow)
                result[date_key[:4]] = calculate_payout(cash_flow[date_key])
            return result
        ## End of helper functions
        return get_payout_ratios(self.cash_flow_stmts)
    
    def average_dividend_payout_ratio(self, payout_ratio_history: dict):
        payout_list = [payout for payout in payout_ratio_history.values()]
        return round(sum(payout_list) / len(payout_list), 3)
    
    def get_roe_history(self):
        result = {}
        for i in range(len(self.balance_sheet_stmts)):
            date_key = Stock.get_date_key(self.balance_sheet_stmts[i])
            net_equity = self.balance_sheet_stmts[i][date_key]['totalAssets'] - self.balance_sheet_stmts[i][date_key]['totalLiab']
            net_income = self.income_stmts[i][date_key]['netIncome']
            result[date_key[:4]] = self.calculate_roe(net_income, net_equity)
        return result

    def calculate_roe(self, income: float, equity: float):
        if equity == 0:
            raise ValueError("Equity should be a non-zero value. 0 was passed as equity")
        if equity < 0:
            raise ValueError(f"Equity is negative: {equity}. A postive value should be passed in")
        return round(income/equity, 3)

    def average_roe(self, roe_history: dict):
        sum = 0
        for roe in roe_history.values():
            sum += roe
        return round(sum / len(roe_history), 3)
    
    def growth_rate(self):
        payout = self.average_dividend_payout_ratio(self.get_dividend_payout_ratio_history())
        roe = self.average_roe(self.get_roe_history())
        if payout > 1:
            raise ValueError("Payout rate exceeds 1. Invalid value for growth rate")
        if roe < 0:
            raise ValueError("ROE is negative. Invalid value for growth rate")
        return round((1 - payout) * roe, 3)
    
