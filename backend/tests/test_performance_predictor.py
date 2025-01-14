import pytest
from app.services.performance_predictor import PerformancePredictor

def test_predict_ftp():
    predictor = PerformancePredictor()
    activities = [
        {"type": "ride", "power": {"normalized": 250}, "duration": 3600},
        {"type": "ride", "power": {"normalized": 280}, "duration": 1800}
    ]
    
    ftp = predictor.predict_ftp(activities)
    assert isinstance(ftp, (int, float))
    assert ftp > 0

def test_predict_race_time():
    predictor = PerformancePredictor()
    current_ftp = 250
    race_distance = 40000  # 40km
    
    time = predictor.predict_race_time(current_ftp, race_distance)
    assert isinstance(time, (int, float))
    assert time > 0