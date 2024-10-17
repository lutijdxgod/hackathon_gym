from sqlalchemy import MetaData, Column, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from ..config import settings


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=settings.db.naming_convention)

    id = Column(Integer, primary_key=True, nullable=False)
