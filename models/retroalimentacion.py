from sqlalchemy import Column, Integer, String, Date, Float
from database.db_manager import Base
from datetime import date

class Retroalimentacion(Base):
    __tablename__ = "retroalimentacion"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, default=date.today)
    energia = Column(Integer, default=5)
    productividad = Column(Integer, default=5)
    disciplina = Column(Integer, default=5)
    estres = Column(Integer, default=5)
    animo = Column(Integer, default=5)
    horas_sueno = Column(Float, default=7.0)
    comentario = Column(String, default="")
    momento_dia = Column(String, default="General") # Mañana, Tarde, Noche
