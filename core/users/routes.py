from fastapi import APIRouter, Path, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from users.models import UserModel, TokenModel
from users.schemas import *
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
import secrets
from auth.jwt_auth import generate_access_token, generate_refresh_token, decode_refresh_token

router = APIRouter(tags=["users"],prefix="/users")

def generate_token(length=32):
    return secrets.token_hex(length)


@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    
    user_obj = db.query(UserModel).filter_by(username=request.username).first()
    if not db.query(UserModel).filter_by(username=request.username).first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user_obj.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    return JSONResponse(content={"detail": "Logged in successfully",
     "access_token": access_token, "refresh_token": refresh_token})

@router.post("/register")
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=request.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    user_obj = UserModel(username=request.username.lower())
    try:
        user_obj.set_password(request.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    db.add(user_obj)
    db.commit()
    return JSONResponse(content={"message": "User created successfully"})


@router.post("/refresh-token")
async def user_refresh_token(request: UserRefreshTokenSchema, db: Session = Depends(get_db)):
    user_id = decode_refresh_token(request.token)
    access_token = generate_access_token(user_id)
    return JSONResponse(content={"access_token": access_token})