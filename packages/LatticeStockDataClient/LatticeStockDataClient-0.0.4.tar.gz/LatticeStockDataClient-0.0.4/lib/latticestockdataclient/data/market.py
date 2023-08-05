from cachetools.func import ttl_cache
from latticestockdataclient.util.ttlcache import daily_cache
from latticestockdataclient.util.LatticeStockDataAccessor import LatticeStockDataAccessor


@daily_cache
def s_and_p_composition():
    return get_json("/market/index/s-and-p-composition")["stocks"]

@daily_cache
def nasdaq_composition():
    return get_json("/market/index/nasdaq-composition")["stocks"]

@daily_cache
def dji_composition():
    return get_json("/market/index/dji-composition")["stocks"]

@daily_cache
def russel_one_thousand_composition():
    return get_json("/market/index/russel-one-thousand-composition")["stocks"]

@daily_cache
def nyse_composition():
    return get_json("/market/exchange/nyse-composition")["stocks"]

@daily_cache
def nasdaq_exchange_composition():
    return get_json("/market/exchange/nasdaq-exchange-composition")["stocks"]

@daily_cache
def all_public_companies():
    return get_json("/market/all-public-companies")["stocks"]
