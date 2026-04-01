import sys
from PyQt6.QtWidgets import QApplication
from database.db_manager import SessionLocal, engine, Base
from ui.main_window import MainWindow
from ui.dashboard_view import DashboardView
from ui.today_view import TodayView
from ui.create_habit_view import CreateHabitView
from ui.stats_view import StatsView
from ui.habit_stats_view import HabitStatsView
from ui.feedback_view import FeedbackView
from ui.feedback_history_view import FeedbackHistoryView
from ui.store_view import StoreView
import models.usuario
import models.habito
import models.registro
import models.retroalimentacion
import models.recompensa

from sqlalchemy import text

def run_migrations(engine):
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE usuarios ADD COLUMN oro_total INTEGER DEFAULT 0"))
            conn.commit()
        except Exception:
            pass # Ya existe
            
        try:
            conn.execute(text("ALTER TABLE habitos ADD COLUMN racha_actual INTEGER DEFAULT 0"))
            conn.commit()
        except Exception:
            pass # Ya existe

def main():
    # Initialize Database Migrations
    run_migrations(engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Initialize Application
    app = QApplication(sys.argv)
    window = MainWindow(db)

    # Initialize Views in Order
    # 0: Dashboard
    dashboard = DashboardView(db)
    # 1: Today
    today = TodayView(db)
    # 2: Create
    create_habit = CreateHabitView(db)
    # 3: Stats
    stats = StatsView(db)
    # 4: Individual Stats
    habit_stats = HabitStatsView(db)
    # 5: Feedback
    feedback = FeedbackView(db)
    # 6: Feedback History
    feedback_history = FeedbackHistoryView(db)
    # 7: Store
    store = StoreView(db)

    # Add Views to Content Stack
    window.content_stack.addWidget(dashboard)
    window.content_stack.addWidget(today)
    window.content_stack.addWidget(create_habit)
    window.content_stack.addWidget(stats)
    window.content_stack.addWidget(habit_stats)
    window.content_stack.addWidget(feedback)
    window.content_stack.addWidget(feedback_history)
    window.content_stack.addWidget(store)

    # Set Initial View
    window.content_stack.setCurrentIndex(0)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
