from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.user import CRUDUser
from app.services.auth import decode_token
from app.schemas.user import UserResponse
from fastapi.security import OAuth2PasswordBearer

# Define OAuth2PasswordBearer for getting the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await CRUDUser.get_user_by_email(db, payload["sub"])
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.from_orm(user)
