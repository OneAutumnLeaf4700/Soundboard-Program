"""
Main Window Implementation with Minimal Studio Design
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStatusBar, QMenuBar, QMenu, QLabel,
    QPushButton, QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QColor, QPalette

# Color scheme
COLORS = {
    'bg_dark': '#1E1E1E',
    'bg_light': '#252526',
    'accent': '#007ACC',
    'text': '#CCCCCC',
    'text_dim': '#808080',
    'border': '#333333',
    'hover': '#2A2D2E'
}

class StudioButton(QPushButton):
    """Custom button with minimal studio design"""
    def __init__(self, text, parent=None, is_sidebar=False):
        super().__init__(text, parent)
        self.is_sidebar = is_sidebar
        self._setup_style()
        
    def _setup_style(self):
        if self.is_sidebar:
            self.setFixedHeight(40)
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['bg_dark']};
                    color: {COLORS['text_dim']};
                    border: none;
                    text-align: left;
                    padding: 10px 15px;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['hover']};
                    color: {COLORS['text']};
                }}
                QPushButton:checked {{
                    background-color: {COLORS['bg_light']};
                    color: {COLORS['text']};
                    border-left: 2px solid {COLORS['accent']};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['bg_light']};
                    color: {COLORS['text']};
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['hover']};
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
                background-color: {COLORS['bg_dark']};
            }}
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border: none;
            }}
        """)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Initialize UI components
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components"""
        self._create_menu_bar()
        self._create_main_content()
        self._create_status_bar()
    
    def _create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {COLORS['bg_dark']};
                color: {COLORS['text']};
                border-bottom: 1px solid {COLORS['border']};
                padding: 2px;
            }}
            QMenuBar::item:selected {{
                background-color: {COLORS['hover']};
            }}
            QMenu {{
                background-color: {COLORS['bg_dark']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['hover']};
            }}
        """)
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Soundboard")
        file_menu.addAction("Open Soundboard")
        file_menu.addAction("Save Soundboard")
        file_menu.addSeparator()
        file_menu.addAction("Exit")
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Add Sound")
        edit_menu.addAction("Edit Sound")
        edit_menu.addAction("Delete Sound")
        
        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Toggle Sidebar")
        
        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        settings_menu.addAction("Audio Devices")
        settings_menu.addAction("Hotkeys")
        settings_menu.addAction("Theme")
    
    def _create_main_content(self):
        """Create the main content area"""
        # Create sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border-right: 1px solid {COLORS['border']};
            }}
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(1)
        sidebar_layout.setContentsMargins(0, 10, 0, 10)
        
        # Add sidebar sections
        section_titles = ["LIBRARY", "PLAYLISTS", "SETTINGS"]
        section_items = [
            ["All Sounds", "Favorites", "Recent"],
            ["Default", "Custom"],
            ["Audio Devices", "Hotkeys", "Preferences"]
        ]
        
        for title, items in zip(section_titles, section_items):
            # Add section title
            section_label = QLabel(title)
            section_label.setStyleSheet(f"""
                color: {COLORS['text_dim']};
                font-size: 11px;
                padding: 15px 15px 5px 15px;
            """)
            sidebar_layout.addWidget(section_label)
            
            # Add section items
            for item in items:
                btn = StudioButton(item, is_sidebar=True)
                btn.setCheckable(True)
                if item == "All Sounds":  # Set default selected
                    btn.setChecked(True)
                sidebar_layout.addWidget(btn)
            
            sidebar_layout.addSpacing(15)
        
        sidebar_layout.addStretch()
        
        # Create main sound grid area
        main_area = QFrame()
        main_area.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
            }}
        """)
        
        main_layout = QVBoxLayout(main_area)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Add header
        header_layout = QHBoxLayout()
        header_label = QLabel("All Sounds")
        header_label.setStyleSheet(f"""
            color: {COLORS['text']};
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        add_sound_btn = StudioButton("Add Sound")
        header_layout.addWidget(add_sound_btn)
        
        main_layout.addLayout(header_layout)
        
        # Add sound grid placeholder
        sound_grid = QFrame()
        sound_grid.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border-radius: 4px;
            }}
        """)
        sound_grid.setMinimumHeight(400)
        main_layout.addWidget(sound_grid)
        
        # Add to main layout
        self.main_layout.addWidget(sidebar)
        self.main_layout.addWidget(main_area)
    
    def _create_status_bar(self):
        """Create the status bar"""
        status_bar = QStatusBar()
        status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {COLORS['bg_dark']};
                color: {COLORS['text_dim']};
            }}
        """)
        self.setStatusBar(status_bar)
        
        # Add status bar widgets
        status_bar.addWidget(QLabel("Ready"))
        status_bar.addPermanentWidget(QLabel("Version 0.1.0")) 