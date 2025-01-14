import pytest
from datetime import datetime, timedelta
from app.services.training_planner import TrainingPlanner

def test_generate_training_plan():
    planner = TrainingPlanner()
    
    goal = {
        "id": 1,
        "type": "ftp",
        "target_value": 300,
        "target_date": datetime.now() + timedelta(weeks=12)
    }
    
    preferences = {
        "weekly_hours": 10,
        "max_session_duration": 120
    }
    
    plan = planner.generate_plan(goal, preferences)
    
    assert plan is not None
    assert len(plan["workouts"]) > 0
    assert all(w["duration"] <= preferences["max_session_duration"] for w in plan["workouts"])

def test_adapt_plan_to_progress():
    planner = TrainingPlanner()
    
    original_plan = {
        "id": 1,
        "workouts": [
            {
                "date": datetime.now(),
                "type": "interval",
                "target_power": 250
            }
        ]
    }
    
    new_ftp = 280  # FTP a augmenté
    
    adapted_plan = planner.adapt_plan(original_plan, new_ftp)
    
    assert adapted_plan is not None
    assert adapted_plan["workouts"][0]["target_power"] > original_plan["workouts"][0]["target_power"]

def test_validate_plan():
    planner = TrainingPlanner()
    
    invalid_plan = {
        "id": 1,
        "workouts": [
            {
                "date": datetime.now(),
                "type": "interval",
                "target_power": -50  # Puissance négative invalide
            }
        ]
    }
    
    with pytest.raises(ValueError):
        planner.validate_plan(invalid_plan)