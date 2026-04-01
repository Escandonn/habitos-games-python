from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QPushButton, QScrollArea, QDialog, QGridLayout,
                             QSlider, QComboBox, QTextEdit, QDoubleSpinBox, QMessageBox)
from PyQt6.QtCore import Qt
from models.retroalimentacion import Retroalimentacion

class EditFeedbackDialog(QDialog):
    def __init__(self, db, record_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.record_id = record_id
        self.record = self.db.query(Retroalimentacion).filter(Retroalimentacion.id == record_id).first()
        self.setWindowTitle("Editar Retroalimentación")
        self.resize(400, 500)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_frame = QFrame()
        form_layout = QGridLayout(form_frame)
        form_layout.setSpacing(15)

        form_layout.addWidget(QLabel("Momento:"), 0, 0)
        self.momento_input = QComboBox()
        self.momento_input.addItems(["🌅 Mañana", "☀️ Tarde", "🌙 Noche"])
        form_layout.addWidget(self.momento_input, 0, 1)

        form_layout.addWidget(QLabel("Energía:"), 1, 0)
        self.energy_slider = QSlider(Qt.Orientation.Horizontal)
        self.energy_slider.setRange(1, 10)
        form_layout.addWidget(self.energy_slider, 1, 1)

        form_layout.addWidget(QLabel("Productividad:"), 2, 0)
        self.prod_slider = QSlider(Qt.Orientation.Horizontal)
        self.prod_slider.setRange(1, 10)
        form_layout.addWidget(self.prod_slider, 2, 1)

        form_layout.addWidget(QLabel("Disciplina:"), 3, 0)
        self.disc_slider = QSlider(Qt.Orientation.Horizontal)
        self.disc_slider.setRange(1, 10)
        form_layout.addWidget(self.disc_slider, 3, 1)

        form_layout.addWidget(QLabel("Estrés (1 = Relajado):"), 4, 0)
        self.stress_slider = QSlider(Qt.Orientation.Horizontal)
        self.stress_slider.setRange(1, 10)
        form_layout.addWidget(self.stress_slider, 4, 1)

        form_layout.addWidget(QLabel("Ánimo (10 = Feliz):"), 5, 0)
        self.mood_slider = QSlider(Qt.Orientation.Horizontal)
        self.mood_slider.setRange(1, 10)
        form_layout.addWidget(self.mood_slider, 5, 1)

        form_layout.addWidget(QLabel("Horas de Sueño:"), 6, 0)
        self.sleep_input = QDoubleSpinBox()
        self.sleep_input.setDecimals(1)
        self.sleep_input.setSingleStep(0.5)
        self.sleep_input.setRange(0, 24)
        form_layout.addWidget(self.sleep_input, 6, 1)

        form_layout.addWidget(QLabel("Notas / Diario:"), 7, 0, 1, 2)
        self.comments_input = QTextEdit()
        self.comments_input.setFixedHeight(80)
        form_layout.addWidget(self.comments_input, 8, 0, 1, 2)
        
        layout.addWidget(form_frame)
        
        save_btn = QPushButton("💾 Guardar Cambios")
        save_btn.setObjectName("PrimaryAction")
        save_btn.clicked.connect(self.save_changes)
        layout.addWidget(save_btn)

    def load_data(self):
        if not self.record: return
        self.momento_input.setCurrentText(self.record.momento_dia)
        self.energy_slider.setValue(self.record.energia)
        self.prod_slider.setValue(self.record.productividad)
        self.disc_slider.setValue(self.record.disciplina)
        self.stress_slider.setValue(self.record.estres)
        self.mood_slider.setValue(self.record.animo)
        self.sleep_input.setValue(self.record.horas_sueno)
        self.comments_input.setText(self.record.comentario)

    def save_changes(self):
        if self.record:
            self.record.momento_dia = self.momento_input.currentText()
            self.record.energia = self.energy_slider.value()
            self.record.productividad = self.prod_slider.value()
            self.record.disciplina = self.disc_slider.value()
            self.record.estres = self.stress_slider.value()
            self.record.animo = self.mood_slider.value()
            self.record.horas_sueno = self.sleep_input.value()
            self.record.comentario = self.comments_input.toPlainText()
            self.db.commit()
            
            # Request all views to refresh if main window method available
            main_win = self.parent().window()
            if hasattr(main_win, 'refresh_all_views'):
                main_win.refresh_all_views()
                
        self.accept()

class FeedbackHistoryView(QWidget):
    def __init__(self, db_session):
        super().__init__()
        self.db = db_session
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header = QLabel("📖 Historial de Notas")
        header.setObjectName("Header")
        layout.addWidget(header)

        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(15)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        container = QWidget()
        container.setLayout(self.scroll_layout)
        scroll.setWidget(container)
        
        layout.addWidget(scroll)

    def refresh_stats(self):
        self.refresh_list()

    def refresh_list(self):
        # Limpiar
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        records = self.db.query(Retroalimentacion).order_by(Retroalimentacion.fecha.desc(), Retroalimentacion.id.desc()).all()
        
        if not records:
            empty = QLabel("Aún no tienes notas en tu historial.")
            empty.setStyleSheet("color: #777777; font-size: 16px;")
            self.scroll_layout.addWidget(empty)
            return

        for r in records:
            card = self.create_history_card(r)
            self.scroll_layout.addWidget(card)

    def create_history_card(self, r):
        card = QFrame()
        card.setObjectName("Card")
        l = QVBoxLayout(card)
        l.setSpacing(10)
        
        # Top Row (Date, Moment)
        top = QHBoxLayout()
        date_lbl = QLabel(f"<b>{r.fecha.strftime('%d %b %Y')}</b> | {r.momento_dia}")
        date_lbl.setStyleSheet("color: #3c3c3c; font-size: 16px;")
        
        btn_edit = QPushButton("✏️ Editar")
        btn_edit.setStyleSheet("color: #1cb0f6; font-weight: bold; padding: 5px; border: none; background: transparent;")
        btn_edit.clicked.connect(lambda _, rec_id=r.id: self.edit_record(rec_id))
        
        btn_del = QPushButton("🗑️ Eliminar")
        btn_del.setStyleSheet("color: #ff4b4b; font-weight: bold; padding: 5px; border: none; background: transparent;")
        btn_del.clicked.connect(lambda _, rec_id=r.id: self.delete_record(rec_id))
        
        top.addWidget(date_lbl)
        top.addStretch()
        top.addWidget(btn_edit)
        top.addWidget(btn_del)
        l.addLayout(top)
        
        # Second Row (Metrics)
        metrics = QLabel(f"⚡ Ene: {r.energia}/10  |  ⚙️ Prod: {r.productividad}/10  |  🛡️ Disc: {r.disciplina}/10  |  😴 Sueño: {r.horas_sueno}h")
        metrics.setStyleSheet("color: #58cc02; font-size: 14px; font-weight: bold;")
        l.addWidget(metrics)
        
        # Comments
        if r.comentario:
            notes = QLabel(r.comentario)
            notes.setWordWrap(True)
            notes.setStyleSheet("color: #777777; font-size: 14px; margin-top: 5px;")
            l.addWidget(notes)

        return card

    def edit_record(self, record_id):
        dialog = EditFeedbackDialog(self.db, record_id, self)
        if dialog.exec():
            # Already refreshed in save_changes via Main Windows, but fallback here
            self.refresh_list()

    def delete_record(self, record_id):
        result = QMessageBox.question(self, "Eliminar Registro", "¿Seguro que deseas eliminar esta retroalimentación? Se perderán estos datos para tus gráficos.", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.Yes:
            record = self.db.query(Retroalimentacion).filter(Retroalimentacion.id == record_id).first()
            if record:
                self.db.delete(record)
                self.db.commit()
                main_win = self.window()
                if hasattr(main_win, 'refresh_all_views'):
                    main_win.refresh_all_views()
                else:
                    self.refresh_list()
