from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """User model for storing Telegram user information"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    is_bot = Column(Boolean, default=False)
    refer_id = Column(Integer, nullable=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    username = Column(String(255), nullable=True)
    language_code = Column(String(10), nullable=True)
    is_premium = Column(Boolean, nullable=True)
    can_join_groups = Column(Boolean, nullable=True)
    can_read_all_groups_messages = Column(Boolean, nullable=True)
    supports_inline_queries = Column(Boolean, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now())
    blocked_at = Column(DateTime, nullable=True)

    # Relationship
    drink_records = relationship(
        "DrinkRecord", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, first_name={self.first_name})>"


class DrinkRecord(Base):
    """Drink record model for tracking alcohol consumption"""
    __tablename__ = "drink_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    drink_name = Column(String(255), nullable=False)
    amount = Column(Float, nullable=True)  # in ml or units
    amount_unit = Column(String(50), nullable=True)  # ml, units, etc.
    price = Column(Float, nullable=True)
    note = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now())

    # Relationship
    user = relationship("User", back_populates="drink_records")

    def __repr__(self):
        return f"<DrinkRecord(id={self.id}, user_id={self.user_id}, drink_name={self.drink_name})>"
