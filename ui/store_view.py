from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout,
                             QLineEdit, QSpinBox, QMessageBox)
from PyQt6.QtCore import Qt
from models.recompensa import Recompensa
from models.usuario import Usuario

class StoreView(QWidget):
    def __init__(self, db_session):
        super().__init__()
        self.db = db_session
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header con Oro
        header_layout = QHBoxLayout()
        title = QLabel("🛒 Tienda de Recompensas")
        title.setObjectName("Header")
        
        self.gold_label = QLabel("💰 Oro: 0")
        self.gold_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #f59e0b;")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.gold_label)
        layout.addLayout(header_layout)

        # Formulario para agregar recompensa
        form_frame = QFrame()
        form_frame.setObjectName("Card")
        form_layout = QHBoxLayout(form_frame)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ej: Jugar 1h Videojuegos")
        self.cost_input = QSpinBox()
        self.cost_input.setRange(10, 10000)
        self.cost_input.setSingleStep(50)
        self.cost_input.setValue(100)
        self.cost_input.setPrefix("💰 ")
        
        btn_add = QPushButton("➕ Agregar Recompensa")
        btn_add.setObjectName("PrimaryAction")
        btn_add.clicked.connect(self.add_reward)
        
        form_layout.addWidget(QLabel("Nueva:"))
        form_layout.addWidget(self.name_input, stretch=1)
        form_layout.addWidget(QLabel("Costo:"))
        form_layout.addWidget(self.cost_input)
        form_layout.addWidget(btn_add)
        
        layout.addWidget(form_frame)

        # Área de Scroll para las Recompensas
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(15)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        container = QWidget()
        container.setLayout(self.grid_layout)
        scroll.setWidget(container)
        
        layout.addWidget(scroll)

    def refresh_stats(self):
        self.refresh_list()

    def refresh_list(self):
        user = self.db.query(Usuario).first()
        if user:
            self.gold_label.setText(f"💰 Oro: {user.oro_total}")

        # Limpiar Grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        rewards = self.db.query(Recompensa).order_by(Recompensa.comprada.asc(), Recompensa.costo_oro.asc()).all()
        
        row = 0
        col = 0
        for r in rewards:
            card = self.create_reward_card(r, user.oro_total if user else 0)
            self.grid_layout.addWidget(card, row, col)
            col += 1
            if col > 2: # 3 cards por fila
                col = 0
                row += 1

    def create_reward_card(self, r, current_gold):
        card = QFrame()
        card.setObjectName("Card")
        l = QVBoxLayout(card)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon = QLabel(r.icono)
        icon.setStyleSheet("font-size: 40px; margin-bottom: 10px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        name = QLabel(r.nombre)
        name.setWordWrap(True)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name.setStyleSheet("font-size: 16px; font-weight: bold; color: #3c3c3c;")
        
        cost = QLabel(f"💰 {r.costo_oro}")
        cost.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cost.setStyleSheet("font-size: 14px; color: #f59e0b; font-weight: bold; margin-bottom: 15px;")
        
        l.addWidget(icon)
        l.addWidget(name)
        l.addWidget(cost)
        
        if r.comprada:
            badge = QLabel("✅ Comprado")
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setStyleSheet("color: white; background-color: #58cc02; padding: 5px; border-radius: 5px; font-weight: bold;")
            l.addWidget(badge)
            
            btn_delete = QPushButton("🗑️")
            btn_delete.setStyleSheet("border: none; color: gray; margin-top: 5px;")
            btn_delete.clicked.connect(lambda _, rec_id=r.id: self.delete_reward(rec_id))
            l.addWidget(btn_delete)
        else:
            can_afford = current_gold >= r.costo_oro
            btn_buy = QPushButton("Comprar")
            if can_afford:
                btn_buy.setObjectName("PrimaryAction")
                btn_buy.clicked.connect(lambda _, rec_id=r.id: self.buy_reward(rec_id))
            else:
                btn_buy.setStyleSheet("background-color: #e5e5e5; color: #afafaf; border-radius: 12px; padding: 10px; font-weight: bold;")
                btn_buy.setEnabled(False)
            l.addWidget(btn_buy)

        return card

    def add_reward(self):
        name = self.name_input.text().strip()
        if not name: return
        
        cost = self.cost_input.value()
        import random
        icons = ["🎁", "🎮", "🍿", "🍕", "🏖️", "💤", "🎟️"]
        
        r = Recompensa(nombre=name, costo_oro=cost, icono=random.choice(icons))
        self.db.add(r)
        self.db.commit()
        
        self.name_input.clear()
        self.refresh_list()

    def buy_reward(self, rec_id):
        r = self.db.query(Recompensa).filter(Recompensa.id == rec_id).first()
        user = self.db.query(Usuario).first()
        
        if r and user and user.oro_total >= r.costo_oro:
            respuesta = QMessageBox.question(self, "Confirmar Compra", f"¿Gastar {r.costo_oro} Oro para obtener: {r.nombre}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if respuesta == QMessageBox.StandardButton.Yes:
                user.oro_total -= r.costo_oro
                r.comprada = True
                self.db.commit()
                
                main_win = self.window()
                if hasattr(main_win, 'refresh_all_views'):
                    main_win.refresh_all_views()
                else:
                    self.refresh_list()

    def delete_reward(self, rec_id):
        r = self.db.query(Recompensa).filter(Recompensa.id == rec_id).first()
        if r:
            self.db.delete(r)
            self.db.commit()
            self.refresh_list()
