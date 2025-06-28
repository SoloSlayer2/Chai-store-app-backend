from app.controllers.user_controller import (
    login_user,
    logout_user,
    register_user,
    reset_password,
)
from app.db.setup_db import SessionLocal
from fastapi import APIRouter, Depends, Request
from app.schemas.UserSchema import ResetPasswordFormat, UserLoginOrRegisterSchema
from sqlalchemy.orm import Session

user_router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post("/register")
def register(credentials: UserLoginOrRegisterSchema, db: Session = Depends(get_db)):
    return register_user(credentials=credentials, db=db)


@user_router.post("/login")
def login(credentials: UserLoginOrRegisterSchema, db: Session = Depends(get_db)):
    return login_user(credentials=credentials, db=db)


@user_router.post("/reset-password")
def reset_pwd(credentials: ResetPasswordFormat, db: Session = Depends(get_db)):
    return reset_password(credentials=credentials, db=db)


@user_router.post("/logout")
def logout(req: Request, db: Session = Depends(get_db)):
    return logout_user(req=req, db=db)
