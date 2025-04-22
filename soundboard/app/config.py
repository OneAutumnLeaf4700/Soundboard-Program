from PyQt6.QtGui import QPalette, QColor
import json
from pathlib import Path

class AppConfig:
    def __init__(self):
        self.settings_path = Path("profiles/default.json")
        self.settings = self.load_settings()

    def load_settings(self):
        if self.settings_path.exists():
            with open(self.settings_path, 'r') as f:
                return json.load(f)
        else:
            return {
                "theme": "dark",
                "language": "en"
            }

    def apply_theme(self, app):
        theme = self.settings.get("theme", "dark")
        palette = QPalette()
        if theme == "dark":
            palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(30, 30, 30))
        app.setPalette(palette)
