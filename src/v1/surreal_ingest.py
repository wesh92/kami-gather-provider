import pathlib
from abc import ABC, abstractmethod
from logging import addLevelName, log

import toml
from collect import MarketData
from config.config import LOCALES
from data_models.market_reponse_models import WorldMarketListResponse
from surrealdb import Surreal

addLevelName(31, "SURREAL_INFO")

with open(pathlib.Path(__file__).parent / 'config' / '.secrets.toml') as f: # Path to secrets file /config/.secrets.toml
    secrets = toml.load(f)

# Base strategy interface
class DataStrategy(ABC):
    @abstractmethod
    def parse_data(self, main_category: int = None, sub_category: int = None, item_number: list[int] = None) -> list:
        pass

    @abstractmethod
    async def insert_data(self, records) -> None:
        pass

# Strategy for handling market data
class WorldMarketDataStrategy(DataStrategy):
    def parse_data(self, main_category: int = None, sub_category: int = None, item_number: list[int] = None) -> list[WorldMarketListResponse]:
        mkt = MarketData(regions=LOCALES, endpoint_names=["get_world_market_list"])
        request_data = {
            "keyType": 0,
            "mainCategory": main_category,
            "subCategory": sub_category
        }
        data = mkt.get_data(request_data)
        parsed_listings = []
        for region in LOCALES:
            result_msg = data[region]
            listing = result_msg.split('|')
            for field in listing:
                fields = field.split('-')
                if fields[0]:
                    valid_field = WorldMarketListResponse(
                        item_id=int(fields[0]),
                        current_stock=int(fields[1]),
                        total_trades=int(fields[2]),
                        base_price=int(fields[3])
                    )
                    parsed_listings.append(valid_field)
        return parsed_listings


    async def insert_data(self, records: list[WorldMarketListResponse]) -> None:
        # Inserting logic for market_data, e.g., using the previous SurrealDB example
        async with Surreal("ws://localhost:8000/rpc") as db:
            await db.signin({"user": secrets["DB_USER"], "pass": secrets["DB_PASS"]})
            await db.use("bdo", "market_data")
            for record in records:
                await db.create(
                    "world_market_list",
                    {
                        "item_id": record.item_id,
                        "current_stock": record.current_stock,
                        "total_trades": record.total_trades,
                        "base_price": record.base_price,
                        "processed_at": record.processed_at,
                    },
                )
        log(31, f"Market data inserted successfully. Inserted {len(records)} records.")



# async def main():
#     """Example of how to use the SurrealDB client."""
#     async with Surreal("ws://localhost:8000/rpc") as db:
#         await db.signin({"user": secrets["DB_USER"], "pass": secrets["DB_PASS"]})
#         await db.use("test", "test")
#         await db.create(
#             "person",
#             {
#                 "user": "me",
#                 "pass": "safe",
#                 "marketing": True,
#                 "tags": ["python", "documentation"],
#             },
#         )
#         print(await db.select("person"))
#         print(await db.delete("person"))



if __name__ == "__main__":
    import asyncio
    a = WorldMarketDataStrategy()
    asyncio.run(a.insert_data(a.parse_data(main_category=5, sub_category=1)))