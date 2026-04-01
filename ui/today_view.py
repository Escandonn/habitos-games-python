from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QFrame
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
        header = QLabel("Tareas de Hoy")
        header.setObjectName("Header")
        
        date_label = QLabel(date.today().strftime("%A, %d %B %Y"))
        date_label.setStyleSheet("color: #777777; font-weight: bold;")
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(date_label)
        layout.addLayout(header_layout)

        # Habit List Area (The scroll_layout belongs here)
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(15)
        layout.addLayout(self.scroll_layout)

        self.refresh_habits()

    def create_habit_item(self, habit, record):
        widget = QFrame()
        widget.setObjectName("Card")
        widget.setMinimumHeight(80)
        
        layout = QHBoxLayout(widget)
        
        icon_lbl = QLabel(habit.icono)
        icon_lbl.setStyleSheet("font-size: 24px;")
        
        info_layout = QVBoxLayout()
        name_lbl = QLabel(habit.nombre)
        name_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #3c3c3c;")
        
        xp_val = XPService.calculate_xp(habit.prioridad, habit.intensidad)
        meta = QLabel(f"Nivel {habit.nivel_habito} • {xp_val} XP • {habit.meta_diaria}")
        meta.setStyleSheet("color: #777777; font-size: 13px;")
        
        info_layout.addWidget(name_lbl)
        info_layout.addWidget(meta)
        
        chk = QCheckBox()
        chk.setCursor(Qt.CursorShape.PointingHandCursor)
        chk.setChecked(record.completado)
        chk.setFixedSize(40, 40)
        chk.setStyleSheet("""
            QCheckBox::indicator {
                width: 30px; height: 30px;
                border: 2px solid #e5e5e5;
                border-radius: 8px;
            }
            QCheckBox::indicator:checked {
                background-color: #58cc02;
                border-color: #46a302;
            }
        """)
        chk.stateChanged.connect(lambda state: self.update_habit(habit, record, state))
        
        layout.addWidget(icon_lbl)
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(chk)
        
        return widget
        
    def refresh_habits(self):
        # Clear current layout
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        from services.habit_service import HabitService
        HabitService.ensure_today_records(self.db)

        regs = self.db.query(RegistroDiario).filter(RegistroDiario.fecha == date.today()).all()
        for r in regs:
            h = self.db.query(Habito).filter(Habito.id == r.habito_id).first()
            if h:
                item = self.create_habit_item(h, r)
                self.scroll_layout.addWidget(item)

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
            # Recalculate Total XP from all records
            total_regs = self.db.query(RegistroDiario.xp_ganada).all()
            user.xp_total = sum(x[0] for x in total_regs)
            
            # Check Level Up
            while True:
                level_up, new_level = XPService.check_level_up(user.xp_total, user.nivel)
                if level_up:
                    user.nivel = new_level
                else:
                    break
            
            self.db.commit()
            
            # Global refresh
            main_win = self.window()
            if hasattr(main_win, 'refresh_all_views'):
                main_win.refresh_all_views()
                    
            print(f"Hábito '{habit.nombre}' actualizado. XP ganada: {xp}. Nivel: {user.nivel if user else 1}")
