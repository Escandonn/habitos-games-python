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
        cards_layout1 = QHBoxLayout()
        self.level_card = self.create_card("Nivel 1", "0 XP", "Racha 🔥 0")
        self.today_card = self.create_card("Hábitos Hoy", "0 / 0", "Progreso 0%")
        cards_layout1.addWidget(self.level_card)
        cards_layout1.addWidget(self.today_card)
        layout.addLayout(cards_layout1)

        cards_layout2 = QHBoxLayout()
        self.best_habit_card = self.create_card("Mejor Hábito", "Cargando...", "Top Semana")
        self.weekly_avg_card = self.create_card("Promedio Semanal", "Energía: 0", "Prod: 0 | Disc: 0")
        cards_layout2.addWidget(self.best_habit_card)
        cards_layout2.addWidget(self.weekly_avg_card)
        layout.addLayout(cards_layout2)

        # Progress Bar
        progress_layout = QVBoxLayout()
        self.progress_label = QLabel("Progreso de Nivel (0 / 100 XP)")
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(25)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        layout.addLayout(progress_layout)
        
        # Insights Panel
        self.insight_label = QLabel("Cargando insights...")
        self.insight_label.setWordWrap(True)
        self.insight_label.setStyleSheet("background-color: #e0f2fe; color: #0369a1; padding: 15px; border-radius: 10px; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.insight_label)

        # Weekly Activity (Chart)
        activity_label = QLabel("Actividad Semanal")
        activity_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(activity_label)
        
        from ui.stats_view import MplCanvas
        self.canvas = MplCanvas(self, width=5, height=3, dpi=100)
        self.canvas.axes.set_facecolor('#f7f7f7')
        self.canvas.figure.set_facecolor('#ffffff')
        layout.addWidget(self.canvas)

        self.refresh_stats()

    def create_card(self, title, sub, extra):
        card = QFrame()
        card.setMinimumHeight(120)
        card.setObjectName("Card")
        
        card_layout = QVBoxLayout(card)
        t_label = QLabel(title)
        t_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3c3c3c;")
        
        s_label = QLabel(sub)
        s_label.setStyleSheet("font-size: 16px; color: #777777;")
        
        e_label = QLabel(extra)
        e_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #58cc02;")
        
        card_layout.addWidget(t_label)
        card_layout.addWidget(s_label)
        card_layout.addWidget(e_label)
        
        return card

    def refresh_stats(self):
        from services.habit_service import HabitService
        HabitService.ensure_today_records(self.db)
        
        # Fetch user
        user = self.db.query(Usuario).first()
        if not user:
            user = Usuario(nombre="Usuario", xp_total=0, nivel=1, racha=0)
            self.db.add(user)
            self.db.commit()

        # Update Level Card
        layout = self.level_card.layout()
        layout.itemAt(0).widget().setText(f"Nivel {user.nivel}  |  💰 Oro: {user.oro_total}")
        layout.itemAt(1).widget().setText(f"{user.xp_total} XP Total")
        layout.itemAt(2).widget().setText(f"Racha Global 🔥 {user.racha}")

        # Update Progress bar
        next_threshold = XPService.get_level_threshold(user.nivel + 1)
        prev_threshold = XPService.get_level_threshold(user.nivel)
        progress = user.xp_total - prev_threshold
        range_xp = max(1, next_threshold - prev_threshold) # Prevent Div by 0
        
        self.progress_bar.setRange(0, range_xp)
        self.progress_bar.setValue(progress)
        self.progress_bar.setStyleSheet("color: black;")
        self.progress_label.setText(f"Progreso de Nivel ({progress} / {range_xp} XP para Nivel {user.nivel + 1})")

        # Update Today Card
        today_regs = self.db.query(RegistroDiario).filter(RegistroDiario.fecha == date.today()).all()
        total = len(today_regs)
        completed = sum(1 for r in today_regs if r.completado)
        perc = int((completed / total * 100)) if total > 0 else 0
        
        t_layout = self.today_card.layout()
        t_layout.itemAt(1).widget().setText(f"¡{completed} de {total} hábitos listos!")
        t_layout.itemAt(2).widget().setText(f"Progreso de hoy: {perc}%")
        
        from services.stats_service import StatsService
        
        # Generar Insights Analíticos IA
        new_insight = StatsService.generate_insights(self.db)
        self.insight_label.setText(new_insight)
        
        # Update Best Habit
        best = StatsService.get_best_habit(self.db)
        b_layout = self.best_habit_card.layout()
        b_layout.itemAt(1).widget().setText(f"⭐ {best}")
        
        # Update Weekly Activity Chart
        weekly_xp = StatsService.get_weekly_xp(self.db)
        if weekly_xp:
            self.canvas.axes.clear()
            dates = [d.strftime("%d/%m") for d in weekly_xp.keys()]
            values = list(weekly_xp.values())
            bars = self.canvas.axes.bar(dates, values, color='#1cb0f6', edgecolor='#1899d6', linewidth=2, zorder=3)
            self.canvas.axes.tick_params(axis='x', colors='#4b4b4b', labelsize=9)
            self.canvas.axes.tick_params(axis='y', colors='#4b4b4b')
            self.canvas.axes.spines['top'].set_visible(False)
            self.canvas.axes.spines['right'].set_visible(False)
            
            self.canvas.axes.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
            v_max = max(values) if values else 10
            self.canvas.axes.set_ylim(0, v_max * 1.25 if v_max > 0 else 10)
            
            for bar in bars:
                h = bar.get_height()
                if h > 0:
                    self.canvas.axes.text(bar.get_x() + bar.get_width() / 2, h + (v_max * 0.02), f'{int(h)} XP', ha='center', va='bottom', color='#3c3c3c', fontsize=9, fontweight='bold')
            
            self.canvas.figure.set_facecolor('#ffffff')
            self.canvas.axes.set_facecolor('#f7f7f7')
            self.canvas.figure.autofmt_xdate()
            self.canvas.draw()
