from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from ..services.performance_predictor import PerformancePredictor
from ..services.intervals_client import IntervalsClient

router = APIRouter()

class PredictionRequest(BaseModel):
    days_ahead: int = 30

class RaceReadinessRequest(BaseModel):
    race_date: datetime
    target_ftp: float
    required_ctl: float

@router.post('/performance')
async def predict_performance(
    request: PredictionRequest,
    intervals_client: IntervalsClient = Depends(get_intervals_client)
):
    predictor = PerformancePredictor(intervals_client)
    try:
        prediction = predictor.predict_performance(request.days_ahead)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/race-readiness')
async def analyze_race_readiness(
    request: RaceReadinessRequest,
    intervals_client: IntervalsClient = Depends(get_intervals_client)
):
    predictor = PerformancePredictor(intervals_client)
    try:
        analysis = predictor.analyze_race_readiness(
            race_date=request.race_date,
            target_ftp=request.target_ftp,
            required_ctl=request.required_ctl
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
