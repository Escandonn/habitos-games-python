from sqlalchemy import Column, Integer, String
from database.db_manager import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, default="Usuario")
    xp_total = Column(Integer, default=0)
    nivel = Column(Integer, default=1)
    racha = Column(Integer, default=0)
