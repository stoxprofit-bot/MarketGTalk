from pydantic import BaseModel, Field


class CoinSwitchConnectRequest(BaseModel):
    api_key: str = Field(min_length=4)
    secret_key: str = Field(min_length=8)
    exchange: str | None = None


class CoinSwitchStatusResponse(BaseModel):
    connected: bool
    exchange: str | None = None
    validated: bool = False
