from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from ui.styles import get_dark_style

class MainWindow(QMainWindow):
    def __init__(self, db_session):
        super().__init__()
        self.db = db_session
        self.setWindowTitle("Habitos Games - Pro Edition")
        self.resize(1100, 750)
        self.setStyleSheet(get_dark_style())

        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 30, 15, 30)
        sidebar_layout.setSpacing(10)

        self.logo = QLabel("HABITOS GAMES")
        self.logo.setStyleSheet("font-size: 18px; font-weight: bold; color: #3b82f6; margin-bottom: 20px;")
        sidebar_layout.addWidget(self.logo)

        self.btn_dashboard = self.create_nav_btn("📊 Dashboard", 0)
        self.btn_today = self.create_nav_btn("📅 Hoy", 1)
        self.btn_create = self.create_nav_btn("➕ Crear Hábito", 2)
        self.btn_stats = self.create_nav_btn("📈 Estadísticas", 3)
        self.btn_feedback = self.create_nav_btn("📒 Retroalimentación", 4)
        self.btn_excel = self.create_nav_btn("📥 Exportar Excel", 5)

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_today)
        sidebar_layout.addWidget(self.btn_create)
        sidebar_layout.addWidget(self.btn_stats)
        sidebar_layout.addWidget(self.btn_feedback)
        sidebar_layout.addWidget(self.btn_excel)
        
        sidebar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.btn_config = self.create_nav_btn("⚙️ Configuración", 6)
        sidebar_layout.addWidget(self.btn_config)

        main_layout.addWidget(self.sidebar)

        # Content Area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.nav_buttons = [self.btn_dashboard, self.btn_today, self.btn_create, self.btn_stats, self.btn_feedback, self.btn_excel, self.btn_config]
        self.set_active_btn(0)

    def create_nav_btn(self, text, index):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda: self.switch_view(index))
        return btn

    def switch_view(self, index):
        if index == 5: # Export Excel
            self.export_excel()
            return

        self.content_stack.setCurrentIndex(index)
        self.set_active_btn(index)

        # Refresh the view if it has a refresh method
        current_widget = self.content_stack.currentWidget()
        if hasattr(current_widget, "refresh_stats"):
            current_widget.refresh_stats()
        if hasattr(current_widget, "refresh_habits"):
            current_widget.refresh_habits()
        if hasattr(current_widget, "refresh_charts"):
            current_widget.refresh_charts()

    def set_active_btn(self, index):
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.setObjectName("Active")
            else:
                btn.setObjectName("")
            btn.setStyle(btn.style()) # Refresh style

    def export_excel(self):
        from services.excel_service import ExcelService
        ExcelService.export_all_data(self.db)
        print("Excel exportado con éxito.")
