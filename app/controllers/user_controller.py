from uuid import UUID

from fastapi import Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.setup_db import SessionLocal
from app.models.chai_models import ChaiStore
from app.models.users_models import Users
from app.schemas.ChaiSchema import OrderChaiFormat
from app.schemas.UserSchema import (
    ResetPasswordFormat,
    UserLoginOrRegisterSchema,
    UserResponse,
)
from app.utils import ApiError, ApiResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generateRefreshAndAccessToken(userId: UUID, db: Session) -> dict:

    user = db.query(Users).filter(Users.id == userId).first()

    if not user:
        raise ApiError(message="User Not Found in Database", status_code=400)

    accessToken = user.generateAccessToken()
    refreshToken = user.generateRefreshToken()

    user.refresh_token = refreshToken
    db.commit()

    return {"at": accessToken, "rt": refreshToken}


def register_user(credentials: UserLoginOrRegisterSchema, db: Session) -> UserResponse:
    hashed_pwd = pwd_context.hash(credentials.password)

    new_user = Users(
        username=credentials.username,
        email=credentials.email,
        hashed_password=hashed_pwd,
    )

    username = new_user.username
    email = new_user.email

    checkUser1 = db.query(Users).filter(Users.username == username).first()
    checkUser2 = db.query(Users).filter(Users.email == email).first()

    if checkUser1:
        raise ApiError(message="Username not available! Please try another one")
    if checkUser2:
        raise ApiError(message="Email id linked to another account already present")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response = ApiResponse(
        status=200,
        message="User Created successful",
        data={
            "username": new_user.username,
            "email": new_user.email,
            "created_at": new_user.created_at,
        },
    )
    encoded_response = jsonable_encoder(response)
    fastapi_response = JSONResponse(content=encoded_response)
    return fastapi_response


def login_user(credentials: UserLoginOrRegisterSchema, db: Session) -> JSONResponse:
    new_user = Users(username=credentials.username, email=credentials.email)

    username = new_user.username
    email = new_user.email
    checkUser = (
        db.query(Users)
        .filter(or_(Users.username == username, Users.email == email))
        .first()
    )

    if not checkUser:
        raise ApiError(message="Username/Email is incorrect")

    # Check Password
    isPasswordValid = checkUser.isPasswordCorrect(credentials.password)

    if not isPasswordValid:
        raise ApiError(message="Password Incorrect")

    tokens = generateRefreshAndAccessToken(checkUser.id, db)
    access_token = tokens.get("at")
    refresh_token = tokens.get("rt")

    response = ApiResponse(status=200, message="Login successful", data={})
    fastapi_response = JSONResponse(
        content=jsonable_encoder(response)
    )  # model_dump() gives you a dictionary — great for Python. But jsonable_encoder() cleans that dictionary up so JSON can understand it.

    options = {
        "httponly": True,
        "secure": True,  # 🔒 only over HTTPS
        "samesite": "lax",
        "max_age": 7 * 24 * 60 * 60,  # 1 week
    }

    fastapi_response.set_cookie(key="refresh_token", value=refresh_token, **options)

    fastapi_response.set_cookie(key="access_token", value=access_token, **options)
    return fastapi_response


def reset_password(credentials: ResetPasswordFormat, db: Session) -> JSONResponse:
    new_user = Users(username=credentials.username, email=credentials.email)
    username = new_user.username
    email = new_user.email
    checkUser = (
        db.query(Users)
        .filter(or_(Users.username == username, Users.email == email))
        .first()
    )

    if not checkUser:
        raise ApiError(message="Username/Email is incorrect")

    # Check Password
    isPasswordValid = checkUser.isPasswordCorrect(credentials.oldPassword)

    if not isPasswordValid:
        raise ApiError(message="Incorrect Password")

    if checkUser.isPasswordCorrect(credentials.newPassword):
        raise ApiError(message="New password cannot be same as the old one.")

    checkUser.hashed_password = pwd_context.hash(credentials.newPassword)
    db.commit()

    response = ApiResponse(message="Password Reset successful!!", data={})
    fastapi_response = JSONResponse(content=jsonable_encoder(response))
    return fastapi_response


def logout_user(req: Request, db: Session) -> JSONResponse:
    user_id = req.state.user.get("id")

    # Removing from database
    user = (
        db.query(Users).filter(Users.id == user_id).first()
    )  # Users.id == user_id order is imp we cant do user_id==Users.id
    user.refresh_token = None
    db.commit()

    # Removing from cookie
    response = ApiResponse(status=200, message="Logout Successful", data={})

    fastapi_response = JSONResponse(content=response.model_dump())
    fastapi_response.delete_cookie(key="refresh_token")
    fastapi_response.delete_cookie(key="access_token")
    return fastapi_response
