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
        form_frame.setStyleSheet("background-color: #1e293b; border-radius: 12px; border: 1px solid #334155;")
        form_layout = QGridLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        form_layout.addWidget(QLabel("Nombre del Hábito:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ej: Leer 10 páginas")
        form_layout.addWidget(self.name_input, 0, 1)

        form_layout.addWidget(QLabel("Categoría:"), 1, 0)
        self.cat_input = QComboBox()
        self.cat_input.addItems(["Salud", "Estudio", "Finanzas", "Personal", "Social", "Mental", "Trabajo", "Otros"])
        form_layout.addWidget(self.cat_input, 1, 1)

        form_layout.addWidget(QLabel("Prioridad:"), 2, 0)
        self.prior_input = QComboBox()
        self.prior_input.addItems(["Baja", "Media", "Alta"])
        form_layout.addWidget(self.prior_input, 2, 1)

        form_layout.addWidget(QLabel("Intensidad:"), 3, 0)
        self.intens_input = QComboBox()
        self.intens_input.addItems(["Baja", "Media", "Alta"])
        form_layout.addWidget(self.intens_input, 3, 1)

        form_layout.addWidget(QLabel("Frecuencia:"), 4, 0)
        self.freq_input = QComboBox()
        self.freq_input.addItems(["Diario", "Semanal", "Mensual"])
        form_layout.addWidget(self.freq_input, 4, 1)

        form_layout.addWidget(QLabel("Fecha de Inicio:"), 5, 0)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        form_layout.addWidget(self.date_input, 5, 1)

        self.btn_save = QPushButton("💾 Guardar Hábito")
        self.btn_save.setStyleSheet("background-color: #3b82f6; font-weight: bold; border-radius: 8px; padding: 10px;")
        self.btn_save.clicked.connect(self.save_habit)
        form_layout.addWidget(self.btn_save, 6, 0, 1, 2)

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

        habit = Habito(
            nombre=name,
            categoria=self.cat_input.currentText(),
            prioridad=self.prior_input.currentText(),
            intensidad=self.intens_input.currentText(),
            frecuencia=self.freq_input.currentText(),
            fecha_inicio=self.date_input.date().toPyDate(),
            activo=True
        )
        self.db.add(habit)
        self.db.commit()
        
        self.name_input.clear()
        print(f"Hábito '{name}' guardado correctamente.")
