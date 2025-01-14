from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from ..db.database import Base
from datetime import datetime
import enum

class PriorityLevel(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"

class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(DateTime)
    distance = Column(Float)
    elevation = Column(Float)
    priority = Column(Enum(PriorityLevel))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PowerGoal(Base):
    __tablename__ = "power_goals"

    id = Column(Integer, primary_key=True, index=True)
    target_ftp = Column(Float)
    target_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
