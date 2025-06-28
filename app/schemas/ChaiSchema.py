from decimal import Decimal
from typing import Annotated, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ChaiPydanticSchema(BaseModel):
    name: str
    price: Annotated[Decimal, Field(max_digits=5, decimal_places=2)]
    chai_type: Optional[str]
    available: bool

    model_config = ConfigDict(from_attributes=True)


class OrderChaiFormat(BaseModel):
    name: str
    quantity: Annotated[Decimal, Field(decimal_places=0)]


class ChaiReceipt(BaseModel):
    order: Optional[Dict[str, str]]
    notAvailable: Optional[List[str]]
    Total: Decimal
