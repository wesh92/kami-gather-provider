from pydantic import BaseModel, Field


class MarketRawResponse(BaseModel):
    item_id: int = Field(..., description="Item ID")
    current_stock: int = Field(..., description="Current stock")
    total_trades: int = Field(..., description="Total trades")
    base_price: int = Field(..., description="Base price")

class GetWorldMarketListRawResponse(MarketRawResponse):
    ...

    class Config:
        arbitrary_types_allowed = True
        optional_sub_category = True

class GetWorldMarketSubListRawResponse(MarketRawResponse):
    enhancement_range_min: int = Field(..., description="Minimum enhancement level")
    enhancement_range_max: int = Field(..., description="Maximum enhancement level")
    price_hard_cap_min: int = Field(..., description="Minimum price hard cap")
    price_hard_cap_max: int = Field(..., description="Maximum price hard cap")
    last_sale_price: int = Field(..., description="Last sale price")
    last_sale_time: int = Field(..., description="Last sale timestamp (Unix)")

class GetWorldMarketSearchListRawResponse(MarketRawResponse):
    ...

class GetBiddingInfoListRawResponse(BaseModel):
    # field name: index id
    price: int = Field(..., description="Price")
    amount_of_sell_orders: int = Field(..., description="Amount of sell orders")
    amount_of_buy_orders: int = Field(..., description="Amount of purchase orders")
    
    class Config:
        arbitrary_types_allowed = True
        optional_sub_category = True

class GetMarketPriceInfoRawResponse(BaseModel):
    ninety_day_prices: list[int] = Field(0, description="List of prices for the last 90 days")

    class Config:
        arbitrary_types_allowed = True
