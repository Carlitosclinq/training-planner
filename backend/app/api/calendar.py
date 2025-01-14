from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from ..db.database import get_db
from ..models.calendar import DaySettings
from pydantic import BaseModel

router = APIRouter()

class TimeSlot(BaseModel):
    start: str
    end: str

class DaySettingsCreate(BaseModel):
    date: date
    available: bool = True
    time_slots: List[TimeSlot]
    is_remote_work: bool = False
    notes: Optional[str] = None

class DaySettingsResponse(BaseModel):
    id: int
    date: date
    available: bool
    time_slots: List[TimeSlot]
    is_remote_work: bool
    notes: Optional[str]

class WeeklySettings(BaseModel):
    start_date: date
    end_date: date
    settings: List[DaySettingsCreate]

@router.post('/days', response_model=DaySettingsResponse)
async def create_day_settings(settings: DaySettingsCreate, db: Session = Depends(get_db)):
    db_settings = DaySettings(
        date=settings.date,
        available=settings.available,
        time_slots=[slot.dict() for slot in settings.time_slots],
        is_remote_work=settings.is_remote_work,
        notes=settings.notes
    )
    
    # Vérifier si les paramètres existent déjà pour cette date
    existing = db.query(DaySettings).filter(DaySettings.date == settings.date).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Les paramètres pour cette date existent déjà"
        )
    
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings

@router.get('/days/{date}', response_model=DaySettingsResponse)
async def get_day_settings(date: date, db: Session = Depends(get_db)):
    settings = db.query(DaySettings).filter(DaySettings.date == date).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Paramètres non trouvés")
    return settings

@router.put('/days/{date}', response_model=DaySettingsResponse)
async def update_day_settings(
    date: date,
    settings_update: DaySettingsCreate,
    db: Session = Depends(get_db)
):
    db_settings = db.query(DaySettings).filter(DaySettings.date == date).first()
    if not db_settings:
        raise HTTPException(status_code=404, detail="Paramètres non trouvés")
    
    db_settings.available = settings_update.available
    db_settings.time_slots = [slot.dict() for slot in settings_update.time_slots]
    db_settings.is_remote_work = settings_update.is_remote_work
    db_settings.notes = settings_update.notes
    
    db.commit()
    db.refresh(db_settings)
    return db_settings

@router.delete('/days/{date}')
async def delete_day_settings(date: date, db: Session = Depends(get_db)):
    db_settings = db.query(DaySettings).filter(DaySettings.date == date).first()
    if not db_settings:
        raise HTTPException(status_code=404, detail="Paramètres non trouvés")
    
    db.delete(db_settings)
    db.commit()
    return {"message": "Paramètres supprimés"}

@router.post('/weeks', response_model=List[DaySettingsResponse])
async def set_weekly_settings(settings: WeeklySettings, db: Session = Depends(get_db)):
    """Définir les paramètres pour une semaine entière"""
    responses = []
    for day_settings in settings.settings:
        try:
            db_settings = DaySettings(
                date=day_settings.date,
                available=day_settings.available,
                time_slots=[slot.dict() for slot in day_settings.time_slots],
                is_remote_work=day_settings.is_remote_work,
                notes=day_settings.notes
            )
            
            existing = db.query(DaySettings).filter(DaySettings.date == day_settings.date).first()
            if existing:
                # Mettre à jour les paramètres existants
                for key, value in day_settings.dict().items():
                    if key == 'time_slots':
                        existing.time_slots = [slot.dict() for slot in value]
                    else:
                        setattr(existing, key, value)
                db_settings = existing
            else:
                db.add(db_settings)
            
            db.commit()
            db.refresh(db_settings)
            responses.append(db_settings)
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Erreur lors de la configuration du {day_settings.date}: {str(e)}"
            )
    
    return responses

@router.get('/weeks/{start_date}/{end_date}', response_model=List[DaySettingsResponse])
async def get_weekly_settings(start_date: date, end_date: date, db: Session = Depends(get_db)):
    """Récupérer les paramètres pour une période donnée"""
    settings = db.query(DaySettings).filter(
        DaySettings.date >= start_date,
        DaySettings.date <= end_date
    ).all()
    
    return settings
