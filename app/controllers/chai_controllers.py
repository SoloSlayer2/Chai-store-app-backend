from functools import reduce
from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.chai_models import ChaiStore
from app.schemas.ChaiSchema import ChaiPydanticSchema, ChaiReceipt, OrderChaiFormat
from app.utils import ApiError, ApiResponse


def show_chai_menu(db: Session):
    chai_menu = db.query(ChaiStore).all()
    if not chai_menu:
        raise ApiError(message="No Chai found!")

    menu_data = [ChaiPydanticSchema.model_validate(chai) for chai in chai_menu]

    response = ApiResponse(message="The Chai Menu", data={"menu": menu_data})

    fastapi_res = JSONResponse(content=jsonable_encoder(response))

    return fastapi_res


def order_chai(orders: List[OrderChaiFormat], db: Session):

    chai_menu = db.query(
        ChaiStore
    ).all()  # I optimized instead of calling the db many times

    menu_price = {chai.name: chai.price for chai in chai_menu}
    menu_available = {chai.name: chai.available for chai in chai_menu}
    chai_name = [chai.name for chai in chai_menu]
    notAvailable = []
    price_list = []

    # order_price={order.name:order.quantity for order in orders}

    for order in orders:
        if order.name not in chai_name:
            raise ApiError(
                message=f"Enter correct chai name please. No entries for {order.name}"
            )

        if not menu_available.get(order.name):
            notAvailable.append(order.name)

        if order.name not in notAvailable:
            price_list.append(menu_price.get(order.name) * order.quantity)

    total = reduce(lambda x, y: x + y, price_list)
    order_receipt = {
        order.name: f"Quantity: {order.quantity} Price: {menu_price.get(order.name)}"
        for order in orders
        if order.name not in notAvailable
    }

    res = ApiResponse(
        message="Your Bill",
        data={
            "order receipt": ChaiReceipt(
                order=order_receipt, notAvailable=notAvailable, Total=total
            )
        },
    )

    fastapi_res = JSONResponse(content=jsonable_encoder(res))

    return fastapi_res
