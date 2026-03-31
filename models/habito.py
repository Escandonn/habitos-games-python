from sqlalchemy import Column, Integer, String, Boolean, Date
from database.db_manager import Base
from datetime import date

class Habito(Base):
    __tablename__ = "habitos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    categoria = Column(String)
    prioridad = Column(String) # Baja, Media, Alta
    intensidad = Column(String) # Baja, Media, Alta
    frecuencia = Column(String) # Diario, Semanal, etc.
    dias_especificos = Column(String, default="") # L,M,M,J,V,S,D
    fecha_inicio = Column(Date, default=date.today)
    activo = Column(Boolean, default=True)
