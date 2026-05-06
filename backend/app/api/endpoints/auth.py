"""
인증 관련 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...schemas.auth import SignupRequest, LoginRequest, TokenResponse
from ...services.auth_service import create_user, authenticate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    """회원가입"""
    try:
        user = create_user(db, req.username, req.email, req.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    from ...core.security import create_access_token
    token = create_access_token({"sub": str(user.id), "username": user.username})
    return TokenResponse(access_token=token, username=user.username)


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """로그인"""
    try:
        token = authenticate(db, req.username, req.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return TokenResponse(access_token=token, username=req.username)
