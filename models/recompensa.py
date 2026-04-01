from sqlalchemy import Column, Integer, String, Boolean
from database.db_manager import Base

class Recompensa(Base):
    __tablename__ = "recompensas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    costo_oro = Column(Integer, default=100)
    icono = Column(String, default="🎁")
    comprada = Column(Boolean, default=False)
