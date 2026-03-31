from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from models.usuario import Usuario
from models.registro import RegistroDiario
from services.xp_service import XPService
from datetime import date

class DashboardView(QWidget):
    def __init__(self, db_session):
        super().__init__()
        self.db = db_session
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Header
        header = QLabel("Dashboard")
        header.setObjectName("Header")
        layout.addWidget(header)

        # Stats Cards
        cards_layout = QHBoxLayout()
        self.level_card = self.create_card("Nivel 1", "0 XP", "Racha 🔥 0")
        self.today_card = self.create_card("Hábitos Hoy", "0 / 0", "Progreso 0%")
        cards_layout.addWidget(self.level_card)
        cards_layout.addWidget(self.today_card)
        layout.addLayout(cards_layout)

        # Progress Bar
        progress_layout = QVBoxLayout()
        self.progress_label = QLabel("Progreso de Nivel (0 / 100 XP)")
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(25)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        layout.addLayout(progress_layout)

        # Weekly Activity (Placeholder for Chart)
        activity_label = QLabel("Actividad Semanal")
        activity_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(activity_label)
        
        self.activity_frame = QFrame()
        self.activity_frame.setFixedHeight(250)
        self.activity_frame.setStyleSheet("background-color: #1e293b; border-radius: 10px; border: 1px solid #334155;")
        layout.addWidget(self.activity_frame)

        self.refresh_stats()

    def create_card(self, title, sub, extra):
        card = QFrame()
        card.setMinimumHeight(150)
        card.setStyleSheet("background-color: #1e293b; border-radius: 10px; border: 1px solid #334155;")
        
        card_layout = QVBoxLayout(card)
        t_label = QLabel(title)
        t_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #60a5fa;")
        
        s_label = QLabel(sub)
        s_label.setStyleSheet("font-size: 16px; color: #94a3b8;")
        
        e_label = QLabel(extra)
        e_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #fbbf24;")
        
        card_layout.addWidget(t_label)
        card_layout.addWidget(s_label)
        card_layout.addWidget(e_label)
        
        return card

    def refresh_stats(self):
        # Fetch user
        user = self.db.query(Usuario).first()
        if not user:
            user = Usuario(nombre="Usuario", xp_total=0, nivel=1, racha=0)
            self.db.add(user)
            self.db.commit()

        # Update Level Card
        # Re-fetch labels in level_card
        layout = self.level_card.layout()
        layout.itemAt(0).widget().setText(f"Nivel {user.nivel}")
        layout.itemAt(1).widget().setText(f"{user.xp_total} XP Total")
        layout.itemAt(2).widget().setText(f"Racha 🔥 {user.racha}")

        # Update Progress bar
        next_threshold = XPService.get_level_threshold(user.nivel + 1)
        prev_threshold = XPService.get_level_threshold(user.nivel)
        progress = user.xp_total - prev_threshold
        range_xp = next_threshold - prev_threshold
        
        self.progress_bar.setRange(0, range_xp)
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"Progreso de Nivel ({progress} / {range_xp} XP para Nivel {user.nivel + 1})")

        # Update Today Card
        today_regs = self.db.query(RegistroDiario).filter(RegistroDiario.fecha == date.today()).all()
        total = len(today_regs)
        completed = sum(1 for r in today_regs if r.completado)
        perc = int((completed / total * 100)) if total > 0 else 0
        
        t_layout = self.today_card.layout()
        t_layout.itemAt(0).widget().setText(f"Hábitos Hoy")
        t_layout.itemAt(1).widget().setText(f"{completed} / {total} Completados")
        t_layout.itemAt(2).widget().setText(f"Progreso {perc}%")
