"""
Main Window Implementation with Modern Card Design
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStatusBar, QMenuBar, QMenu, QLabel,
    QPushButton, QScrollArea, QFrame, QSizePolicy,
    QStackedWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QColor, QPalette

# Modern color scheme
COLORS = {
    'bg_primary': '#121212',
    'bg_secondary': '#181818',
    'bg_elevated': '#282828',
    'accent': '#1DB954',  # Vibrant green
    'text_primary': '#FFFFFF',
    'text_secondary': '#B3B3B3',
    'card_hover': '#2A2A2A',
    'divider': '#282828'
}

class ModernButton(QPushButton):
    """Modern styled button"""
    def __init__(self, text, parent=None, is_primary=False):
        super().__init__(text, parent)
        self.is_primary = is_primary
        self._setup_style()
        
    def _setup_style(self):
        if self.is_primary:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent']};
                    color: {COLORS['text_primary']};
                    border: none;
                    border-radius: 20px;
                    padding: 8px 24px;
                    font-weight: bold;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: #1ed760;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['bg_elevated']};
                    color: {COLORS['text_primary']};
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['card_hover']};
                }}
            """)

class CategoryTab(QPushButton):
    """Modern category tab button"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {COLORS['text_primary']};
            }}
            QPushButton:checked {{
                color: {COLORS['text_primary']};
                border-bottom: 2px solid {COLORS['accent']};
            }}
        """)

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Soundboard")
        self.setMinimumSize(1200, 800)
        
        # Set window style
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['bg_primary']};
            }}
            QFrame {{
                background-color: {COLORS['bg_primary']};
                border: none;
            }}
        """)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Initialize UI components
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components"""
        self._create_header()
        self._create_main_content()
        self._create_status_bar()
    
    def _create_header(self):
        """Create the modern header area"""
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_secondary']};
                border-bottom: 1px solid {COLORS['divider']};
            }}
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(0)
        header_layout.setContentsMargins(24, 16, 24, 0)
        
        # Top bar with title and controls
        top_bar = QHBoxLayout()
        
        # Title
        title = QLabel("Soundboard")
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 24px;
            font-weight: bold;
        """)
        top_bar.addWidget(title)
        
        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)
        
        add_sound_btn = ModernButton("Add Sound", is_primary=True)
        settings_btn = ModernButton("Settings")
        
        controls_layout.addWidget(add_sound_btn)
        controls_layout.addWidget(settings_btn)
        
        top_bar.addStretch()
        top_bar.addLayout(controls_layout)
        
        # Category tabs
        tabs_layout = QHBoxLayout()
        tabs_layout.setSpacing(0)
        tabs_layout.setContentsMargins(0, 16, 0, 0)
        
        categories = ["All Sounds", "Favorites", "Recent", "Custom"]
        for category in categories:
            tab = CategoryTab(category)
            if category == "All Sounds":
                tab.setChecked(True)
            tabs_layout.addWidget(tab)
        
        tabs_layout.addStretch()
        
        header_layout.addLayout(top_bar)
        header_layout.addLayout(tabs_layout)
        
        self.main_layout.addWidget(header)
    
    def _create_main_content(self):
        """Create the main content area"""
        content_area = QFrame()
        content_area.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_primary']};
            }}
        """)
        
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)
        
        # Create scrollable sound grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                width: 8px;
                background: transparent;
            }
            QScrollBar::handle:vertical {
                background: #404040;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Sound grid placeholder
        grid_widget = QWidget()
        grid_widget.setStyleSheet(f"""
            background-color: {COLORS['bg_primary']};
        """)
        grid_layout = QVBoxLayout(grid_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(16)
        
        # Add placeholder text
        placeholder = QLabel("Add sounds to get started")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 16px;
            padding: 40px;
        """)
        grid_layout.addWidget(placeholder)
        grid_layout.addStretch()
        
        scroll_area.setWidget(grid_widget)
        content_layout.addWidget(scroll_area)
        
        self.main_layout.addWidget(content_area)
    
    def _create_status_bar(self):
        """Create the status bar"""
        status_bar = QStatusBar()
        status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_secondary']};
            }}
        """)
        self.setStatusBar(status_bar)
        
        # Add status bar widgets
        status_bar.addWidget(QLabel("Ready"))
        status_bar.addPermanentWidget(QLabel("Version 0.1.0")) 