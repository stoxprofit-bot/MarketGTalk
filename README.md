# Crypto Copy Trading Platform

Full-stack crypto copy trading platform built with:

- React Native (Expo) mobile app
- FastAPI backend
- MongoDB database
- JWT authentication
- CoinSwitch API key connection
- Admin/manual signal broadcasting
- TradingView webhook ingestion
- Dashboard for balances, P&L, and recent trades
- Encrypted CoinSwitch secret-key storage
- User-level risk management with max trade size

## Project Structure

```text
backend/   FastAPI + MongoDB + CoinSwitch integration
mobile/    React Native Expo app
```

## Backend Setup

1. Create and activate a Python virtual environment inside `backend`.
2. Install dependencies:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`.
4. Generate an encryption key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

5. Put that value into `ENCRYPTION_KEY`.
6. Start MongoDB on `mongodb://localhost:27017`.
7. Run the backend:

```bash
uvicorn app.main:app --reload
```

Backend base URL: `http://localhost:8000`

## Mobile Setup

1. Configure `mobile/.env.example` as `.env`.
2. Update `EXPO_PUBLIC_API_URL` for your device/emulator.
3. Install dependencies and run:

```bash
cd mobile
npm install
npm start
```

Common API URLs:

- Android emulator: `http://10.0.2.2:8000/api/v1`
- iOS simulator: `http://localhost:8000/api/v1`
- Physical device: `http://YOUR_LOCAL_IP:8000/api/v1`

## First Admin User

Set `ADMIN_EMAILS=admin@example.com` in the backend `.env`.

When that email signs up, the backend assigns the `admin` role automatically. Admin users can broadcast manual copy-trade signals from the app.

## TradingView Webhook Example

POST to:

```text
http://YOUR_SERVER:8000/api/v1/webhooks/tradingview
```

Body:

```json
{
  "secret": "change-me",
  "symbol": "BTC/USDT",
  "side": "buy",
  "price": 64000,
  "quantity": 0.002,
  "exchange": "c2c1",
  "note": "EMA crossover"
}
```

## Core API Endpoints

- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `PATCH /api/v1/auth/risk-limit?max_trade_size=1000`
- `POST /api/v1/coinswitch/connect`
- `GET /api/v1/coinswitch/status`
- `GET /api/v1/dashboard/summary`
- `GET /api/v1/dashboard/trades`
- `POST /api/v1/signals/manual`
- `GET /api/v1/signals/history`
- `POST /api/v1/webhooks/tradingview`

## Security

- JWT auth for mobile and backend access
- `bcrypt` password hashing
- Fernet encryption for CoinSwitch secret keys at rest
- TradingView shared-secret validation
- Admin-only manual signal broadcast

## Risk Management

Each user stores a `max_trade_size` value. Before sending a copied trade, the backend caps the requested quantity:

```text
max_quantity = max_trade_size / price
final_quantity = min(signal_quantity, max_quantity)
```

If that final quantity is zero, the trade is skipped and recorded as blocked by risk limits.

## CoinSwitch Integration Notes

The backend client is based on the official CoinSwitch PRO V2 trading documentation at https://api-trading.coinswitch.co/, including Ed25519 request signing and `X-AUTH-APIKEY` / `X-AUTH-EPOCH` headers.

Implemented exchange calls:

- `GET /trade/api/v2/validate/keys`
- `GET /trade/api/v2/user/portfolio`
- `GET /trade/api/v2/orders`
- `POST /trade/api/v2/order`

## Production Hardening

- Restrict CORS in `backend/app/main.py`
- Move secrets to a managed secret store
- Add retries, rate-limit handling, and idempotency
- Add a background worker queue for large fan-out trade execution
- Add richer P&L reconciliation from fills and closed orders

## Important Assumptions

- This implementation uses limit orders for copy trading.
- CoinSwitch public docs contain minor signing-example inconsistencies across GET and POST examples; the backend follows the V2 pattern documented for key validation and order creation.
- Dashboard P&L is derived from locally stored recent trade responses plus live portfolio snapshots when available.
