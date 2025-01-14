from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..db.database import get_db
from ..models.goals import Race, PowerGoal
from ..services.metrics_analyzer import MetricsAnalyzer
from ..services.intervals_client import IntervalsClient
from pydantic import BaseModel

router = APIRouter()

class RaceCreate(BaseModel):
    name: str
    date: datetime
    distance: float
    elevation: float
    priority: str
    description: Optional[str] = None

class RaceResponse(BaseModel):
    id: int
    name: str
    date: datetime
    distance: float
    elevation: float
    priority: str
    description: Optional[str]
    preparation_analysis: Optional[dict]

class PowerGoalCreate(BaseModel):
    target_ftp: float
    target_date: datetime
    description: Optional[str] = None

class PowerGoalResponse(BaseModel):
    id: int
    target_ftp: float
    target_date: datetime
    description: Optional[str]
    progress_analysis: Optional[dict]

# Routes pour les objectifs de course
@router.post('/races', response_model=RaceResponse)
async def create_race(
    race: RaceCreate,
    db: Session = Depends(get_db),
    intervals_client: IntervalsClient = Depends(get_intervals_client)
):
    db_race = Race(**race.dict())
    db.add(db_race)
    db.commit()
    db.refresh(db_race)
    
    analyzer = MetricsAnalyzer(intervals_client)
    metrics = await analyzer.get_training_metrics()
    analysis = analyzer.analyze_race_preparation(db_race, metrics['current_metrics'])
    
    return {
        **db_race.__dict__,
        'preparation_analysis': analysis
    }

@router.get('/races/{race_id}', response_model=RaceResponse)
async def get_race(race_id: int, db: Session = Depends(get_db)):
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Course non trouvée")
    return race

@router.put('/races/{race_id}', response_model=RaceResponse)
async def update_race(
    race_id: int,
    race_update: RaceCreate,
    db: Session = Depends(get_db)
):
    db_race = db.query(Race).filter(Race.id == race_id).first()
    if not db_race:
        raise HTTPException(status_code=404, detail="Course non trouvée")
    
    for key, value in race_update.dict().items():
        setattr(db_race, key, value)
    
    db.commit()
    db.refresh(db_race)
    return db_race

@router.delete('/races/{race_id}')
async def delete_race(race_id: int, db: Session = Depends(get_db)):
    db_race = db.query(Race).filter(Race.id == race_id).first()
    if not db_race:
        raise HTTPException(status_code=404, detail="Course non trouvée")
    
    db.delete(db_race)
    db.commit()
    return {"message": "Course supprimée"}

# Routes pour les objectifs de puissance
@router.post('/power', response_model=PowerGoalResponse)
async def create_power_goal(
    goal: PowerGoalCreate,
    db: Session = Depends(get_db),
    intervals_client: IntervalsClient = Depends(get_intervals_client)
):
    db_goal = PowerGoal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    
    analyzer = MetricsAnalyzer(intervals_client)
    metrics = await analyzer.get_training_metrics()
    progress = analyzer.analyze_power_progress(db_goal, metrics['current_metrics'])
    
    return {
        **db_goal.__dict__,
        'progress_analysis': progress
    }

@router.get('/power/{goal_id}', response_model=PowerGoalResponse)
async def get_power_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    intervals_client: IntervalsClient = Depends(get_intervals_client)
):
    goal = db.query(PowerGoal).filter(PowerGoal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Objectif non trouvé")
    
    analyzer = MetricsAnalyzer(intervals_client)
    metrics = await analyzer.get_training_metrics()
    progress = analyzer.analyze_power_progress(goal, metrics['current_metrics'])
    
    return {
        **goal.__dict__,
        'progress_analysis': progress
    }

@router.put('/power/{goal_id}', response_model=PowerGoalResponse)
async def update_power_goal(
    goal_id: int,
    goal_update: PowerGoalCreate,
    db: Session = Depends(get_db)
):
    db_goal = db.query(PowerGoal).filter(PowerGoal.id == goal_id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Objectif non trouvé")
    
    for key, value in goal_update.dict().items():
        setattr(db_goal, key, value)
    
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.delete('/power/{goal_id}')
async def delete_power_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = db.query(PowerGoal).filter(PowerGoal.id == goal_id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Objectif non trouvé")
    
    db.delete(db_goal)
    db.commit()
    return {"message": "Objectif supprimé"}
