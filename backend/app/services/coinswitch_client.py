import json
import time
from urllib.parse import urlencode, unquote_plus

import httpx
from cryptography.hazmat.primitives.asymmetric import ed25519

from app.core.config import settings


class CoinSwitchClient:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key

    def _private_key(self) -> ed25519.Ed25519PrivateKey:
        return ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(self.secret_key))

    def _sign_get(self, endpoint: str, params: dict) -> tuple[str, str, str]:
        epoch_time = str(int(time.time() * 1000))
        full_endpoint = endpoint if not params else f"{endpoint}?{urlencode(params)}"
        message = "GET" + unquote_plus(full_endpoint) + epoch_time
        signature = self._private_key().sign(message.encode()).hex()
        return signature, epoch_time, full_endpoint

    def _sign_json(self, method: str, endpoint: str, payload: dict) -> str:
        message = method.upper() + endpoint + json.dumps(payload, separators=(",", ":"), sort_keys=True)
        return self._private_key().sign(message.encode()).hex()

    async def _request(self, method: str, endpoint: str, payload: dict | None = None, params: dict | None = None) -> dict:
        payload = payload or {}
        params = params or {}
        headers = {"Content-Type": "application/json", "X-AUTH-APIKEY": self.api_key}

        if method.upper() == "GET":
            signature, epoch_time, signed_endpoint = self._sign_get(endpoint, params)
            headers["X-AUTH-SIGNATURE"] = signature
            headers["X-AUTH-EPOCH"] = epoch_time
            url = f"{settings.coinswitch_base_url}{signed_endpoint}"
            request_kwargs = {"headers": headers}
        else:
            headers["X-AUTH-SIGNATURE"] = self._sign_json(method, endpoint, payload)
            url = f"{settings.coinswitch_base_url}{endpoint}"
            request_kwargs = {"headers": headers, "json": payload}

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.request(method.upper(), url, **request_kwargs)

        try:
            data = response.json()
        except Exception:
            data = {"message": response.text}

        if response.status_code >= 400:
            raise ValueError(data.get("message", "CoinSwitch request failed"))
        return data

    async def validate_keys(self) -> bool:
        data = await self._request("GET", "/trade/api/v2/validate/keys")
        return data.get("message") == "Valid Access"

    async def get_portfolio(self) -> dict:
        return await self._request("GET", "/trade/api/v2/user/portfolio")

    async def get_orders(self, open_orders: bool) -> dict:
        return await self._request("GET", "/trade/api/v2/orders", params={"open": str(open_orders).lower(), "count": 20})

    async def create_order(self, *, symbol: str, side: str, price: float, quantity: float, exchange: str, order_type: str) -> dict:
        payload = {
            "side": side.lower(),
            "symbol": symbol.upper(),
            "type": order_type.lower(),
            "price": price,
            "quantity": quantity,
            "exchange": exchange.lower(),
        }
        return await self._request("POST", "/trade/api/v2/order", payload=payload)
