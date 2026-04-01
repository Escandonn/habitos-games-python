def get_duolingo_style():
    return """
    QMainWindow {
        background-color: #ffffff;
    }
    QWidget {
        color: #4b4b4b;
        font-family: 'din-round', sans-serif;
        font-size: 16px;
    }
    QFrame#Sidebar {
        background-color: #ffffff;
        border-right: 2px solid #e5e5e5;
    }
    QPushButton {
        background-color: #ffffff;
        border: 2px solid #e5e5e5;
        border-bottom: 4px solid #e5e5e5;
        border-radius: 12px;
        padding: 12px 20px;
        text-align: left;
        font-weight: bold;
        color: #afafaf;
        margin: 5px;
    }
    QPushButton:hover {
        background-color: #f7f7f7;
    }
    QPushButton#Active {
        background-color: #ddf4ff;
        border: 2px solid #84d8ff;
        border-bottom: 4px solid #84d8ff;
        color: #1899d6;
    }
    
    /* Duolingo Green Button */
    QPushButton#PrimaryAction {
        background-color: #58cc02;
        border: 2px solid #58cc02;
        border-bottom: 6px solid #46a302;
        color: white;
        text-align: center;
    }
    QPushButton#PrimaryAction:pressed {
        border-bottom: 2px solid #46a302;
        margin-top: 4px;
    }

    QLabel#Header {
        font-size: 28px;
        font-weight: bold;
        color: #3c3c3c;
    }
    
    QFrame#Card {
        background-color: #ffffff;
        border: 2px solid #e5e5e5;
        border-radius: 16px;
        padding: 15px;
    }
    
    QProgressBar {
        border: 2px solid #e5e5e5;
        border-radius: 12px;
        text-align: center;
        background-color: #e5e5e5;
        height: 20px;
        font-weight: bold;
    }
    QProgressBar::chunk {
        background-color: #58cc02;
        border-radius: 10px;
    }
    
    QLineEdit, QComboBox, QTextEdit, QSpinBox {
        background-color: #f7f7f7;
        border: 2px solid #e5e5e5;
        border-radius: 12px;
        padding: 10px;
        color: #3c3c3c;
    }
    
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    
    QScrollBar:vertical {
        border: none;
        background: #f1f1f1;
        width: 10px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #ccc;
        min-height: 20px;
        border-radius: 5px;
    }
    """
