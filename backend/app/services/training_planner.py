from datetime import datetime, timedelta
from typing import List, Dict, Any
from .intervals_client import IntervalsClient
from ..models.goals import Race, PowerGoal
from ..models.calendar import DaySettings

class TrainingPlanner:
    def __init__(self, intervals_client: IntervalsClient):
        self.intervals = intervals_client

    def generate_training_plan(
        self,
        races: List[Race],
        power_goals: List[PowerGoal],
        calendar: List[DaySettings],
        start_date: datetime,
        end_date: datetime,
        prompt: str = None
    ) -> List[Dict[str, Any]]:
        # Récupérer les données de fitness actuelles
        fitness_data = self.intervals.get_fitness_history()
        current_ftp = fitness_data[-1].get('ftp', 200)  # FTP par défaut si non disponible

        # Trier les courses par date et priorité
        sorted_races = sorted(races, key=lambda x: (x.date, x.priority))

        # Générer le plan d'entraînement
        training_plan = []
        current_date = start_date

        while current_date <= end_date:
            # Vérifier si le jour est disponible
            day_setting = next((d for d in calendar if d.date.date() == current_date.date()), None)
            if not day_setting or not day_setting.available:
                current_date += timedelta(days=1)
                continue

            # Trouver la prochaine course
            next_race = next((r for r in sorted_races if r.date > current_date), None)

            # Déterminer le type d'entraînement en fonction des objectifs
            if next_race:
                weeks_to_race = (next_race.date - current_date).days // 7
                if weeks_to_race <= 2:
                    # Affinage pour la course
                    workout = self._generate_taper_workout(current_ftp, next_race)
                elif weeks_to_race <= 8:
                    # Entraînement spécifique pour la course
                    workout = self._generate_race_specific_workout(current_ftp, next_race)
                else:
                    # Entraînement de base
                    workout = self._generate_base_workout(current_ftp)
            else:
                # Entraînement général d'amélioration
                workout = self._generate_base_workout(current_ftp)

            training_plan.append(workout)
            current_date += timedelta(days=1)

        return training_plan

    def _generate_base_workout(self, ftp: float) -> Dict[str, Any]:
        """Génère un entraînement de base pour l'amélioration générale"""
        # Exemple simple - à personnaliser selon les besoins
        return {
            "name": "Entraînement de base",
            "description": "Séance d'amélioration générale",
            "intervals": [
                {
                    "name": "Warm-up",
                    "duration": 900,  # 15 minutes
                    "power": ftp * 0.6
                },
                {
                    "name": "Main Set",
                    "repeat": 4,
                    "intervals": [
                        {
                            "duration": 480,  # 8 minutes
                            "power": ftp * 0.88
                        },
                        {
                            "duration": 120,  # 2 minutes
                            "power": ftp * 0.5
                        }
                    ]
                },
                {
                    "name": "Cool-down",
                    "duration": 600,  # 10 minutes
                    "power": ftp * 0.55
                }
            ]
        }

    def _generate_race_specific_workout(self, ftp: float, race: Race) -> Dict[str, Any]:
        """Génère un entraînement spécifique pour une course"""
        # Adapter l'entraînement en fonction du profil de la course
        if race.elevation > 2000:  # Course avec beaucoup de dénivelé
            return {
                "name": "Entraînement spécifique montagne",
                "description": f"Préparation pour {race.name}",
                "intervals": [
                    {
                        "name": "Warm-up",
                        "duration": 900,
                        "power": ftp * 0.6
                    },
                    {
                        "name": "Main Set",
                        "repeat": 3,
                        "intervals": [
                            {
                                "duration": 1200,  # 20 minutes
                                "power": ftp * 0.92
                            },
                            {
                                "duration": 300,  # 5 minutes
                                "power": ftp * 0.5
                            }
                        ]
                    },
                    {
                        "name": "Cool-down",
                        "duration": 600,
                        "power": ftp * 0.55
                    }
                ]
            }
        else:  # Course plate
            return {
                "name": "Entraînement spécifique plat",
                "description": f"Préparation pour {race.name}",
                "intervals": [
                    {
                        "name": "Warm-up",
                        "duration": 900,
                        "power": ftp * 0.6
                    },
                    {
                        "name": "Main Set",
                        "repeat": 5,
                        "intervals": [
                            {
                                "duration": 300,  # 5 minutes
                                "power": ftp * 1.05
                            },
                            {
                                "duration": 180,  # 3 minutes
                                "power": ftp * 0.5
                            }
                        ]
                    },
                    {
                        "name": "Cool-down",
                        "duration": 600,
                        "power": ftp * 0.55
                    }
                ]
            }

    def _generate_taper_workout(self, ftp: float, race: Race) -> Dict[str, Any]:
        """Génère un entraînement d'affinage avant une course"""
        return {
            "name": "Affinage pré-course",
            "description": f"Affinage pour {race.name}",
            "intervals": [
                {
                    "name": "Warm-up",
                    "duration": 900,
                    "power": ftp * 0.6
                },
                {
                    "name": "Main Set",
                    "repeat": 4,
                    "intervals": [
                        {
                            "duration": 120,  # 2 minutes
                            "power": ftp * 1.1
                        },
                        {
                            "duration": 240,  # 4 minutes
                            "power": ftp * 0.5
                        }
                    ]
                },
                {
                    "name": "Cool-down",
                    "duration": 600,
                    "power": ftp * 0.55
                }
            ]
        }
