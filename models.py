from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base
import enum

class TodoStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TodoCategory(str, enum.Enum):
    DESIGN = "design"
    PERSONAL = "personal"
    HOUSE = "house"
    WORK = "work"
    HEALTH = "health"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String)

    todos = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    category = Column(SQLEnum(TodoCategory), nullable=False)
    status = Column(SQLEnum(TodoStatus), default=TodoStatus.PENDING, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    scheduled_date = Column(Date, nullable=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")
