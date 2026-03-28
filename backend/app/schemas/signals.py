from pydantic import BaseModel, Field


class SignalCreate(BaseModel):
    symbol: str = Field(description="Example: BTC/USDT")
    side: str = Field(description="buy or sell")
    price: float = Field(gt=0)
    quantity: float = Field(gt=0)
    exchange: str | None = None
    order_type: str = "limit"
    note: str | None = None


class TradingViewWebhookPayload(BaseModel):
    secret: str
    symbol: str
    side: str
    price: float = Field(gt=0)
    quantity: float = Field(gt=0)
    exchange: str | None = None
    note: str | None = None
