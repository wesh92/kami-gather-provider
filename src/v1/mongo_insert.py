import asyncio
import pathlib
from abc import ABC, abstractmethod
from logging import addLevelName, log

import toml
from collect import MarketData
from config.config import LOCALES
from data_models.market_reponse_models import WorldMarketListResponse
from utils.mongo_service import mongo_connect

addLevelName(31, "MONGO_INFO")

with open(pathlib.Path(__file__).parent / "config" / ".secrets.toml") as f:  # Path to secrets file /config/.secrets.toml
    secrets = toml.load(f)


# Base strategy interface
class MarketDataStrategy(ABC):
    @abstractmethod
    def parse_data(
        self,
        main_category: int = None,
        sub_category: int = None,
        item_number: list[int] = None,
    ) -> list:
        pass

    @abstractmethod
    async def insert_market_data(
        self,
        records: list[WorldMarketListResponse],
        mongo_connection_string: str,
        mongo_db_name: str,
        mongo_collection_name: str,
    ) -> None:
        pass


# Strategy for handling market data
class WorldMarketDataStrategy(MarketDataStrategy):
    def parse_data(
        self,
        main_category: int = None,
        sub_category: int = None,
        item_number: list[int] = None,
    ) -> list[WorldMarketListResponse]:
        mkt = MarketData(regions=LOCALES, endpoint_names=["get_world_market_list"])
        request_data = {
            "keyType": 0,
            "mainCategory": main_category,
            "subCategory": sub_category,
        }
        data = mkt.get_data(request_data)
        parsed_listings = []
        for region in LOCALES:
            result_msg = data[region]
            listing = result_msg.split("|")
            for field in listing:
                fields = field.split("-")
                if fields[0]:
                    valid_field = WorldMarketListResponse(
                        item_id=int(fields[0]),
                        current_stock=int(fields[1]),
                        total_trades=int(fields[2]),
                        base_price=int(fields[3]),
                        region=region,
                    )
                    parsed_listings.append(valid_field)
        return parsed_listings

    async def insert_market_data(
        self,
        records: list[WorldMarketListResponse],
        mongo_connection_string: str,
        mongo_db_name: str,
        mongo_collection_name: str,
    ) -> None:
        connection = mongo_connect(mongo_connection_string)

        await connection[mongo_db_name][mongo_collection_name].insert_many([record.dict() for record in records])


async def main() -> None:
    connection_string = f"mongodb://{secrets['DB_USER']}:{secrets['DB_PASS']}@localhost:27017/?authMechanism=DEFAULT&tls=false"  # noqa: E501
    db_name = "bdo"
    collection_name = "market_list_data"
    strat = WorldMarketDataStrategy()
    market_data = strat.parse_data(main_category=1, sub_category=1)

    await strat.insert_market_data(
        records=market_data,
        mongo_connection_string=connection_string,
        mongo_db_name=db_name,
        mongo_collection_name=collection_name,
    )
    log(
        31,
        f"Market data inserted successfully. Inserted {len(market_data)} records.",
    )


if __name__ == "__main__":
    asyncio.run(main())
