from sqlalchemy import MetaData, Column, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config import settings


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=settings.db.naming_convention)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        cols = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
