from pydantic import BaseModel


class TradeItem(BaseModel):
    id: str
    signal_id: str | None = None
    symbol: str
    side: str
    exchange: str
    status: str
    quantity: float
    price: float
    order_id: str | None = None
    error: str | None = None
    created_at: str


class DashboardResponse(BaseModel):
    balance: float
    pnl: float
    total_trades: int
    win_rate: float
    connected_exchange: str | None
    portfolio: list[dict]
    recent_trades: list[TradeItem]
