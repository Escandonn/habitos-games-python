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
        self.xp_canvas.axes.set_title("XP Ganada esta Semana", color='#3c3c3c', fontweight='bold')
        self.xp_canvas.axes.set_facecolor('#f7f7f7')
        self.xp_canvas.figure.set_facecolor('#ffffff')
        charts_layout.addWidget(self.xp_canvas)

        # 2. Daily Energy Trends
        self.energy_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.energy_canvas.axes.set_title("Niveles de Energía", color='#3c3c3c', fontweight='bold')
        self.energy_canvas.axes.set_facecolor('#f7f7f7')
        self.energy_canvas.figure.set_facecolor('#ffffff')
        charts_layout.addWidget(self.energy_canvas)

        layout.addLayout(charts_layout)

        # Summary Labels
        summary_layout = QHBoxLayout()
        self.xp_card = self.create_stat_card("XP Total", "0")
        self.energy_card = self.create_stat_card("Energía Promedio", "0")
        summary_layout.addWidget(self.xp_card)
        summary_layout.addWidget(self.energy_card)

        layout.addLayout(summary_layout)

        self.refresh_charts()

    def create_stat_card(self, label, value):
        card = QFrame()
        card.setObjectName("Card")
        card.setStyleSheet("#Card { background-color: #ffffff; border: 2px solid #e5e5e5; border-radius: 15px; padding: 15px; }")
        l = QVBoxLayout(card)
        lbl = QLabel(label); lbl.setStyleSheet("color: #777777; font-size: 14px;")
        val = QLabel(value); val.setStyleSheet("color: #3c3c3c; font-size: 24px; font-weight: bold;")
        l.addWidget(lbl); l.addWidget(val)
        return card

    def refresh_charts(self):
        # Weekly XP
        weekly_xp = StatsService.get_weekly_xp(self.db)
        if weekly_xp:
            self.xp_canvas.axes.clear()
            dates = [d.strftime("%d/%m") for d in weekly_xp.keys()]
            values = list(weekly_xp.values())
            self.xp_canvas.axes.bar(dates, values, color='#58cc02', edgecolor='#46a302', linewidth=2)
            self.xp_canvas.axes.set_title("Progreso Semanal (XP)", color='#3c3c3c', fontweight='bold')
            self.xp_canvas.axes.tick_params(axis='both', colors='#4b4b4b')
            self.xp_canvas.figure.set_facecolor('#ffffff')
            self.xp_canvas.axes.set_facecolor('#f7f7f7')
            self.xp_canvas.draw()
            
            total_xp = sum(values)
            self.xp_card.layout().itemAt(1).widget().setText(f"{total_xp} XP")

        # Energy, Prod, Discipline trends
        energy_data = StatsService.get_energy_trends(self.db)
        if energy_data:
            from collections import defaultdict
            daily_avg = defaultdict(lambda: {'e': [], 'p': [], 'd': []})
            for r in energy_data:
                daily_avg[r.fecha]['e'].append(r.energia)
                daily_avg[r.fecha]['p'].append(r.productividad)
                daily_avg[r.fecha]['d'].append(r.disciplina) # o usar estres si se prefiere
            
            dates = [d.strftime("%d/%m") for d in sorted(daily_avg.keys())]
            energies = [sum(daily_avg[k]['e'])/len(daily_avg[k]['e']) for k in sorted(daily_avg.keys())]
            prods = [sum(daily_avg[k]['p'])/len(daily_avg[k]['p']) for k in sorted(daily_avg.keys())]
            discs = [sum(daily_avg[k]['d'])/len(daily_avg[k]['d']) for k in sorted(daily_avg.keys())]
            
            self.energy_canvas.figure.clf()
            
            # Subplot 1: Energía
            ax1 = self.energy_canvas.figure.add_subplot(311)
            ax1.plot(dates, energies, color='#58cc02', marker='o', linewidth=2)
            ax1.set_title("⚡ Energía", color='#3c3c3c', loc='left', fontsize=10, fontweight='bold')
            
            # Subplot 2: Productividad
            ax2 = self.energy_canvas.figure.add_subplot(312)
            ax2.plot(dates, prods, color='#1cb0f6', marker='o', linewidth=2)
            ax2.set_title("⚙️ Productividad", color='#3c3c3c', loc='left', fontsize=10, fontweight='bold')
            
            # Subplot 3: Disciplina
            # Reusing pink/purple for discipline
            ax3 = self.energy_canvas.figure.add_subplot(313)
            ax3.plot(dates, discs, color='#ce82ff', marker='o', linewidth=2)
            ax3.set_title("🛡️ Disciplina", color='#3c3c3c', loc='left', fontsize=10, fontweight='bold')
            
            for ax in [ax1, ax2, ax3]:
                ax.set_ylim(0, 11)
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                ax.tick_params(axis='both', colors='#4b4b4b', labelsize=8)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.set_facecolor('#f7f7f7')
            
            self.energy_canvas.figure.set_facecolor('#ffffff')
            self.energy_canvas.figure.tight_layout()
            self.energy_canvas.draw()
            
            avg_energy = sum(energies) / len(energies) if energies else 0
            self.energy_card.layout().itemAt(1).widget().setText(f"{avg_energy:.1f} / 10")

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
