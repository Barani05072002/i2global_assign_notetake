from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_name = Column(String(255), nullable=False)
    user_email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    create_on = Column(DateTime, default=datetime.utcnow)

    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")

class Note(Base):
    __tablename__ = "notes"
    note_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    note_title = Column(String(255), nullable=False)
    note_content = Column(String(255), nullable=False)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_on = Column(DateTime, default=datetime.utcnow)

    user_id = Column(CHAR(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="notes")