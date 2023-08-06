from functools import reduce, partial

from quantifin.equity import Stock
from quantifin.util import markets

def CAPM(risk_free: float, market_premium: float, beta: float):
    return risk_free + beta * (market_premium - risk_free)

def gordon_growth_valuation(current_dividend: float, req_rate: float, growth_rate: float):
    if current_dividend == 0:
        raise ValueError(__valuation_error_message("Dividend"))
    if  __any_negative_value([current_dividend, req_rate]):
        raise ValueError("Invalid value. Either current_dividend or required rate is negative")
    return round((current_dividend * (growth_rate + 1)) / (req_rate - growth_rate), 3)

def __any_negative_value(values: list):
    for val in values:
        if val < 0:
             return True
    return False

def forward_pe(payout_ratio: float, growth_rate: float, req_rate: float, eps: float):
    if payout_ratio == 0:
        raise ValueError(__valuation_error_message("Payout"))
    if __any_negative_value([payout_ratio, growth_rate, eps]):
        raise Warning("One or more of the values supplied is negative. This may reduce the effectiveness of the result")
    exp_payout = payout_ratio * (1 + growth_rate)
    forward_pe = exp_payout / (req_rate - growth_rate)
    return round(forward_pe * eps, 3)

def multistage_growth(current_cf: float, req_rate: float, growth_trajectory: list):
    ##Helper methods
    def no_terminal_value(trajectory: list):
        return trajectory[-1][0] is not None
    
    def terminal_value(dividend, growth_rate, req_rate):
        return (dividend * (1 + growth_rate))/ (req_rate - growth_rate)
    
    def calculate_dividend_projection(growth_tuple: tuple, current_cf):
        projection = []
        for i in range(growth_tuple[0]):
            current_cf *= (1 + growth_tuple[1])
            projection.append(current_cf)     
        return projection
    
    def present_value_reduce(accum, value, discount_rate):
        return (accum + value) / (1 + discount_rate)
    ##End of helper function 

    if no_terminal_value(growth_trajectory):
        raise ValueError("No terminal growth rate provided. Please append a tuple at the end of growth_trajectory with value (None, <growth_rate>)")

    proj_dividends = []
    for growth in growth_trajectory[:-1]:   
        proj_dividends.extend(calculate_dividend_projection(growth, current_cf))
        current_cf =  proj_dividends[-1]  #Update current dividend based on projection

    proj_dividends[-1] += (terminal_value(proj_dividends[-1], growth_trajectory[-1][1], req_rate))   #Append terminal value
    partial_present_value_reduce = partial(present_value_reduce, discount_rate = req_rate)  #Generate partial reduce func with discount rate = req rate

    return round(reduce(partial_present_value_reduce, proj_dividends[::-1], 0), 3)

def __valuation_error_message(value):
    return f"{value} provided is 0. Result using this valuation method is invalid"

'''
 TODO:
    Three stage Dividend Discount
 ''' 