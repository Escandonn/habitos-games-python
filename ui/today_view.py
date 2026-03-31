from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QCheckBox, QPushButton, QFrame
from PyQt6.QtCore import Qt
from models.registro import RegistroDiario
from models.habito import Habito
from models.usuario import Usuario
from services.xp_service import XPService
from datetime import date

class TodayView(QWidget):
    def __init__(self, db_session):
        super().__init__()
        self.db = db_session
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        header = QLabel("Hábitos de Hoy")
        header.setObjectName("Header")
        
        date_label = QLabel(date.today().strftime("%A, %d %B %Y"))
        date_label.setStyleSheet("color: #94a3b8; font-size: 16px;")
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(date_label)
        layout.addLayout(header_layout)

        # Habits List
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(10)
        self.list_widget.setStyleSheet("background-color: transparent; border: none;")
        layout.addWidget(self.list_widget)

        self.refresh_habits()

    def refresh_habits(self):
        self.list_widget.clear()
        
        # Get habits for today
        habits = self.db.query(Habito).filter(Habito.activo == True).all()
        # Logic to filter by frequency (To be improved with custom frequency logic)
        
        for h in habits:
            # Check if record exists for today
            reg = self.db.query(RegistroDiario).filter(
                RegistroDiario.habito_id == h.id, 
                RegistroDiario.fecha == date.today()
            ).first()
            
            if not reg:
                reg = RegistroDiario(habito_id=h.id, fecha=date.today(), completado=False)
                self.db.add(reg)
                self.db.commit()

            self.add_habit_item(h, reg)

    def add_habit_item(self, habit, record):
        item = QListWidgetItem()
        widget = QFrame()
        widget.setObjectName("HabitItem")
        widget.setStyleSheet("background-color: #1e293b; border-radius: 8px; border: 1px solid #334155; padding: 5px;")
        
        layout = QHBoxLayout(widget)
        
        chk = QCheckBox(f" {habit.nombre}")
        chk.setChecked(record.completado)
        chk.setStyleSheet("font-size: 16px; font-weight: bold; border: none;")
        chk.stateChanged.connect(lambda state: self.update_habit(habit, record, state))
        
        meta = QLabel(f"[{habit.categoria}] • {habit.prioridad} • {habit.intensidad}")
        meta.setStyleSheet("color: #94a3b8; font-size: 12px; border: none;")
        
        layout.addWidget(chk)
        layout.addStretch()
        layout.addWidget(meta)
        
        item.setSizeHint(widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

    def update_habit(self, habit, record, state):
        completed = state == 2
        record.completado = completed
        
        # Calculate XP
        xp = 0
        if completed:
            xp = XPService.calculate_xp(habit.prioridad, habit.intensidad)
        
        record.xp_ganada = xp
        self.db.commit()

        # Update User XP
        user = self.db.query(Usuario).first()
        if user:
            # Recalculate Total XP from all records (more robust)
            total_xp = self.db.query(RegistroDiario.xp_ganada).all()
            user.xp_total = sum(x[0] for x in total_xp)
            
            # Check Level Up
            while True:
                level_up, new_level = XPService.check_level_up(user.xp_total, user.nivel)
                if level_up:
                    user.nivel = new_level
                else:
                    break
                    
            self.db.commit()
            
        print(f"Hábito '{habit.nombre}' actualizado. XP ganada: {xp}. Nivel: {user.nivel if user else 1}")
