from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """User model for database."""

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    name = Column(String(255), nullable=False)
    phone_number = Column(String(255), unique=True, index=True, nullable=False)
    todos = relationship(
        "Todo",
        back_populates="owner",
        cascade="all, delete-orphan",
    )




