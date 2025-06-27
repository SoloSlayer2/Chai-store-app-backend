from typing import Optional

from sqlalchemy import Boolean, Integer, Numeric, PrimaryKeyConstraint, String, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import decimal

class Base(DeclarativeBase):
    pass


class ChaiStore(Base):
    __tablename__ = 'chai_store'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='chai_store_pkey'),
        UniqueConstraint('name', name='chai_store_name_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(5, 2))
    chai_type: Mapped[Optional[str]] = mapped_column(String(50))
    available: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))