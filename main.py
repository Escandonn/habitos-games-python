import sys
from PyQt6.QtWidgets import QApplication
from database.db_manager import SessionLocal, engine, Base
from ui.main_window import MainWindow
from ui.dashboard_view import DashboardView
from ui.today_view import TodayView
from ui.create_habit_view import CreateHabitView
from ui.stats_view import StatsView
from ui.feedback_view import FeedbackView

def main():
    # Initialize Database
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Initialize Application
    app = QApplication(sys.argv)
    window = MainWindow(db)

    # Initialize Views
    dashboard = DashboardView(db)
    today = TodayView(db)
    create_habit = CreateHabitView(db)
    stats = StatsView(db)
    feedback = FeedbackView(db)

    # Add Views to Content Stack
    window.content_stack.addWidget(dashboard)
    window.content_stack.addWidget(today)
    window.content_stack.addWidget(create_habit)
    window.content_stack.addWidget(stats)
    window.content_stack.addWidget(feedback)

    # Set Initial View
    window.content_stack.setCurrentIndex(0)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
