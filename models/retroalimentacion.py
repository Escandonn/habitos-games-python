from sqlalchemy import Column, Integer, String, Date
from database.db_manager import Base
from datetime import date

class Retroalimentacion(Base):
    __tablename__ = "retroalimentacion"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, default=date.today)
    energia = Column(Integer, default=5)
    productividad = Column(Integer, default=5)
    disciplina = Column(Integer, default=5)
    comentario = Column(String, default="")
