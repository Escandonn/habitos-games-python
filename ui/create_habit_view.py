from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QScrollArea, QFrame, QGridLayout, QDateEdit
from PyQt6.QtCore import Qt, QDate
from models.habito import Habito
from datetime import date

class CreateHabitView(QWidget):
    def __init__(self, db_session):
        super().__init__()
        self.db = db_session
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header = QLabel("Crear Hábito")
        header.setObjectName("Header")
        layout.addWidget(header)

        # Form
        form_frame = QFrame()
        form_frame.setObjectName("Card")
        form_layout = QGridLayout(form_frame)
        form_layout.setSpacing(15)

        form_layout.addWidget(QLabel("Nombre del Hábito:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ej: 🏃 Deporte")
        form_layout.addWidget(self.name_input, 0, 1)

        form_layout.addWidget(QLabel("Categoría:"), 1, 0)
        self.cat_input = QComboBox()
        self.cat_input.addItems(["Salud", "Productividad", "Mente", "Finanzas", "Social", "Hogar"])
        form_layout.addWidget(self.cat_input, 1, 1)

        form_layout.addWidget(QLabel("Prioridad:"), 2, 0)
        self.prior_input = QComboBox()
        self.prior_input.addItems(["Baja", "Media", "Alta", "Crítica"])
        form_layout.addWidget(self.prior_input, 2, 1)

        form_layout.addWidget(QLabel("Intensidad:"), 3, 0)
        self.intens_input = QComboBox()
        self.intens_input.addItems(["Ligero", "Moderado", "Intenso", "Extremo"])
        form_layout.addWidget(self.intens_input, 3, 1)

        form_layout.addWidget(QLabel("Frecuencia Diaria:"), 4, 0)
        self.freq_input = QComboBox()
        self.freq_input.addItems(["1 vez", "2 veces", "3 veces", "Mas de 3"])
        form_layout.addWidget(self.freq_input, 4, 1)

        form_layout.addWidget(QLabel("Fecha de Inicio:"), 5, 0)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        form_layout.addWidget(self.date_input, 5, 1)

        form_layout.addWidget(QLabel("Meta Diaria:"), 6, 0)
        self.goal_input = QLineEdit()
        self.goal_input.setPlaceholderText("Ej: 50 flexiones")
        form_layout.addWidget(self.goal_input, 6, 1)

        form_layout.addWidget(QLabel("Duración (min):"), 7, 0)
        self.dur_input = QLineEdit()
        self.dur_input.setPlaceholderText("Ej: 30")
        form_layout.addWidget(self.dur_input, 7, 1)

        form_layout.addWidget(QLabel("Color (Hex):"), 8, 0)
        self.color_input = QLineEdit()
        self.color_input.setText("#58cc02")
        form_layout.addWidget(self.color_input, 8, 1)

        self.btn_save = QPushButton("💾 GUARDAR HÁBITO")
        self.btn_save.setObjectName("PrimaryAction")
        self.btn_save.clicked.connect(self.save_habit)
        form_layout.addWidget(self.btn_save, 9, 0, 1, 2)

        layout.addWidget(form_frame)

        # Suggestions
        layout.addWidget(QLabel("Sugerencias de Hábitos Comunes"))
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        grid = QGridLayout(container)
        grid.setSpacing(10)
        
        suggestions = [
            "🏃 Deporte", "🏋️ Gimnasio", "🚶 Caminar", "🧘 Meditación", "💧 Tomar agua",
            "🥗 Comer sano", "📚 Estudiar", "💻 Programar", "📖 Leer", "🌍 Inglés",
            "💰 Ahorrar", "🧹 Limpiar", "📞 Llamar padres", "🧩 Resolver problemas", "📧 Correos"
        ]
        
        for i, s in enumerate(suggestions):
            btn = QPushButton(s)
            btn.setStyleSheet("background-color: #1e293b; color: #f8fafc; text-align: center; border-radius: 5px; border: 1px solid #334155;")
            btn.clicked.connect(lambda _, x=s: self.name_input.setText(x))
            grid.addWidget(btn, i // 4, i % 4)
            
        scroll.setWidget(container)
        layout.addWidget(scroll)

    def save_habit(self):
        name = self.name_input.text()
        if not name: return

        # Extract icon from name if possible (e.g., "🏃 Deporte")
        icon = "🎯"
        if len(name) > 2 and name[0] in "🏃🏋️🧘💧📚💻📖🌍💰🧹📞🧩📧🌞🩺🥗🚶🚴🧎🫀🧴🪥🌞🫁🩺":
            icon = name[0]
            name = name[2:].strip()

        try:
            dur = int(self.dur_input.text()) if self.dur_input.text() else 0
        except: dur = 0

        habit = Habito(
            nombre=name,
            categoria=self.cat_input.currentText(),
            prioridad=self.prior_input.currentText(),
            intensidad=self.intens_input.currentText(),
            frecuencia=self.freq_input.currentText(),
            fecha_inicio=self.date_input.date().toPyDate(),
            meta_diaria=self.goal_input.text(),
            duracion_min=dur,
            color=self.color_input.text(),
            icono=icon,
            activo=True
        )
        self.db.add(habit)
        self.db.commit()
        
        self.name_input.clear()
        self.goal_input.clear()
        self.dur_input.clear()
        print(f"Hábito '{name}' guardado con éxito.")
        
        main_win = self.window()
        if hasattr(main_win, 'refresh_all_views'):
            main_win.refresh_all_views()
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "¡Éxito!", f"El hábito '{name}' ha sido guardado y ya está activo.")
            main_win.switch_view(0)
