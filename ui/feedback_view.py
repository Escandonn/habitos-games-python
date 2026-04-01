from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QGridLayout, QSlider, QComboBox, QTextEdit, QDoubleSpinBox, QPushButton
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

        # Momento del día
        form_layout.addWidget(QLabel("Momento del Día:"), 1, 0)
        self.momento_input = QComboBox()
        self.momento_input.addItems(["🌅 Mañana", "☀️ Tarde", "🌙 Noche"])
        form_layout.addWidget(self.momento_input, 1, 1)

        # Productivity level
        form_layout.addWidget(QLabel("Productividad (1-10):"), 2, 0)
        self.prod_slider = QSlider(Qt.Orientation.Horizontal)
        self.prod_slider.setRange(1, 10)
        self.prod_slider.setValue(5)
        form_layout.addWidget(self.prod_slider, 2, 1)

        # Discipline level
        form_layout.addWidget(QLabel("Disciplina (1-10):"), 2, 0)
        self.disc_slider = QSlider(Qt.Orientation.Horizontal)
        self.disc_slider.setRange(1, 10)
        self.disc_slider.setValue(5)
        form_layout.addWidget(self.disc_slider, 2, 1)

        # Stress level
        form_layout.addWidget(QLabel("Estrés (1-10):"), 3, 0)
        self.stress_slider = QSlider(Qt.Orientation.Horizontal)
        self.stress_slider.setRange(1, 10)
        self.stress_slider.setValue(3)
        form_layout.addWidget(self.stress_slider, 3, 1)

        # Mood level
        form_layout.addWidget(QLabel("Estado de Ánimo (1-10):"), 4, 0)
        self.mood_slider = QSlider(Qt.Orientation.Horizontal)
        self.mood_slider.setRange(1, 10)
        self.mood_slider.setValue(7)
        form_layout.addWidget(self.mood_slider, 4, 1)

        # Sleep hours
        from PyQt6.QtWidgets import QDoubleSpinBox
        form_layout.addWidget(QLabel("Horas de Sueño:"), 5, 0)
        self.sleep_input = QDoubleSpinBox()
        self.sleep_input.setRange(0, 24)
        self.sleep_input.setValue(7.5)
        form_layout.addWidget(self.sleep_input, 5, 1)

        # Review
        form_layout.addWidget(QLabel("Comentarios del Día:"), 6, 0)
        self.comments_input = QTextEdit()
        self.comments_input.setPlaceholderText("¿Qué aprendiste hoy? ¿Qué podrías mejorar mañana?")
        form_layout.addWidget(self.comments_input, 6, 1)

        # Save Button
        self.btn_save = QPushButton("✅ Guardar Reflexión Diaria PRO")
        self.btn_save.setStyleSheet("background-color: #ec4899; font-weight: bold; border-radius: 8px; padding: 12px;")
        self.btn_save.clicked.connect(self.save_feedback)
        form_layout.addWidget(self.btn_save, 7, 0, 1, 2)

        layout.addWidget(form_frame)

    def save_feedback(self):
        momento = self.momento_input.currentText()
        # Check if feedback already exists for today and this specific moment
        feedback = self.db.query(Retroalimentacion).filter(
            Retroalimentacion.fecha == date.today(),
            Retroalimentacion.momento_dia == momento
        ).first()
        
        if not feedback:
            feedback = Retroalimentacion(fecha=date.today(), momento_dia=momento)
            self.db.add(feedback)

        feedback.energia = self.energy_slider.value()
        feedback.productividad = self.prod_slider.value()
        feedback.disciplina = self.disc_slider.value()
        feedback.estres = self.stress_slider.value()
        feedback.animo = self.mood_slider.value()
        feedback.horas_sueno = self.sleep_input.value()
        feedback.comentario = self.comments_input.toPlainText()
        
        self.db.commit()
        print(f"Retroalimentación {momento} Guardada.")
        
        main_win = self.window()
        if hasattr(main_win, 'refresh_all_views'):
            main_win.refresh_all_views()
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "¡Excelente!", f"Tu reflexión de la {momento} ha sido guardada.")
            main_win.switch_view(0)
