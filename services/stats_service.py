from sqlalchemy.orm import Session
from sqlalchemy import func
from models.registro import RegistroDiario
from models.retroalimentacion import Retroalimentacion
from models.habito import Habito
from datetime import date, timedelta

class StatsService:
    @staticmethod
    def get_weekly_xp(db: Session):
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        
        results = db.query(
            RegistroDiario.fecha, 
            func.sum(RegistroDiario.xp_ganada)
        ).filter(RegistroDiario.fecha >= start_of_week).group_by(RegistroDiario.fecha).all()
        
        return {r[0]: r[1] for r in results}

    @staticmethod
    def get_habit_performance(db: Session):
        results = db.query(
            Habito.nombre, 
            func.count(RegistroDiario.id)
        ).join(RegistroDiario).filter(RegistroDiario.completado == True).group_by(Habito.nombre).all()
        
        return {r[0]: r[1] for r in results}

    @staticmethod
    def get_energy_trends(db: Session, days=7):
        start_date = date.today() - timedelta(days=days)
        results = db.query(
            Retroalimentacion.fecha, 
            Retroalimentacion.energia,
            Retroalimentacion.productividad,
            Retroalimentacion.disciplina
        ).filter(Retroalimentacion.fecha >= start_date).order_by(Retroalimentacion.fecha).all()
        
        return results
