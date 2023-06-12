import logging
import pathlib
from abc import ABC, abstractmethod
from logging import info

import polars as pl
import sqlalchemy
import toml

from .configs.config import LOCALES
from .market_collector import MarketData
from .models.market_models import WorldMarketListResponse


# Base strategy interface
class MarketDataStrategy(ABC):
    @abstractmethod
    def parse_data(self, main_category: int = None, sub_category: int = None) -> list:
        pass

    @abstractmethod
    def update_market_data(
        self, main_categories: dict = None, table_name: str = None
    ) -> None:
        ...


# Strategy for handling market data
class WorldMarketDataStrategy(MarketDataStrategy):
    def parse_data(
        self, main_category: int = None, sub_category: int = None
    ) -> list[WorldMarketListResponse]:
        mkt = MarketData(regions=LOCALES, endpoint_names=["get_world_market_list"])
        request_data = {
            "keyType": 0,
            "mainCategory": main_category,
            "subCategory": sub_category,
        }
        try:
            data = mkt.get_data(request_data)
        except Exception as e:  # noqa: BLE001
            logging.error(f"Error getting data: {e}")
            return []

        parsed_listings = []
        for region in LOCALES:
            result_msg = data[region]
            listing = result_msg.split("|")
            for field in listing:
                fields = field.split("-")
                if fields[0]:
                    valid_field = WorldMarketListResponse(
                        item_id=int(fields[0]),
                        item_main_category=main_category,
                        item_sub_category=sub_category,
                        current_stock=int(fields[1]),
                        total_trades=int(fields[2]),
                        base_price=int(fields[3]),
                        region=region,
                    )
                    parsed_listings.append(valid_field)
        return parsed_listings

    def update_market_data(
        self, main_categories: dict = None, table_name: str = None
    ) -> None:
        CONFIG_FILE = (  # noqa: N806
            pathlib.Path(__file__).parent.parent / "src" / "configs" / "secrets.toml"
        )
        with open(CONFIG_FILE) as file:
            CONFIG = toml.load(file)  # noqa: N806

        PG_USER = CONFIG["bdo_data_postgresql"]["username"]  # noqa: N806
        PG_PASSWORD = CONFIG["bdo_data_postgresql"]["password"]  # noqa: N806
        PG_DB = CONFIG["bdo_data_postgresql"]["database"]  # noqa: N806
        ENGINE_STRING = sqlalchemy.create_engine(  # noqa: N806
            f"postgresql://{PG_USER}:{PG_PASSWORD}@postgres-data-postgresql:5432/{PG_DB}"
        ).url

        if table_name is None:
            table_name = CONFIG["bdo_data_postgresql"]["tables"]["world_market_table"]

        if main_categories is not None:
            for main_category, details in main_categories.items():
                sub_categories = details[1]
                for sub_category in sub_categories:
                    market_data = self.parse_data(
                        main_category=int(main_category), sub_category=int(sub_category)
                    )
                    data_dicts = [listing.dict() for listing in market_data]
                    market_df = pl.DataFrame(data_dicts)
                    try:
                        market_df.write_database(
                            table_name=table_name,
                            connection_uri=ENGINE_STRING,
                            if_exists="append",
                        )
                    except ValueError as e:
                        logging.error(f"Error writing to database: {e}")
                        continue

        info("Done!")
