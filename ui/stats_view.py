from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from services.stats_service import StatsService

class StatsView(QWidget):
    def __init__(self, db_session):
        super().__init__()
        self.db = db_session
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Header
        header = QLabel("Estadísticas y Análisis")
        header.setObjectName("Header")
        layout.addWidget(header)

        # Charts Area
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)

        # 1. Weekly XP Chart
        self.xp_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.xp_canvas.axes.set_title("XP Ganada esta Semana", color='#60a5fa')
        self.xp_canvas.axes.set_facecolor('#1e293b')
        self.xp_canvas.figure.set_facecolor('#0f172a')
        charts_layout.addWidget(self.xp_canvas)

        # 2. Daily Energy Trends
        self.energy_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.energy_canvas.axes.set_title("Niveles de Energía", color='#60a5fa')
        self.energy_canvas.axes.set_facecolor('#1e293b')
        self.energy_canvas.figure.set_facecolor('#0f172a')
        charts_layout.addWidget(self.energy_canvas)

        layout.addLayout(charts_layout)

        # Summary Labels
        summary_frame = QFrame()
        summary_frame.setStyleSheet("background-color: #1e293b; border-radius: 10px; border: 1px solid #334155; padding: 20px;")
        summary_layout = QHBoxLayout(summary_frame)
        self.total_xp_lbl = QLabel("XP Total: 0")
        self.total_xp_lbl.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.avg_energy_lbl = QLabel("Energía Promedio: 0")
        self.avg_energy_lbl.setStyleSheet("font-size: 18px; font-weight: bold;")
        summary_layout.addWidget(self.total_xp_lbl)
        summary_layout.addWidget(self.avg_energy_lbl)

        layout.addWidget(summary_frame)

        self.refresh_charts()

    def refresh_charts(self):
        # Weekly XP
        weekly_xp = StatsService.get_weekly_xp(self.db)
        dates = list(weekly_xp.keys())
        values = list(weekly_xp.values())
        
        self.xp_canvas.axes.clear()
        self.xp_canvas.axes.bar([str(d) for d in dates], values, color='#3b82f6')
        self.xp_canvas.axes.set_title("XP Semanal", color='white')
        self.xp_canvas.draw()

        # Energy trends
        energy_data = StatsService.get_energy_trends(self.db)
        if energy_data:
            dates = [str(r[0]) for r in energy_data]
            energies = [r[1] for r in energy_data]
            prods = [r[2] for r in energy_data]
            
            self.energy_canvas.axes.clear()
            self.energy_canvas.axes.plot(dates, energies, label="Energía", color='#ec4899', marker='o')
            self.energy_canvas.axes.plot(dates, prods, label="Prod.", color='#f59e0b', marker='x')
            self.energy_canvas.axes.legend()
            self.energy_canvas.axes.set_title("Tendencias Diarias", color='white')
            self.energy_canvas.draw()

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
