from pydantic import BaseModel, Field
import pendulum


class MarketBaseModel(BaseModel):
    processed_at: str = Field(default_factory=lambda: pendulum.now().to_iso8601_string(), description="Processed at (ISO 8601 datetime)")

class WorldMarketListResponse(MarketBaseModel):
    item_id: int = Field(..., description="Item ID")
    current_stock: int = Field(..., description="Current stock")
    total_trades: int = Field(..., description="Total trades")
    base_price: int = Field(..., description="Base price")

class WorldMarketSubListResponse(MarketBaseModel):
    item_id: int = Field(..., description="Item ID")
    enhancement_range: tuple[int, int] = Field(..., description="Enhancement range (min, max)")
    base_price: int = Field(..., description="Base price")
    current_stock: int = Field(..., description="Current stock")
    total_trades: int = Field(..., description="Total trades")
    price_hard_cap: tuple[int, int] = Field(..., description="Price hard cap (min, max)")
    last_sale_price: int = Field(..., description="Last sale price")
    last_sale_time: int = Field(..., description="Last sale time (UNIX timestamp)")
    
    @validator('enhancement_range', pre=True)
    def max_enhancement_range_less_than_20(cls, v):
        if v[1] >= 20:
            raise ValueError("Max enhancement range must be less than 20")
        return v
