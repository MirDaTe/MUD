"""인증 서비스"""
from sqlalchemy.orm import Session
from ..models.user import User
from ..core.security import hash_password, verify_password, create_access_token


def create_user(db: Session, username: str, email: str, password: str) -> User:
    if db.query(User).filter(User.username == username).first():
        raise ValueError("이미 존재하는 이름입니다.")
    if db.query(User).filter(User.email == email).first():
        raise ValueError("이미 등록된 이메일입니다.")
    user = User(username=username, email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, username: str, password: str) -> str:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("이름 또는 비밀번호가 틀렸습니다.")
    return create_access_token({"sub": str(user.id), "username": user.username})
