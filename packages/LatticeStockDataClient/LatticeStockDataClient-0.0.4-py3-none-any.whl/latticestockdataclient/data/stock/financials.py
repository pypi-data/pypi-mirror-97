from cachetools.func import ttl_cache
from data.stockmarket.util.get import get_json, get_df
from data.stockmarket.util.ttlcache import daily_cache


## Basics #############################################################################################################################################

@daily_cache
def annual_balance_sheet(ticker_symbol):
    return get_df("/stock/financials/balance-sheet/annual", {"ticker_symbol": ticker_symbol})

@daily_cache
def quarterly_balance_sheet(ticker_symbol):
    return get_df("/stock/financials/balance-sheet/quarterly", {"ticker_symbol": ticker_symbol})

@daily_cache
def current_annual_balance_sheet(ticker_symbol):
    return get_json("/stock/financials/balance-sheet/current-annual", {"ticker_symbol": ticker_symbol})

@daily_cache
def current_quarterly_balance_sheet(ticker_symbol):
    return get_json("/stock/financials/balance-sheet/current-quarterly", {"ticker_symbol": ticker_symbol})

@daily_cache
def annual_income_statement(ticker_symbol):
    return get_df("/stock/financials/income-statement/annual", {"ticker_symbol": ticker_symbol})

@daily_cache
def quarterly_income_statement(ticker_symbol):
    return get_df("/stock/financials/income-statement/quarterly", {"ticker_symbol": ticker_symbol})

@daily_cache
def current_annual_income_statement(ticker_symbol):
    return get_json("/stock/financials/income-statement/current-annual", {"ticker_symbol": ticker_symbol})

@daily_cache
def current_quarterly_income_statement(ticker_symbol):
    return get_json("/stock/financials/income-statement/current-quarterly", {"ticker_symbol": ticker_symbol})


## Income statement line items ########################################################################################################################

def revenue(ticker_symbol):
    return current_annual_income_statement(ticker_symbol).get("Total Revenue", 0.0)

def gross_profit(ticker_symbol):
    return current_annual_income_statement(ticker_symbol).get("Gross Profit", 0.0)

def yoy_revenue_growth(ticker_symbol):
    prev_revenue = previous_annual_income_statement(ticker_symbol).get("Total Revenue", 0.0)
    return (revenue(ticker_symbol) - prev_revenue) / prev_revenue

def yoy_gross_profit_growth(ticker_symbol):
    prev_revenue = previous_annual_income_statement(ticker_symbol).get("Gross Profit", 0.0)
    return (gross_profit(ticker_symbol) - prev_revenue) / prev_revenue

