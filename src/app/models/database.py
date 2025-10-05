from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import os
from ..config import settings

# Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DriveThruSession(Base):
    __tablename__ = "drive_thru_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_uuid = Column(String, unique=True, index=True)
    vehicle_info = Column(String(100))
    lane_number = Column(Integer)
    status = Column(String(50), default="active")
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    total_amount = Column(Float, default=0.0)
    estimated_wait_time = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="session")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("drive_thru_sessions.id"))
    order_number = Column(String(50), unique=True, index=True)
    status = Column(String(50), default="ordering")
    total_amount = Column(Float, default=0.0)
    special_instructions = Column(Text)
    payment_status = Column(String(50), default="pending")
    payment_method = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    session = relationship("DriveThruSession", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float)
    selected_modifiers = Column(JSON)
    special_instructions = Column(Text)
    item_total = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="items")

class ConversationTurn(Base):
    __tablename__ = "conversation_turns"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("drive_thru_sessions.id"))
    speaker = Column(String(50), nullable=False)
    utterance_text = Column(Text, nullable=False)
    intent = Column(String(100))
    entities = Column(JSON)
    track = Column(String(50))
    audio_duration = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("DriveThruSession")

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()