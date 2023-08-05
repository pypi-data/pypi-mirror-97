from cachetools.func import ttl_cache
from data.stockmarket.util.get import get_json, get_df
from data.stockmarket.util.ttlcache import hourly_cache


@hourly_cache
def cost_of_equity(ticker_symbol):
    return get_json("/stock/valuation/cost-of-equity", {"ticker_symbol": ticker_symbol})["cost_of_equity"]

@hourly_cache
def enterprise_value(ticker_symbol):
    return get_json("/stock/valuation/enterprise-value", {"ticker_symbol": ticker_symbol})["enterprise_value"]

@hourly_cache
def historical_valuation_measures_table(ticker_symbol):
    return get_df("/stock/valuation/historical-valuation-measures", {"ticker_symbol": ticker_symbol})

@hourly_cache
def current_valuation_measures(ticker_symbol):
    return get_json("/stock/valuation/valuation-measures", {"ticker_symbol": ticker_symbol})

def forward_pe(ticker_symbol):
    return current_valuation_measures(ticker_symbol)["Forward P/E"]

def trailing_pe(ticker_symbol):
    return current_valuation_measures(ticker_symbol)["Trailing P/E"]

def market_cap(ticker_symbol):
    return current_valuation_measures(ticker_symbol)["Market Cap (intraday)"]

