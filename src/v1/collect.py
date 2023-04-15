from dataclasses import dataclass
from logging import log

import requests
from config.config import LOCALES, MarketEndpoint, market_url_structure
from utils.unpack import unpack


@dataclass
class MarketData:
    regions: list[str] = None
    endpoint_names: list[str] = None

    def get_urls(self) -> list[tuple[str, str]]:
        regions = LOCALES if self.regions is None else self.regions
        endpoints = (
            list(MarketEndpoint)
            if self.endpoint_names is None
            else [MarketEndpoint[endpoint_names.upper()] for endpoint_names in self.endpoint_names]
        )

        return [(r, market_url_structure[r][e.name]) for r in regions for e in endpoints]

    def get_data(self, request_data: dict) -> dict:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "BlackDesert",
        }

        region_data = {}
        for region, url in self.get_urls():
            log(f"Requesting {region} market data...")
            response = requests.post(url, headers=headers, json=request_data, timeout=300)
            region_data[region] = unpack(response.content)

        return region_data
