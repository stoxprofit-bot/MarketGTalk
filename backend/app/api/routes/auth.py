from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.mongodb import get_db
from app.models.common import object_id_str, utc_now
from app.schemas.auth import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
async def signup(payload: UserCreate):
    db = get_db()
    existing_user = await db.users.find_one({"email": payload.email.lower()})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = "admin" if payload.email.lower() in settings.admin_email_list else "user"
    user_doc = {
        "email": payload.email.lower(),
        "full_name": payload.full_name,
        "hashed_password": get_password_hash(payload.password),
        "role": role,
        "max_trade_size": 1000.0,
        "created_at": utc_now(),
    }
    result = await db.users.insert_one(user_doc)
    return TokenResponse(access_token=create_access_token(str(result.inserted_id)))


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin):
    user = await get_db().users.find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(str(user["_id"])))


@router.get("/me", response_model=UserResponse)
async def me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=object_id_str(current_user["_id"]),
        email=current_user["email"],
        full_name=current_user["full_name"],
        role=current_user["role"],
        max_trade_size=current_user.get("max_trade_size", 0),
    )


@router.patch("/risk-limit", response_model=UserResponse)
async def update_risk_limit(max_trade_size: float, current_user: dict = Depends(get_current_user)):
    if max_trade_size <= 0:
        raise HTTPException(status_code=400, detail="Max trade size must be positive")
    await get_db().users.update_one({"_id": current_user["_id"]}, {"$set": {"max_trade_size": max_trade_size}})
    current_user["max_trade_size"] = max_trade_size
    return await me(current_user)
