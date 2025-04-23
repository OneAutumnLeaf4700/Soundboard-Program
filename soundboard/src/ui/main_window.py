"""
Main Window Implementation
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QStatusBar, QMenuBar, QMenu, QLabel,
    QPushButton, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Soundboard")
        self.setMinimumSize(1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        
        # Initialize UI components
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components"""
        # Create menu bar
        self._create_menu_bar()
        
        # Create toolbar
        self._create_toolbar()
        
        # Create main content area
        self._create_main_content()
        
        # Create status bar
        self._create_status_bar()
    
    def _create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        
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
        view_menu.addAction("Toggle Status Bar")
        
        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        settings_menu.addAction("Audio Devices")
        settings_menu.addAction("Hotkeys")
        settings_menu.addAction("Theme")
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Documentation")
        help_menu.addAction("About")
    
    def _create_toolbar(self):
        """Create the application toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Add toolbar buttons
        toolbar.addAction("Add Sound")
        toolbar.addAction("Edit Sound")
        toolbar.addAction("Delete Sound")
        toolbar.addSeparator()
        toolbar.addAction("Play")
        toolbar.addAction("Stop")
        toolbar.addSeparator()
        toolbar.addAction("Settings")
    
    def _create_main_content(self):
        """Create the main content area"""
        # Create sidebar
        sidebar = QFrame()
        sidebar.setMaximumWidth(250)
        sidebar.setMinimumWidth(200)
        sidebar.setFrameStyle(QFrame.Shape.StyledPanel)
        sidebar_layout = QVBoxLayout(sidebar)
        
        # Add sidebar content
        sidebar_layout.addWidget(QLabel("Categories"))
        sidebar_layout.addWidget(QPushButton("All Sounds"))
        sidebar_layout.addWidget(QPushButton("Favorites"))
        sidebar_layout.addWidget(QPushButton("Recent"))
        sidebar_layout.addStretch()
        
        # Create main sound grid area
        main_area = QFrame()
        main_area.setFrameStyle(QFrame.Shape.StyledPanel)
        main_layout = QVBoxLayout(main_area)
        
        # Add search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(QPushButton("Search"))
        main_layout.addLayout(search_layout)
        
        # Add sound grid placeholder
        sound_grid = QFrame()
        sound_grid.setFrameStyle(QFrame.Shape.StyledPanel)
        sound_grid.setMinimumHeight(400)
        main_layout.addWidget(sound_grid)
        
        # Add to main layout
        self.main_layout.addWidget(sidebar)
        self.main_layout.addWidget(main_area)
    
    def _create_status_bar(self):
        """Create the status bar"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # Add status bar widgets
        status_bar.addWidget(QLabel("Ready"))
        status_bar.addPermanentWidget(QLabel("Version 0.1.0")) 