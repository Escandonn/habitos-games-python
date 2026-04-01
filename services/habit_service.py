from sqlalchemy.orm import Session
from models.habito import Habito
from models.registro import RegistroDiario
from datetime import date

class HabitService:
    @staticmethod
    def ensure_today_records(db: Session):
        """Genera registros diarios para hoy si no existen."""
        today = date.today()
        # Obtener todos los hábitos activos
        active_habits = db.query(Habito).filter(Habito.activo == True).all()
        
        for h in active_habits:
            # Verificar si ya existe un registro para hoy
            exists = db.query(RegistroDiario).filter(
                RegistroDiario.habito_id == h.id, 
                RegistroDiario.fecha == today
            ).first()
            
            if not exists:
                record = RegistroDiario(habito_id=h.id, fecha=today, completado=False)
                db.add(record)
        
        db.commit()
