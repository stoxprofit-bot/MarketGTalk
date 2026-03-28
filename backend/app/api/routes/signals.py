from fastapi import APIRouter, Depends

from app.core.config import settings
from app.db.mongodb import get_db
from app.models.common import object_id_str, utc_now
from app.schemas.signals import SignalCreate
from app.services.deps import get_admin_user
from app.services.trading_engine import execute_signal_for_all_users

router = APIRouter(prefix="/signals", tags=["signals"])


@router.post("/manual")
async def create_manual_signal(payload: SignalCreate, admin_user: dict = Depends(get_admin_user)):
    db = get_db()
    signal_doc = {
        "created_by": admin_user["_id"],
        "source": "admin",
        "symbol": payload.symbol.upper(),
        "side": payload.side.lower(),
        "price": payload.price,
        "quantity": payload.quantity,
        "exchange": (payload.exchange or settings.default_exchange).lower(),
        "order_type": payload.order_type.lower(),
        "note": payload.note,
        "created_at": utc_now(),
        "executed_users": 0,
        "success_count": 0,
    }
    result = await db.signals.insert_one(signal_doc)
    signal_doc["_id"] = result.inserted_id
    trades = await execute_signal_for_all_users(signal_doc)
    return {
        "signal_id": object_id_str(result.inserted_id),
        "executed_users": len(trades),
        "success_count": len([trade for trade in trades if trade["status"] == "submitted"]),
    }


@router.get("/history")
async def signal_history(admin_user: dict = Depends(get_admin_user)):
    signal_docs = await get_db().signals.find({}).sort("created_at", -1).to_list(50)
    return [
        {
            "id": object_id_str(signal["_id"]),
            "symbol": signal["symbol"],
            "side": signal["side"],
            "price": signal["price"],
            "quantity": signal["quantity"],
            "exchange": signal["exchange"],
            "source": signal["source"],
            "executed_users": signal.get("executed_users", 0),
            "success_count": signal.get("success_count", 0),
            "created_at": signal["created_at"].isoformat(),
        }
        for signal in signal_docs
    ]
