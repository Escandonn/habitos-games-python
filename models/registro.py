from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey, String
from database.db_manager import Base
from datetime import date

class RegistroDiario(Base):
    __tablename__ = "registro_diario"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, default=date.today)
    habito_id = Column(Integer, ForeignKey("habitos.id"))
    completado = Column(Boolean, default=False)
    xp_ganada = Column(Integer, default=0)
    tiempo_invertido = Column(Integer, default=0) # en minutos
    notas_dia = Column(String, default="")
