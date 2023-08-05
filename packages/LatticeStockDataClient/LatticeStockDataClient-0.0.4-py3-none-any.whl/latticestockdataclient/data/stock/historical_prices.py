from data.stockmarket.util.get import get_df
from data.stockmarket.util.ttlcache import hourly_cache


@hourly_cache
def historical_prices(ticker_symbol, years=5):
    params = {"ticker_symbol": ticker_symbol, "years": years, "format": "csv"}
    return get_df("/stock/historical-prices", params)

