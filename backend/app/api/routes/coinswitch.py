from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.db.mongodb import get_db
from app.schemas.coinswitch import CoinSwitchConnectRequest, CoinSwitchStatusResponse
from app.services.coinswitch_client import CoinSwitchClient
from app.services.deps import get_current_user
from app.services.encryption import encrypt_secret

router = APIRouter(prefix="/coinswitch", tags=["coinswitch"])


@router.post("/connect", response_model=CoinSwitchStatusResponse)
async def connect_coinswitch(payload: CoinSwitchConnectRequest, current_user: dict = Depends(get_current_user)):
    db = get_db()
    client = CoinSwitchClient(payload.api_key, payload.secret_key)
    try:
        validated = await client.validate_keys()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"CoinSwitch validation failed: {exc}") from exc

    exchange = payload.exchange or settings.default_exchange
    await db.credentials.update_one(
        {"user_id": current_user["_id"]},
        {
            "$set": {
                "user_id": current_user["_id"],
                "api_key": payload.api_key,
                "secret_key_encrypted": encrypt_secret(payload.secret_key),
                "exchange": exchange,
            }
        },
        upsert=True,
    )
    return CoinSwitchStatusResponse(connected=True, exchange=exchange, validated=validated)


@router.get("/status", response_model=CoinSwitchStatusResponse)
async def coinswitch_status(current_user: dict = Depends(get_current_user)):
    credential = await get_db().credentials.find_one({"user_id": current_user["_id"]})
    if not credential:
        return CoinSwitchStatusResponse(connected=False)
    return CoinSwitchStatusResponse(connected=True, exchange=credential.get("exchange"), validated=True)
