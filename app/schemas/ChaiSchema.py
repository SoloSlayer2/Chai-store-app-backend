from pydantic import BaseModel
from typing import Annotated
from pydantic import BaseModel, Field


class ChaiPydanticSchema(BaseModel):
    name: str
    price: Annotated[int, Field(max_digits=5, decimal_places=2)]
    chai_type: str
    available: bool

class OrderChaiFormat(BaseModel):
    name:str
    quantity: Annotated[int,Field(decimal_places=0)]