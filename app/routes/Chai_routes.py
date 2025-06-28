from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.chai_controllers import order_chai, show_chai_menu
from app.db.setup_db import SessionLocal
from app.schemas.ChaiSchema import ChaiPydanticSchema, ChaiReceipt, OrderChaiFormat

chai_router = APIRouter(prefix="/chai", tags=["Chai"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@chai_router.get("/show-menu")
def show_menu(db: Session = Depends(get_db)):
    return show_chai_menu(db=db)


@chai_router.get("/order")
def order(orders: List[OrderChaiFormat], db: Session = Depends(get_db)):
    return order_chai(orders=orders, db=db)
