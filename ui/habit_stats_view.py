from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QFrame, QGridLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from models.habito import Habito
from services.stats_service import StatsService

class HabitStatsView(QWidget):
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
        header = QLabel("Análisis por Hábito")
        header.setObjectName("Header")
        
        self.habit_selector = QComboBox()
        self.habit_selector.setFixedWidth(250)
        self.habit_selector.currentIndexChanged.connect(self.refresh_stats)
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(self.habit_selector)
        layout.addLayout(header_layout)

        # Stats Cards
        self.cards_layout = QGridLayout()
        self.perc_card = self.create_stat_card("Cumplimiento", "0%", "Histórico")
        self.xp_card = self.create_stat_card("XP Generada", "0", "Total")
        self.level_card = self.create_stat_card("Nivel Hábito", "1", "Progreso")
        self.days_card = self.create_stat_card("Días Completados", "0", "Frecuencia")
        
        self.cards_layout.addWidget(self.perc_card, 0, 0)
        self.cards_layout.addWidget(self.xp_card, 0, 1)
        self.cards_layout.addWidget(self.level_card, 1, 0)
        self.cards_layout.addWidget(self.days_card, 1, 1)
        layout.addLayout(self.cards_layout)

        # Chart
        self.canvas = MplCanvas(self, width=5, height=3, dpi=100)
        self.canvas.axes.set_facecolor('#f7f7f7')
        self.canvas.figure.set_facecolor('#ffffff')
        layout.addWidget(self.canvas)

        self.refresh_habit_list()

    def create_stat_card(self, title, val, extra):
        card = QFrame()
        card.setObjectName("Card")
        l = QVBoxLayout(card)
        t = QLabel(title); t.setStyleSheet("color: #777777; font-size: 14px;")
        v = QLabel(val); v.setStyleSheet("color: #1cb0f6; font-size: 24px; font-weight: bold;")
        e = QLabel(extra); e.setStyleSheet("color: #58cc02; font-size: 12px; font-weight: bold;")
        l.addWidget(t); l.addWidget(v); l.addWidget(e)
        return card

    def refresh_habit_list(self):
        self.habit_selector.blockSignals(True)
        self.habit_selector.clear()
        habits = self.db.query(Habito).all()
        for h in habits:
            self.habit_selector.addItem(f"{h.icono} {h.nombre}", h.id)
        self.habit_selector.blockSignals(False)

    def refresh_stats(self):
        # Do NOT call refresh_habit_list here, as it resets the index to 0!
        habit_id = self.habit_selector.currentData()
        if not habit_id: return

        stats = StatsService.get_habit_stats(self.db, habit_id)
        habit = self.db.query(Habito).filter(Habito.id == habit_id).first()

        # Update cards
        self.perc_card.layout().itemAt(1).widget().setText(f"{stats['percentage']:.1f}%")
        self.xp_card.layout().itemAt(1).widget().setText(f"{stats['xp']} XP")
        self.level_card.layout().itemAt(1).widget().setText(f"Nivel {habit.nivel_habito}")
        self.days_card.layout().itemAt(1).widget().setText(f"{stats['completed']} días")

        # Real chart update: Daily completion in current week
        self.canvas.axes.clear()
        
        from models.registro import RegistroDiario
        from datetime import date, timedelta
        
        last_7_days = [date.today() - timedelta(days=i) for i in range(6, -1, -1)]
        day_labels = [d.strftime("%a") for d in last_7_days]
        daily_comp = []
        
        for d in last_7_days:
            reg = self.db.query(RegistroDiario).filter(
                RegistroDiario.habito_id == habit_id, 
                RegistroDiario.fecha == d
            ).first()
            daily_comp.append(1 if reg and reg.completado else 0)
            
        bars = self.canvas.axes.bar(day_labels, daily_comp, color='#1cb0f6', edgecolor='#1899d6', linewidth=2, zorder=3)
        self.canvas.axes.set_title(f"Actividad Semanal: {habit.nombre}", color='#3c3c3c', fontweight='bold')
        self.canvas.axes.tick_params(axis='both', colors='#4b4b4b')
        
        self.canvas.axes.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
        self.canvas.axes.set_ylim(0, 1.3)
        self.canvas.axes.set_yticks([0, 1])
        self.canvas.axes.set_yticklabels(['Fallo', 'Éxito'])
        
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                self.canvas.axes.text(bar.get_x() + bar.get_width() / 2, h + 0.05, 'OK', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#58cc02')
                
        self.canvas.axes.spines['top'].set_visible(False)
        self.canvas.axes.spines['right'].set_visible(False)
        self.canvas.figure.set_facecolor('#ffffff')
        self.canvas.axes.set_facecolor('#f7f7f7')
        self.canvas.draw()

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
