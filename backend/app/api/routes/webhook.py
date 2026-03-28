from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.db.mongodb import get_db
from app.models.common import object_id_str, utc_now
from app.schemas.signals import TradingViewWebhookPayload
from app.services.trading_engine import execute_signal_for_all_users

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/tradingview")
async def tradingview_webhook(payload: TradingViewWebhookPayload):
    db = get_db()
    if payload.secret != settings.tradingview_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid TradingView secret")

    signal_doc = {
        "created_by": None,
        "source": "tradingview",
        "symbol": payload.symbol.upper(),
        "side": payload.side.lower(),
        "price": payload.price,
        "quantity": payload.quantity,
        "exchange": (payload.exchange or settings.default_exchange).lower(),
        "order_type": settings.default_order_type,
        "note": payload.note,
        "created_at": utc_now(),
        "executed_users": 0,
        "success_count": 0,
    }
    result = await db.signals.insert_one(signal_doc)
    signal_doc["_id"] = result.inserted_id
    trades = await execute_signal_for_all_users(signal_doc)
    return {
        "message": "Webhook processed",
        "signal_id": object_id_str(result.inserted_id),
        "executed_users": len(trades),
        "success_count": len([trade for trade in trades if trade["status"] == "submitted"]),
    }
