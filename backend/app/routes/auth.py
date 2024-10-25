from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserUpdate, LoginSchema, RefreshTokenRequest
from app.crud.user import CRUDUser
from app.services.auth import verify_password, create_access_token, create_refresh_token, decode_token
from app.database import get_db
from app.dependencies.user import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = await CRUDUser.get_user_by_email(db, user.email)
    if db_user:
        print(db_user)
        raise HTTPException(status_code=400, detail="Email already registered")
    return await CRUDUser.create_user(db, user)

@router.post("/login")
async def login_user(login_data: LoginSchema, db: Session = Depends(get_db)):
    db_user = await CRUDUser.get_user_by_email(db, login_data.email)
    if not db_user or not verify_password(login_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest):
    payload = decode_token(request.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    new_access_token = create_access_token({"sub": payload["sub"]})
    return {"access_token": new_access_token}
