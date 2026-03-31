def get_dark_style():
    return """
    QMainWindow {
        background-color: #0f172a;
    }
    QWidget {
        color: #f8fafc;
        font-family: 'Segoe UI', sans-serif;
    }
    QFrame#Sidebar {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    QPushButton {
        background-color: transparent;
        border: none;
        padding: 10px;
        text-align: left;
        font-size: 14px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #334155;
    }
    QPushButton#Active {
        background-color: #3b82f6;
        font-weight: bold;
    }
    QLabel#Header {
        font-size: 24px;
        font-weight: bold;
        color: #60a5fa;
    }
    QProgressBar {
        border: 1px solid #334155;
        border-radius: 5px;
        text-align: center;
        background-color: #1e293b;
    }
    QProgressBar::chunk {
        background-color: #3b82f6;
    }
    QLineEdit, QComboBox, QTextEdit, QSpinBox {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 5px;
        padding: 5px;
        color: #f8fafc;
    }
    QListWidget {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 5px;
    }
    QCheckBox {
        spacing: 10px;
    }
    """
