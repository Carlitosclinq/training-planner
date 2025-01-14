from typing import Dict, Any, List
import re

class WorkoutGenerator:
    def __init__(self):
        self.workout_patterns = {
            r'(?i)seuil|threshold': self._generate_threshold_workout,
            r'(?i)vo2|vo2max': self._generate_vo2max_workout,
            r'(?i)sprint|puissance': self._generate_sprint_workout,
            r'(?i)endurance|long': self._generate_endurance_workout,
            r'(?i)récup|recovery': self._generate_recovery_workout,
            r'(?i)test|ftp': self._generate_ftp_test_workout
        }

    def parse_prompt(self, prompt: str, ftp: float) -> Dict[str, Any]:
        # Déterminer le type d'entraînement basé sur le prompt
        for pattern, generator in self.workout_patterns.items():
            if re.search(pattern, prompt):
                return generator(ftp)

        # Par défaut, générer un entraînement d'endurance
        return self._generate_endurance_workout(ftp)

    def _generate_threshold_workout(self, ftp: float) -> Dict[str, Any]:
        return {
            "name": "Séance Seuil",
            "description": "Entraînement au seuil pour améliorer votre endurance",
            "intervals": [
                {
                    "name": "Warm-up",
                    "duration": 900,  # 15 minutes
                    "power": ftp * 0.6
                },
                {
                    "name": "Main Set",
                    "repeat": 3,
                    "intervals": [
                        {
                            "duration": 1200,  # 20 minutes
                            "power": ftp * 0.95
                        },
                        {
                            "duration": 300,  # 5 minutes
                            "power": ftp * 0.55
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

    def _generate_vo2max_workout(self, ftp: float) -> Dict[str, Any]:
        return {
            "name": "Séance VO2max",
            "description": "Intervalles intensifs pour améliorer votre VO2max",
            "intervals": [
                {
                    "name": "Warm-up",
                    "duration": 900,
                    "power": ftp * 0.6
                },
                {
                    "name": "Main Set",
                    "repeat": 6,
                    "intervals": [
                        {
                            "duration": 180,  # 3 minutes
                            "power": ftp * 1.15
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

    def _generate_sprint_workout(self, ftp: float) -> Dict[str, Any]:
        return {
            "name": "Séance Sprint",
            "description": "Développement de la puissance maximale",
            "intervals": [
                {
                    "name": "Warm-up",
                    "duration": 1200,  # 20 minutes
                    "power": ftp * 0.6
                },
                {
                    "name": "Main Set",
                    "repeat": 8,
                    "intervals": [
                        {
                            "duration": 30,  # 30 secondes
                            "power": ftp * 2.0
                        },
                        {
                            "duration": 270,  # 4:30 minutes
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

    def _generate_endurance_workout(self, ftp: float) -> Dict[str, Any]:
        return {
            "name": "Séance Endurance",
            "description": "Développement de l'endurance de base",
            "intervals": [
                {
                    "name": "Main Set",
                    "duration": 7200,  # 2 heures
                    "power": ftp * 0.7
                }
            ]
        }

    def _generate_recovery_workout(self, ftp: float) -> Dict[str, Any]:
        return {
            "name": "Séance Récupération",
            "description": "Séance légère pour favoriser la récupération",
            "intervals": [
                {
                    "name": "Recovery",
                    "duration": 3600,  # 1 heure
                    "power": ftp * 0.5
                }
            ]
        }

    def _generate_ftp_test_workout(self, ftp: float) -> Dict[str, Any]:
        return {
            "name": "Test FTP",
            "description": "Test FTP de 20 minutes",
            "intervals": [
                {
                    "name": "Warm-up",
                    "duration": 1200,  # 20 minutes
                    "power": ftp * 0.6
                },
                {
                    "name": "Ramp-up",
                    "duration": 300,  # 5 minutes
                    "start_power": ftp * 0.7,
                    "end_power": ftp * 0.9
                },
                {
                    "name": "Recovery",
                    "duration": 300,  # 5 minutes
                    "power": ftp * 0.5
                },
                {
                    "name": "Test",
                    "duration": 1200,  # 20 minutes
                    "power": ftp * 1.05
                },
                {
                    "name": "Cool-down",
                    "duration": 600,  # 10 minutes
                    "power": ftp * 0.5
                }
            ]
        }
