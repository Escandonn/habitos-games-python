from sqlalchemy.orm import Session
from sqlalchemy import func
from models.registro import RegistroDiario
from models.retroalimentacion import Retroalimentacion
from models.habito import Habito
from datetime import date, timedelta
import numpy as np

class StatsService:
    @staticmethod
    def get_weekly_xp(db: Session):
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        results = db.query(RegistroDiario.fecha, func.sum(RegistroDiario.xp_ganada)).filter(RegistroDiario.fecha >= start_of_week).group_by(RegistroDiario.fecha).all()
        return {r[0]: r[1] for r in results}

    @staticmethod
    def get_habit_stats(db: Session, habit_id: int):
        # Stats for a single habit
        total_days = db.query(func.count(RegistroDiario.id)).filter(RegistroDiario.habito_id == habit_id).scalar() or 0
        completed_days = db.query(func.count(RegistroDiario.id)).filter(RegistroDiario.habito_id == habit_id, RegistroDiario.completado == True).scalar() or 0
        total_xp = db.query(func.sum(RegistroDiario.xp_ganada)).filter(RegistroDiario.habito_id == habit_id).scalar() or 0
        
        perc = (completed_days / total_days * 100) if total_days > 0 else 0
        return {
            "total": total_days,
            "completed": completed_days,
            "percentage": perc,
            "xp": total_xp
        }

    @staticmethod
    def get_energy_trends(db: Session, days=15):
        start_date = date.today() - timedelta(days=days)
        return db.query(Retroalimentacion).filter(Retroalimentacion.fecha >= start_date).order_by(Retroalimentacion.fecha).all()

    @staticmethod
    def get_correlations(db: Session):
        # Example: Correlation between Sleep and Productivity
        data = db.query(Retroalimentacion.horas_sueno, Retroalimentacion.productividad).all()
        if len(data) < 5: return "Datos insuficientes para correlación"
        
        sleep = [r[0] for r in data]
        prod = [r[1] for r in data]
        corr = np.corrcoef(sleep, prod)[0, 1]
        
        if corr > 0.6: return "Alta correlación: ¡Dormir bien aumenta tu productividad significativamente!"
        if corr > 0.3: return "Correlación moderada detectada entre sueño y productividad."
        return "Sigue registrando para descubrir tus patrones de éxito."
    
    @staticmethod
    def get_best_habit(db: Session):
        result = db.query(Habito.nombre, func.count(RegistroDiario.id)).join(RegistroDiario).filter(RegistroDiario.completado == True).group_by(Habito.nombre).order_by(func.count(RegistroDiario.id).desc()).first()
        return result[0] if result else "Ninguno aún"
