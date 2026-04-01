import pandas as pd
from sqlalchemy.orm import Session
from models.habito import Habito
from models.registro import RegistroDiario
from models.retroalimentacion import Retroalimentacion

class ExcelService:
    @staticmethod
    def export_all_data(db: Session, filename="reporte_habitos_PRO.xlsx"):
        # Habitos
        habitos = db.query(Habito).all()
        habitos_df = pd.DataFrame([{
            "Nombre": h.nombre,
            "Categoría": h.categoria,
            "Prioridad": h.prioridad,
            "Intensidad": h.intensidad,
            "Duración (min)": h.duracion_min,
            "Dificultad": h.dificultad,
            "Nivel Hábito": h.nivel_habito,
            "Meta": h.meta_diaria,
            "Inicio": h.fecha_inicio,
            "Activo": h.activo
        } for h in habitos])
        
        # Registros
        registros = db.query(RegistroDiario).all()
        registros_df = pd.DataFrame([{
            "Fecha": r.fecha,
            "Hábito": db.query(Habito.nombre).filter(Habito.id == r.habito_id).scalar(),
            "Completado": r.completado,
            "XP": r.xp_ganada,
            "Minutos Invertidos": r.tiempo_invertido,
            "Notas": r.notas_dia
        } for r in registros])
        
        # Retroalimentacion
        retro = db.query(Retroalimentacion).all()
        retro_df = pd.DataFrame([{
            "Fecha": r.fecha,
            "Energía": r.energia,
            "Productividad": r.productividad,
            "Disciplina": r.disciplina,
            "Estrés": r.estres,
            "Ánimo": r.animo,
            "Sueño (hrs)": r.horas_sueno,
            "Comentario": r.comentario
        } for r in retro])
        
        with pd.ExcelWriter(filename) as writer:
            habitos_df.to_excel(writer, sheet_name="Habitos", index=False)
            registros_df.to_excel(writer, sheet_name="Registros", index=False)
            retro_df.to_excel(writer, sheet_name="Retroalimentacion", index=False)
            
        return filename
