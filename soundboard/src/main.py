#!/usr/bin/env python3
"""
Soundboard Program - Main Entry Point
"""

import logging
import os
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def _configure_logging():
    """Initialise logging once. Set SOUNDBOARD_DEBUG=1 for verbose output."""
    level = logging.DEBUG if os.environ.get("SOUNDBOARD_DEBUG") else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def main():
    """Main application entry point"""
    _configure_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()