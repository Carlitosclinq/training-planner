from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from ..db.database import Base
from datetime import datetime

class DaySettings(Base):
    __tablename__ = "day_settings"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, unique=True, index=True)
    available = Column(Boolean, default=True)
    time_slots = Column(JSON)  # Liste des créneaux horaires
    is_remote_work = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
