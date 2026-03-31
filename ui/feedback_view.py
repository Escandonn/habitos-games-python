from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QTextEdit, QPushButton, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from models.retroalimentacion import Retroalimentacion
from datetime import date

class FeedbackView(QWidget):
    def __init__(self, db_session):
        super().__init__()
        self.db = db_session
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30,30,30,30)
        layout.setSpacing(25)

        # Header
        header = QLabel("Retroalimentación Diaria")
        header.setObjectName("Header")
        layout.addWidget(header)

        # Form
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #1e293b; border-radius: 12px; border: 1px solid #334155;")
        form_layout = QGridLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(20)

        # Energy level
        form_layout.addWidget(QLabel("Nivel de Energía (1-10):"), 0, 0)
        self.energy_slider = QSlider(Qt.Orientation.Horizontal)
        self.energy_slider.setRange(1, 10)
        self.energy_slider.setValue(5)
        form_layout.addWidget(self.energy_slider, 0, 1)

        # Productivity level
        form_layout.addWidget(QLabel("Productividad (1-10):"), 1, 0)
        self.prod_slider = QSlider(Qt.Orientation.Horizontal)
        self.prod_slider.setRange(1, 10)
        self.prod_slider.setValue(5)
        form_layout.addWidget(self.prod_slider, 1, 1)

        # Discipline level
        form_layout.addWidget(QLabel("Disciplina (1-10):"), 2, 0)
        self.disc_slider = QSlider(Qt.Orientation.Horizontal)
        self.disc_slider.setRange(1, 10)
        self.disc_slider.setValue(5)
        form_layout.addWidget(self.disc_slider, 2, 1)

        # Review
        form_layout.addWidget(QLabel("Comentarios del Día:"), 3, 0)
        self.comments_input = QTextEdit()
        self.comments_input.setPlaceholderText("¿Qué aprendiste hoy? ¿Qué podrías mejorar mañana?")
        form_layout.addWidget(self.comments_input, 3, 1)

        # Save Button
        self.btn_save = QPushButton("✅ Guardar Reflexión Diaria")
        self.btn_save.setStyleSheet("background-color: #3b82f6; font-weight: bold; border-radius: 8px; padding: 12px;")
        self.btn_save.clicked.connect(self.save_feedback)
        form_layout.addWidget(self.btn_save, 4, 0, 1, 2)

        layout.addWidget(form_frame)

    def save_feedback(self):
        # Check if feedback already exists for today
        feedback = self.db.query(Retroalimentacion).filter(Retroalimentacion.fecha == date.today()).first()
        if not feedback:
            feedback = Retroalimentacion(fecha=date.today())
            self.db.add(feedback)

        feedback.energia = self.energy_slider.value()
        feedback.productividad = self.prod_slider.value()
        feedback.disciplina = self.disc_slider.value()
        feedback.comentario = self.comments_input.toPlainText()
        
        self.db.commit()
        print("Retroalimentación guardada.")
