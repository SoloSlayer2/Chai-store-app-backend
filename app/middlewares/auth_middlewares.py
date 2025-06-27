import os
from uuid import UUID

from dotenv import load_dotenv
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db.setup_db import SessionLocal
from app.models.users_models import Users
from app.utils import ApiError

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


async def jwt_verify(req: Request, call_next):
    # path = req.url.path
    # if path.startswith("/auth"):
    #     return await call_next(req)

    PUBLIC_ROUTES = {"/auth/login", "/auth/register"}

    if req.url.path in PUBLIC_ROUTES:
        return await call_next(req)

    token = req.cookies.get("access_token") or (
        req.headers.get("Authorization").split(" ")[1]
        if req.headers.get("Authorization", "").startswith("Bearer ")
        else None
    )
    if not token:
        raise ApiError(message="You are unauthorized!", status_code=401)

    try:
        payload = jwt.decode(token=token, key=JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        db: Session = SessionLocal()
        user = db.query(Users).filter(Users.id == UUID(user_id)).first()
        db.close()
        if not user:
            raise ApiError(
                message="Invalid Token or expired token passed", status_code=401
            )
        req.state.user = payload
    except JWTError:
        raise ApiError(message="Invalid Token or expired token passed", status_code=401)
    return await call_next(req)
