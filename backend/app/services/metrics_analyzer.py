from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from ..models.goals import Race, PowerGoal
from .intervals_client import IntervalsClient

class MetricsAnalyzer:
    def __init__(self, intervals_client: IntervalsClient):
        self.intervals = intervals_client
    
    def _calculate_peak_date(self, analyzed_metrics: List[Dict[str, Any]]) -> Optional[datetime]:
        # Trouver la date où le TSB sera optimal (entre 5 et 15)
        current_date = datetime.now()
        best_tsb = float('-inf')
        peak_date = None
        
        # Simuler les 60 prochains jours
        for days in range(60):
            future_date = current_date + timedelta(days=days)
            projected_tsb = self._project_tsb(analyzed_metrics, future_date)
            
            # Le TSB optimal est entre 5 et 15
            if 5 <= projected_tsb <= 15:
                if projected_tsb > best_tsb:
                    best_tsb = projected_tsb
                    peak_date = future_date
        
        return peak_date
    
    def _project_tsb(self, analyzed_metrics: List[Dict[str, Any]], target_date: datetime) -> float:
        # Projeter le TSB futur basé sur les tendances actuelles
        if not analyzed_metrics:
            return 0.0
            
        current_metrics = analyzed_metrics[-1]
        days_diff = (target_date - datetime.strptime(current_metrics['date'], '%Y-%m-%d')).days
        
        # Utiliser les tendances récentes de CTL et ATL pour projeter
        ctl_daily_change = self._calculate_ctl_trend(analyzed_metrics)
        atl_daily_change = self._calculate_atl_trend(analyzed_metrics)
        
        projected_ctl = current_metrics['ctl'] + (ctl_daily_change * days_diff)
        projected_atl = current_metrics['atl'] + (atl_daily_change * days_diff)
        
        # TSB = CTL - ATL
        return projected_ctl - projected_atl
    
    def _calculate_ctl_trend(self, analyzed_metrics: List[Dict[str, Any]], days: int = 7) -> float:
        # Calculer la tendance CTL sur les derniers jours
        recent_metrics = analyzed_metrics[-days:]
        if len(recent_metrics) < 2:
            return 0.0
            
        ctl_change = recent_metrics[-1]['ctl'] - recent_metrics[0]['ctl']
        return ctl_change / len(recent_metrics)
    
    def _calculate_atl_trend(self, analyzed_metrics: List[Dict[str, Any]], days: int = 7) -> float:
        # Calculer la tendance ATL sur les derniers jours
        recent_metrics = analyzed_metrics[-days:]
        if len(recent_metrics) < 2:
            return 0.0
            
        atl_change = recent_metrics[-1]['atl'] - recent_metrics[0]['atl']
        return atl_change / len(recent_metrics)

    def analyze_race_preparation(self, race: Race, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyser la préparation pour une course spécifique"""
        days_to_race = (race.date - datetime.now()).days
        current_ctl = current_metrics['ctl']
        current_atl = current_metrics['atl']
        
        # Calculer les objectifs de préparation
        target_ctl = self._calculate_target_ctl(race)
        weekly_tss_targets = self._generate_weekly_tss_plan(current_ctl, target_ctl, days_to_race)
        
        return {
            'days_to_race': days_to_race,
            'fitness_gap': target_ctl - current_ctl,
            'weekly_tss_targets': weekly_tss_targets,
            'readiness_score': self._calculate_readiness_score(race, current_metrics),
            'recommendations': self._generate_preparation_recommendations(race, current_metrics)
        }
    
    def _calculate_target_ctl(self, race: Race) -> float:
        """Calculer le CTL cible basé sur le profil de la course"""
        # Formule basée sur la distance et le dénivelé
        base_ctl = 80  # CTL de base pour une course courte
        distance_factor = race.distance / 100  # Augmenter le CTL requis avec la distance
        elevation_factor = race.elevation / 1000  # Augmenter avec le dénivelé
        
        return base_ctl + (distance_factor * 10) + (elevation_factor * 5)
    
    def _generate_weekly_tss_plan(self, current_ctl: float, target_ctl: float, days_available: int) -> List[Dict[str, Any]]:
        """Générer un plan de TSS hebdomadaire pour atteindre le CTL cible"""
        weeks_available = days_available // 7
        if weeks_available < 1:
            return []
        
        ctl_increase_needed = target_ctl - current_ctl
        weekly_increase = ctl_increase_needed / weeks_available
        
        weekly_plan = []
        current_week_ctl = current_ctl
        
        for week in range(weeks_available):
            target_week_ctl = current_week_ctl + weekly_increase
            weekly_tss = target_week_ctl * 7  # Approximation simplifiée
            
            weekly_plan.append({
                'week': week + 1,
                'target_ctl': round(target_week_ctl, 1),
                'weekly_tss': round(weekly_tss)
            })
            
            current_week_ctl = target_week_ctl
        
        return weekly_plan
    
    def _calculate_readiness_score(self, race: Race, current_metrics: Dict[str, Any]) -> int:
        """Calculer un score de préparation sur 100"""
        # Facteurs de pondération
        ctl_weight = 0.4
        tsb_weight = 0.3
        volume_weight = 0.3
        
        # Score CTL
        target_ctl = self._calculate_target_ctl(race)
        ctl_score = min(100, (current_metrics['ctl'] / target_ctl) * 100)
        
        # Score TSB
        tsb = current_metrics['tsb']
        tsb_score = 100 if 5 <= tsb <= 15 else max(0, 100 - abs(tsb - 10) * 5)
        
        # Score volume
        # TODO: Implémenter la comparaison avec le volume d'entraînement requis
        volume_score = 80  # Temporaire
        
        final_score = (
            ctl_weight * ctl_score +
            tsb_weight * tsb_score +
            volume_weight * volume_score
        )
        
        return round(final_score)
    
    def _generate_preparation_recommendations(self, race: Race, current_metrics: Dict[str, Any]) -> List[str]:
        """Générer des recommandations spécifiques pour la préparation"""
        recommendations = []
        target_ctl = self._calculate_target_ctl(race)
        
        # Analyse CTL
        if current_metrics['ctl'] < target_ctl * 0.8:
            recommendations.append(
                "Augmentez progressivement votre charge d'entraînement pour atteindre "
                f"un CTL cible de {round(target_ctl)}."
            )
        
        # Analyse TSB
        if current_metrics['tsb'] < -10:
            recommendations.append(
                "Votre fatigue est élevée. Prévoyez une période de récupération "
                "pour optimiser votre forme."
            )
        elif current_metrics['tsb'] > 20:
            recommendations.append(
                "Votre forme est bonne mais attention à maintenir une charge "
                "d'entraînement suffisante."
            )
        
        # Spécificités de la course
        if race.elevation > 2000:
            recommendations.append(
                "Cette course comporte un dénivelé important. Incluez des séances "
                "spécifiques en montée dans votre préparation."
            )
        
        if race.distance > 100:
            recommendations.append(
                "Pour cette longue distance, focalisez-vous sur l'endurance de base "
                "et la gestion de l'effort."
            )
        
        return recommendations
