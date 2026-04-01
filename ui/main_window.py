from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from ui.styles import get_duolingo_style

class MainWindow(QMainWindow):
    def __init__(self, db_session):
        super().__init__()
        self.db = db_session
        self.setWindowTitle("Habitos Games - Pro Edition")
        self.resize(1100, 750)
        self.setStyleSheet(get_duolingo_style())
        
        # We define this early so switch_view can use it during setup_ui if needed
        self.nav_buttons = []
        
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
        self.logo.setStyleSheet("font-size: 22px; font-weight: bold; color: #1cb0f6; margin-bottom: 30px;")
        sidebar_layout.addWidget(self.logo)

        self.btn_dashboard = self.create_nav_btn("📊 Dashboard", 0)
        self.btn_today = self.create_nav_btn("📅 Hoy", 1)
        self.btn_create = self.create_nav_btn("➕ Crear Hábito", 2)
        self.btn_stats = self.create_nav_btn("📈 Estadísticas", 3)
        self.btn_habit_stats = self.create_nav_btn("🔍 Análisis Individual", 4)
        self.btn_feedback = self.create_nav_btn("📒 Retroalimentación", 5)
        self.btn_feedback_history = self.create_nav_btn("📖 Historial de Notas", 6)
        self.btn_store = self.create_nav_btn("🛒 Tienda", 7)
        self.btn_excel = self.create_nav_btn("📥 Exportar Excel", 8)
        self.btn_config = self.create_nav_btn("⚙️ Configuración", 9)

        self.nav_buttons = [self.btn_dashboard, self.btn_today, self.btn_create, self.btn_stats, self.btn_habit_stats, self.btn_feedback, self.btn_feedback_history, self.btn_store, self.btn_excel, self.btn_config]
        
        for b in self.nav_buttons:
            sidebar_layout.addWidget(b)
        
        sidebar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Pre-select first view
        self.set_active_btn(0)

        main_layout.addWidget(self.sidebar)

        from PyQt6.QtWidgets import QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        
        self.content_stack = QStackedWidget()
        self.scroll_area.setWidget(self.content_stack)
        
        main_layout.addWidget(self.scroll_area)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.apply_styles()
        
        # System Tray Icon Local Notification
        from PyQt6.QtWidgets import QSystemTrayIcon
        from PyQt6.QtGui import QIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        self.tray_icon.show()
        self.tray_icon.showMessage("Habitos Games", "¡Bienvenido! Cumple tus metas de hoy para mantener tus rachas.", QSystemTrayIcon.MessageIcon.Information, 3000)

    def apply_styles(self):
        from ui.styles import get_duolingo_style
        self.setStyleSheet(get_duolingo_style())
        self.sidebar.setObjectName("Sidebar")

    def refresh_all_views(self):
        for i in range(self.content_stack.count()):
            w = self.content_stack.widget(i)
            # Order matters: list updates first, then stats/charts
            if hasattr(w, "refresh_habit_list"): w.refresh_habit_list()
            if hasattr(w, "refresh_habits"): w.refresh_habits()
            if hasattr(w, "refresh_stats"): w.refresh_stats()
            if hasattr(w, "refresh_charts"): w.refresh_charts()

    def create_nav_btn(self, text, index):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda _, x=index: self.switch_view(x))
        return btn

    def switch_view(self, index):
        if index == 8: # Export Excel
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
