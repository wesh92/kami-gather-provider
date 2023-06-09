import pendulum
from pydantic import BaseModel, Field, validator


class MarketBaseModel(BaseModel):
    processed_at: pendulum.DateTime = Field(
        default_factory=lambda: pendulum.now(),
        description="Processed at (ISO 8601 datetime)",
    )
    region: str = Field(..., description="Regional ID")


class WorldMarketListResponse(MarketBaseModel):
    item_id: int = Field(..., description="Item ID")
    item_main_category: int = Field(
        ..., description="Item main category integer identifier"
    )
    item_sub_category: int = Field(
        ..., description="Item sub category integer identifier"
    )
    current_stock: int = Field(..., description="Current stock")
    total_trades: int = Field(..., description="Total trades")
    base_price: int = Field(..., description="Base price")


class WorldMarketSubListResponse(MarketBaseModel):
    item_id: int = Field(..., description="Item ID")
    enhancement_range: tuple[int, int] = Field(
        ..., description="Enhancement range (min, max)"
    )
    base_price: int = Field(..., description="Base price")
    current_stock: int = Field(..., description="Current stock")
    total_trades: int = Field(..., description="Total trades")
    price_hard_cap: tuple[int, int] = Field(
        ..., description="Price hard cap (min, max)"
    )
    last_sale_price: int = Field(..., description="Last sale price")
    last_sale_time: int = Field(..., description="Last sale time (UNIX timestamp)")

    @validator("enhancement_range", pre=True)
    def max_enhancement_range_less_than_20(cls, v):  # noqa: ANN201
        if v[1] >= 20:
            raise ValueError("Max enhancement range must be less than 20")
        return v
