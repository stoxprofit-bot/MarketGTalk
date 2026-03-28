from app.core.config import settings
from app.db.mongodb import get_db
from app.models.common import object_id_str, utc_now
from app.services.coinswitch_client import CoinSwitchClient
from app.services.encryption import decrypt_secret


def clamp_quantity(price: float, requested_quantity: float, max_trade_size: float) -> float:
    if price <= 0:
        return requested_quantity
    max_quantity = max_trade_size / price
    return round(min(requested_quantity, max_quantity), 8)


async def execute_signal_for_all_users(signal: dict) -> list[dict]:
    results = []
    database = get_db()
    async for credential in database.credentials.find({}):
        user = await database.users.find_one({"_id": credential["user_id"]})
        if not user:
            continue

        quantity = clamp_quantity(signal["price"], signal["quantity"], user.get("max_trade_size", 0))
        trade_doc = {
            "user_id": user["_id"],
            "signal_id": signal["_id"],
            "symbol": signal["symbol"],
            "side": signal["side"],
            "exchange": credential.get("exchange", settings.default_exchange),
            "price": signal["price"],
            "requested_quantity": signal["quantity"],
            "quantity": quantity,
            "status": "skipped" if quantity <= 0 else "pending",
            "order_id": None,
            "response": None,
            "error": None,
            "created_at": utc_now(),
        }

        if quantity <= 0:
            trade_doc["error"] = "Trade blocked by user risk limit"
            await database.trades.insert_one(trade_doc)
            results.append(trade_doc)
            continue

        client = CoinSwitchClient(credential["api_key"], decrypt_secret(credential["secret_key_encrypted"]))
        try:
            response = await client.create_order(
                symbol=signal["symbol"],
                side=signal["side"],
                price=signal["price"],
                quantity=quantity,
                exchange=credential.get("exchange", settings.default_exchange),
                order_type=signal.get("order_type", settings.default_order_type),
            )
            trade_doc["status"] = "submitted"
            trade_doc["response"] = response
            trade_doc["order_id"] = (response.get("data") or {}).get("order_id")
        except Exception as exc:
            trade_doc["status"] = "failed"
            trade_doc["error"] = str(exc)

        await database.trades.insert_one(trade_doc)
        results.append(trade_doc)

    await database.signals.update_one(
        {"_id": signal["_id"]},
        {"$set": {"executed_users": len(results), "success_count": len([t for t in results if t["status"] == "submitted"])}},
    )
    return results


def serialize_trade(trade: dict) -> dict:
    return {
        "id": object_id_str(trade.get("_id")),
        "signal_id": object_id_str(trade.get("signal_id")),
        "symbol": trade["symbol"],
        "side": trade["side"],
        "exchange": trade["exchange"],
        "status": trade["status"],
        "quantity": trade["quantity"],
        "price": trade["price"],
        "order_id": trade.get("order_id"),
        "error": trade.get("error"),
        "created_at": trade["created_at"].isoformat(),
    }
