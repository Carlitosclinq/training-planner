from typing import List, Dict, Any
from datetime import datetime, timedelta
from .intervals_client import IntervalsClient
from .training_planner import TrainingPlanner
from .workout_generator import WorkoutGenerator
from ..models.goals import Race, PowerGoal
from ..models.calendar import DaySettings

class SyncService:
    def __init__(self, intervals_client: IntervalsClient):
        self.intervals = intervals_client
        self.training_planner = TrainingPlanner(intervals_client)
        self.workout_generator = WorkoutGenerator()

    async def sync_workouts(
        self,
        races: List[Race],
        power_goals: List[PowerGoal],
        calendar: List[DaySettings],
        start_date: datetime,
        end_date: datetime,
        prompt: str = None
    ) -> Dict[str, Any]:
        # Générer le plan d'entraînement
        training_plan = self.training_planner.generate_training_plan(
            races=races,
            power_goals=power_goals,
            calendar=calendar,
            start_date=start_date,
            end_date=end_date,
            prompt=prompt
        )

        # Synchroniser chaque séance avec intervals.icu
        synced_workouts = []
        failed_workouts = []

        for workout in training_plan:
            try:
                # Adapter le format du workout pour intervals.icu
                intervals_workout = self._convert_to_intervals_format(workout)
                
                # Pousser le workout vers intervals.icu
                response = self.intervals.create_workout(intervals_workout)
                
                synced_workouts.append({
                    'date': workout['date'],
                    'name': workout['name'],
                    'intervals_id': response['id']
                })
            except Exception as e:
                failed_workouts.append({
                    'date': workout['date'],
                    'name': workout['name'],
                    'error': str(e)
                })

        return {
            'success': len(synced_workouts),
            'failed': len(failed_workouts),
            'synced_workouts': synced_workouts,
            'failed_workouts': failed_workouts
        }

    def _convert_to_intervals_format(self, workout: Dict[str, Any]) -> Dict[str, Any]:
        """Convertir le format de workout interne vers le format intervals.icu"""
        return {
            'name': workout['name'],
            'description': workout.get('description', ''),
            'type': self._determine_workout_type(workout),
            'date': workout['date'].strftime('%Y-%m-%d'),
            'intervals': self._convert_intervals(workout['intervals'])
        }

    def _determine_workout_type(self, workout: Dict[str, Any]) -> str:
        """Déterminer le type de séance pour intervals.icu"""
        name = workout['name'].lower()
        description = workout.get('description', '').lower()

        if 'endurance' in name or 'endurance' in description:
            return 'endurance'
        elif 'seuil' in name or 'threshold' in name:
            return 'threshold'
        elif 'vo2' in name or 'vo2max' in name:
            return 'vo2max'
        elif 'sprint' in name or 'puissance' in name:
            return 'sprint'
        elif 'récup' in name or 'recovery' in name:
            return 'recovery'
        else:
            return 'workout'

    def _convert_intervals(self, intervals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convertir les intervalles au format intervals.icu"""
        converted = []

        for interval in intervals:
            if 'repeat' in interval:
                # Gérer les blocs répétés
                repeat_block = {
                    'repeat': interval['repeat'],
                    'intervals': self._convert_intervals(interval['intervals'])
                }
                converted.append(repeat_block)
            else:
                # Intervalle simple
                converted_interval = {
                    'duration': interval['duration'],
                    'power': interval.get('power', 0),
                    'name': interval.get('name', '')
                }

                # Gérer les rampes de puissance
                if 'start_power' in interval and 'end_power' in interval:
                    converted_interval['start_power'] = interval['start_power']
                    converted_interval['end_power'] = interval['end_power']
                    del converted_interval['power']

                converted.append(converted_interval)

        return converted

    async def check_sync_status(self, synced_workouts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Vérifier le statut de synchronisation des workouts"""
        status = []

        for workout in synced_workouts:
            try:
                # Vérifier si le workout existe toujours sur intervals.icu
                response = await self.intervals.get_workout(workout['intervals_id'])
                status.append({
                    **workout,
                    'status': 'synced',
                    'last_check': datetime.now()
                })
            except Exception as e:
                status.append({
                    **workout,
                    'status': 'error',
                    'error': str(e),
                    'last_check': datetime.now()
                })

        return status

    async def resync_failed_workouts(self, failed_workouts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Retenter la synchronisation des workouts échoués"""
        newly_synced = []
        still_failed = []

        for workout in failed_workouts:
            try:
                intervals_workout = self._convert_to_intervals_format(workout)
                response = await self.intervals.create_workout(intervals_workout)
                newly_synced.append({
                    'date': workout['date'],
                    'name': workout['name'],
                    'intervals_id': response['id']
                })
            except Exception as e:
                still_failed.append({
                    'date': workout['date'],
                    'name': workout['name'],
                    'error': str(e)
                })

        return {
            'newly_synced': newly_synced,
            'still_failed': still_failed
        }
