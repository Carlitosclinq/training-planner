from typing import List, Dict, Any
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
from .intervals_client import IntervalsClient

class PerformancePredictor:
    def __init__(self, intervals_client: IntervalsClient):
        self.intervals = intervals_client

    def predict_performance(self, days_ahead: int = 30) -> Dict[str, Any]:
        """Prédire les performances futures basées sur l'historique"""
        history = self.intervals.get_fitness_history()
        
        if not history:
            return {
                'ftp_prediction': None,
                'confidence': 0,
                'recommendations': []
            }

        # Préparer les données
        dates = []
        ftps = []
        ctls = []
        atls = []
        tsbs = []

        for entry in history:
            date = datetime.fromisoformat(entry['date'])
            dates.append((date - datetime.now()).days)
            ftps.append(entry.get('ftp', 0))
            ctls.append(entry.get('ctl', 0))
            atls.append(entry.get('atl', 0))
            tsbs.append(entry.get('tsb', 0))

        # Prédiction FTP
        X = np.array(dates).reshape(-1, 1)
        y = np.array(ftps)
        model = LinearRegression()
        model.fit(X, y)

        future_date = np.array([[days_ahead]])
        predicted_ftp = model.predict(future_date)[0]

        # Calcul du niveau de confiance
        confidence = self._calculate_confidence(model.score(X, y), len(dates))

        # Générer recommandations
        recommendations = self._generate_recommendations(
            current_ftp=ftps[-1],
            predicted_ftp=predicted_ftp,
            current_ctl=ctls[-1],
            current_atl=atls[-1],
            current_tsb=tsbs[-1]
        )

        return {
            'current_ftp': ftps[-1],
            'predicted_ftp': round(predicted_ftp),
            'confidence': confidence,
            'predicted_date': (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d'),
            'recommendations': recommendations,
            'metrics_trends': {
                'ctl_trend': self._calculate_trend(ctls),
                'atl_trend': self._calculate_trend(atls),
                'tsb_trend': self._calculate_trend(tsbs)
            }
        }

    def _generate_recommendations(
        self,
        current_ftp: float,
        predicted_ftp: float,
        current_ctl: float,
        current_atl: float,
        current_tsb: float
    ) -> List[str]:
        recommendations = []

        # Analyse FTP
        ftp_change = ((predicted_ftp - current_ftp) / current_ftp) * 100
        if ftp_change > 5:
            recommendations.append(
                "La progression prévue est excellente. Maintenez votre approche actuelle."
            )
        elif ftp_change < 0:
            recommendations.append(
                "Attention à la baisse prévue de FTP. Augmentez l'intensité des entraînements."
            )

        # Analyse charge d'entraînement
        if current_ctl < 40:
            recommendations.append(
                "Charge d'entraînement faible. Augmentez progressivement le volume."
            )
        elif current_ctl > 100:
            recommendations.append(
                "Charge d'entraînement élevée. Surveillez la fatigue et la récupération."
            )

        # Analyse fatigue
        if current_atl > current_ctl * 1.1:
            recommendations.append(
                "Niveau de fatigue élevé. Prévoyez une période de récupération."
            )

        # Analyse forme
        if current_tsb < -20:
            recommendations.append(
                "Forme basse. Diminuez temporairement la charge d'entraînement."
            )
        elif current_tsb > 15:
            recommendations.append(
                "Pic de forme. Période idéale pour des objectifs importants."
            )

        return recommendations

    def _calculate_confidence(self, r2_score: float, sample_size: int) -> float:
        # Pondération des facteurs
        r2_weight = 0.6
        sample_weight = 0.4

        # Score R2 (0-1)
        r2_score = max(0, min(1, r2_score))

        # Score taille d'échantillon
        min_samples = 10
        max_samples = 90
        sample_score = min(1, max(0, (sample_size - min_samples) / (max_samples - min_samples)))

        # Score final (0-100%)
        confidence = (r2_score * r2_weight + sample_score * sample_weight) * 100

        return round(confidence, 1)

    def _calculate_trend(self, values: List[float], window: int = 7) -> str:
        if len(values) < window:
            return 'stable'

        recent_values = values[-window:]
        slope = np.polyfit(range(len(recent_values)), recent_values, 1)[0]

        if slope > 0.5:
            return 'increasing'
        elif slope < -0.5:
            return 'decreasing'
        else:
            return 'stable'

    def analyze_race_readiness(
        self,
        race_date: datetime,
        target_ftp: float,
        required_ctl: float
    ) -> Dict[str, Any]:
        """Analyser l'état de préparation pour une course"""
        # Prédire l'état de forme pour la date de la course
        days_until_race = (race_date - datetime.now()).days
        race_prediction = self.predict_performance(days_until_race)

        # Évaluer la préparation
        ftp_readiness = race_prediction['predicted_ftp'] / target_ftp
        fitness_readiness = race_prediction['metrics_trends']['ctl_trend']

        return {
            'predicted_ftp': race_prediction['predicted_ftp'],
            'ftp_readiness': round(ftp_readiness * 100),
            'fitness_trend': fitness_readiness,
            'recommendations': self._generate_race_recommendations(
                ftp_readiness,
                fitness_readiness,
                days_until_race
            )
        }

    def _generate_race_recommendations(self,
        ftp_readiness: float,
        fitness_trend: str,
        days_until_race: int
    ) -> List[str]:
        recommendations = []

        # Recommandations basées sur le niveau de FTP
        if ftp_readiness < 0.9:
            recommendations.append(
                "Objectif FTP non atteint. Intensifiez les séances spécifiques."
            )
        elif ftp_readiness > 1.1:
            recommendations.append(
                "Excellent niveau de FTP. Focalisez-vous sur la spécificité course."
            )

        # Recommandations basées sur la tendance de forme
        if fitness_trend == 'decreasing' and days_until_race > 14:
            recommendations.append(
                "Forme en baisse. Ajustez la charge pour inverser la tendance."
            )
        elif fitness_trend == 'increasing' and days_until_race < 7:
            recommendations.append(
                "Réduisez progressivement la charge pour un pic de forme optimal."
            )

        # Recommandations basées sur le timing
        if days_until_race <= 7:
            recommendations.append(
                "Derniers jours : focalisez-vous sur l'affinage et la récupération."
            )
        elif days_until_race <= 21:
            recommendations.append(
                "Phase finale : maintenez l'intensité mais réduisez le volume."
            )

        return recommendations
