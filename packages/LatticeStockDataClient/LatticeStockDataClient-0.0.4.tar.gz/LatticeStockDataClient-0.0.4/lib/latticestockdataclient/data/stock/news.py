from cachetools.func import ttl_cache
from data.stockmarket.util.get import get_json
from data.stockmarket.util.ttlcache import hourly_cache


@hourly_cache
def latest_company_news(ticker_symbol):
    return get_json("/stock/news", {"ticker_symbol": ticker_symbol})["articles"]

@hourly_cache
def latest_news_sentiment(ticker_symbol):
    return get_json("/stock/sentiment", {"ticker_symbol": ticker_symbol})["sentiment"]

