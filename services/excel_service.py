import pandas as pd
from sqlalchemy.orm import Session
from models.habito import Habito
from models.registro import RegistroDiario
from models.retroalimentacion import Retroalimentacion

class ExcelService:
    @staticmethod
    def export_all_data(db: Session, filename="reporte_habitos.xlsx"):
        # Fetch habits
        habitos = db.query(Habito).all()
        habitos_df = pd.DataFrame([{
            "Nombre": h.nombre,
            "Categoría": h.categoria,
            "Prioridad": h.prioridad,
            "Intensidad": h.intensidad,
            "Frecuencia": h.frecuencia,
            "Inicio": h.fecha_inicio,
            "Activo": h.activo
        } for h in habitos])
        
        # Fetch recordings
        registros = db.query(RegistroDiario).all()
        registros_df = pd.DataFrame([{
            "Fecha": r.fecha,
            "Hábito": db.query(Habito.nombre).filter(Habito.id == r.habito_id).first()[0],
            "Completado": r.completado,
            "XP": r.xp_ganada
        } for r in registros])
        
        # Fetch feedback
        retro = db.query(Retroalimentacion).all()
        retro_df = pd.DataFrame([{
            "Fecha": r.fecha,
            "Energía": r.energia,
            "Productividad": r.productividad,
            "Disciplina": r.disciplina,
            "Comentario": r.comentario
        } for r in retro])
        
        # Save to Excel
        with pd.ExcelWriter(filename) as writer:
            habitos_df.to_excel(writer, sheet_name="Habitos", index=False)
            registros_df.to_excel(writer, sheet_name="Registros", index=False)
            retro_df.to_excel(writer, sheet_name="Retroalimentacion", index=False)
            
        return filename
