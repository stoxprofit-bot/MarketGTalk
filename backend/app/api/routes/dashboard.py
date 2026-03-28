from fastapi import APIRouter, Depends

from app.db.mongodb import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.coinswitch_client import CoinSwitchClient
from app.services.deps import get_current_user
from app.services.encryption import decrypt_secret
from app.services.trading_engine import serialize_trade

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardResponse)
async def summary(current_user: dict = Depends(get_current_user)):
    db = get_db()
    credential = await db.credentials.find_one({"user_id": current_user["_id"]})
    portfolio = []
    connected_exchange = None

    if credential:
        connected_exchange = credential.get("exchange")
        client = CoinSwitchClient(credential["api_key"], decrypt_secret(credential["secret_key_encrypted"]))
        try:
            portfolio_response = await client.get_portfolio()
            portfolio = portfolio_response.get("data", [])
        except Exception:
            portfolio = []

    recent_trade_docs = await db.trades.find({"user_id": current_user["_id"]}).sort("created_at", -1).to_list(10)
    total_trades = await db.trades.count_documents({"user_id": current_user["_id"]})
    submitted_count = await db.trades.count_documents({"user_id": current_user["_id"], "status": "submitted"})
    pnl = sum(((item.get("response") or {}).get("data") or {}).get("realised_pnl", 0) for item in recent_trade_docs)

    balance = 0.0
    for item in portfolio:
        current_value = item.get("current_value")
        if current_value is not None:
            balance += float(current_value)
        elif item.get("main_balance") is not None and item.get("currency") == "INR":
            balance += float(item["main_balance"])

    return DashboardResponse(
        balance=round(balance, 2),
        pnl=round(float(pnl), 2),
        total_trades=total_trades,
        win_rate=round((submitted_count / total_trades) * 100, 2) if total_trades else 0,
        connected_exchange=connected_exchange,
        portfolio=portfolio,
        recent_trades=[serialize_trade(trade) for trade in recent_trade_docs],
    )


@router.get("/trades")
async def list_trades(current_user: dict = Depends(get_current_user)):
    trade_docs = await get_db().trades.find({"user_id": current_user["_id"]}).sort("created_at", -1).to_list(100)
    return [serialize_trade(trade) for trade in trade_docs]
