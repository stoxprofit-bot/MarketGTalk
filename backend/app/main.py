from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, coinswitch, dashboard, signals, webhook
from app.db import mongodb
from app.core.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    await mongodb.connect_to_mongo()
    database = mongodb.get_db()
    await database.users.create_index("email", unique=True)
    await database.credentials.create_index("user_id", unique=True)
    await database.trades.create_index("user_id")
    await database.trades.create_index("signal_id")
    await database.signals.create_index("created_at")
    yield
    await mongodb.close_mongo_connection()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(coinswitch.router, prefix=settings.api_v1_prefix)
app.include_router(dashboard.router, prefix=settings.api_v1_prefix)
app.include_router(signals.router, prefix=settings.api_v1_prefix)
app.include_router(webhook.router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    return {"message": "Copy trading backend is running"}
