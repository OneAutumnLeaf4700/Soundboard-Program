# app/main.py

import sys
from PyQt6.QtWidgets import QApplication
from soundboard.ui.main_window import MainWindow
from soundboard.app.config import AppConfig

def main():
    # Initialize application
    app = QApplication(sys.argv)
    
    # Load config, settings, theme, etc.
    config = AppConfig()
    config.apply_theme(app)  # e.g., dark or light theme
    
    # Create and show main window
    window = MainWindow(config)
    window.show()

    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
