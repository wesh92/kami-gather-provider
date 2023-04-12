import requests
from config.config import LOCALES, MARKET_CATEGORIES, MarketEndpoint, entry_split, market_url_structure, property_split
from utils.unpack import unpack
import config.db_config as db_config

def get_urls(region=None, endpoint_name=None) -> list[str]:
    regions = LOCALES if region is None else [region]
    endpoints = list(MarketEndpoint) if endpoint_name is None else [MarketEndpoint[endpoint_name.upper()]]

    return [
        market_url_structure[r][e.name]
        for r in regions
        for e in endpoints
    ]
headers = {
    "Content-Type": "application/json",
    "User-Agent": "BlackDesert",
}
data = {
    "keyType": 0,
    "mainCategory": 1,
    "subCategory": 1
}

response = requests.post(url, headers=headers, json=data)
print(unpack(response.content))
