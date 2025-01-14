from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel

from ..db.database import get_db
from ..services.sync_service import SyncService
from ..services.intervals_client import IntervalsClient
from ..models.goals import Race, PowerGoal
from ..models.calendar import DaySettings

router = APIRouter()

class SyncRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    prompt: Optional[str] = None

class SyncResponse(BaseModel):
    success: int
    failed: int
    synced_workouts: List[dict]
    failed_workouts: List[dict]

@router.post('/sync-workouts', response_model=SyncResponse)
async def sync_workouts(
    sync_request: SyncRequest,
    db: Session = Depends(get_db),
    intervals_client: IntervalsClient = Depends(get_intervals_client)
):
    # Récupérer les objectifs et le calendrier
    races = db.query(Race).filter(
        Race.date >= sync_request.start_date,
        Race.date <= sync_request.end_date
    ).all()

    power_goals = db.query(PowerGoal).filter(
        PowerGoal.target_date >= sync_request.start_date,
        PowerGoal.target_date <= sync_request.end_date
    ).all()

    calendar = db.query(DaySettings).filter(
        DaySettings.date >= sync_request.start_date.date(),
        DaySettings.date <= sync_request.end_date.date()
    ).all()

    # Initialiser le service de synchronisation
    sync_service = SyncService(intervals_client)

    # Synchroniser les workouts
    try:
        result = await sync_service.sync_workouts(
            races=races,
            power_goals=power_goals,
            calendar=calendar,
            start_date=sync_request.start_date,
            end_date=sync_request.end_date,
            prompt=sync_request.prompt
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/sync-status/{workout_id}')
async def check_sync_status(
    workout_id: str,
    intervals_client: IntervalsClient = Depends(get_intervals_client)
):
    sync_service = SyncService(intervals_client)
    try:
        status = await sync_service.check_sync_status([{'intervals_id': workout_id}])
        return status[0] if status else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/resync-failed')
async def resync_failed_workouts(
    failed_workouts: List[dict],
    intervals_client: IntervalsClient = Depends(get_intervals_client)
):
    sync_service = SyncService(intervals_client)
    try:
        result = await sync_service.resync_failed_workouts(failed_workouts)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
