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
    def generate_insights(db: Session):
        # Insights estáticos basados en algoritmos simples
        insights = []
        data = db.query(Retroalimentacion.horas_sueno, Retroalimentacion.productividad, Retroalimentacion.estres, Retroalimentacion.energia).all()
        if len(data) < 3: 
            return "💡 Registra más días de feedback para obtener insights personalizados."
        
        sleep = [r[0] for r in data]
        prod = [r[1] for r in data]
        stress = [r[2] for r in data]
        energy = [r[3] for r in data]
        
        # 1. Sueño vs Productividad
        if np.std(sleep) > 0 and np.std(prod) > 0:
            corr_sleep = np.corrcoef(sleep, prod)[0, 1]
            if corr_sleep > 0.5: insights.append("💡 Dormir bien dispara tu productividad. ¡Protege tus horas de sueño!")
            elif corr_sleep < -0.5: insights.append("💡 Curiosamente, estás siendo productivo incluso con poco sueño. Ten cuidado con el burnout.")
            
        # 2. Estrés vs Energía
        if np.corrcoef(stress, energy)[0, 1] < -0.4:
            insights.append("🛡️ Tus días de alto estrés drenan drásticamente tu energía. Prueba meditar 5 min.")
            
        # 3. Consistencia general
        avg_energy = sum(energy) / len(energy)
        if avg_energy > 7:
            insights.append("⚡ Estás en una racha de alta energía general. ¡Aprovecha para proyectos difíciles!")
        elif avg_energy < 4:
            insights.append("⚠️ Tu energía promedio está baja. Recuerda que descansar es parte del proceso.")

        if not insights:
            return "💡 Tus métricas están muy estables. ¡Sigue así!"
            
        import random
        return random.choice(insights)
    
    @staticmethod
    def get_best_habit(db: Session):
        result = db.query(Habito.nombre, func.count(RegistroDiario.id)).join(RegistroDiario).filter(RegistroDiario.completado == True).group_by(Habito.nombre).order_by(func.count(RegistroDiario.id).desc()).first()
        return result[0] if result else "Ninguno aún"
