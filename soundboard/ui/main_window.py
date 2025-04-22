from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle("Soundboard Pro")
        self.setMinimumSize(800, 600)

        self._init_ui()

    def _init_ui(self):
        pass
