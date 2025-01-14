import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ..core.config import get_settings

class IntervalsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.settings = get_settings()
        self.base_url = self.settings.intervals_api_url

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get_athlete_info(self) -> Dict[str, Any]:
        response = requests.get(
            f'{self.base_url}/athlete',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def get_power_curve(self) -> Dict[str, Any]:
        response = requests.get(
            f'{self.base_url}/power-curve',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def get_fitness_history(self, start_date: datetime = None, end_date: datetime = None) -> List[Dict[str, Any]]:
        if not start_date:
            start_date = datetime.now() - timedelta(days=90)
        if not end_date:
            end_date = datetime.now()

        params = {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        }

        response = requests.get(
            f'{self.base_url}/athlete/fitness',
            headers=self._get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()

    def create_workout(self, workout_data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f'{self.base_url}/workout',
            headers=self._get_headers(),
            json=workout_data
        )
        response.raise_for_status()
        return response.json()

    def get_workouts(self, start_date: datetime = None, end_date: datetime = None) -> List[Dict[str, Any]]:
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()

        params = {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        }

        response = requests.get(
            f'{self.base_url}/workouts',
            headers=self._get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()
