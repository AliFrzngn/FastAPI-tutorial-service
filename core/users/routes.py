from fastapi import APIRouter, Path, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from users.models import *
from users.schemas import *
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List

router = APIRouter(tags=["users"],prefix="/users")

@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=request.username).first()
    if not db.query(UserModel).filter_by(username=request.username).first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not user_obj.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return JSONResponse(content={"message": "User logged in successfully"})

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