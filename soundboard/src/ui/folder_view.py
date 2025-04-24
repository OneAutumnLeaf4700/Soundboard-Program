"""
FolderView Implementation for the Soundboard
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QColor

# Import colors from main_window for consistency
from soundboard.src.ui.main_window import COLORS

class FolderItem(QFrame):
    """
    Widget representing a single folder in the folder view
    """
    clicked = pyqtSignal(str)  # Emits folder_id when clicked
    
    def __init__(self, folder_name, folder_id, sound_count=0, parent=None):
        super().__init__(parent)
        self.folder_name = folder_name
        self.folder_id = folder_id
        self.sound_count = sound_count
        self.is_selected = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        # Set frame properties
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(45)
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Folder icon
        self.icon_label = QLabel("📁")
        self.icon_label.setFixedSize(20, 20)
        self.icon_label.setStyleSheet(f"color: {COLORS['folder_icon']}; font-size: 16px;")
        layout.addWidget(self.icon_label)
        
        # Folder name
        self.name_label = QLabel(self.folder_name)
        self.name_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px;")
        layout.addWidget(self.name_label, 1)
        
        # Sound count badge
        self.count_label = QLabel(f"{self.sound_count}")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_label.setFixedSize(25, 20)
        self.count_label.setStyleSheet(f"""
            background-color: {COLORS['count_badge_bg']};
            color: {COLORS['text_secondary']};
            border-radius: 10px;
            font-size: 11px;
        """)
        layout.addWidget(self.count_label)
        
        # Set initial styling
        self._update_style()
        
        # Connect signals
        self.mousePressEvent = lambda event: self.clicked.emit(self.folder_id)
    
    def set_selected(self, selected):
        """Set the selected state of this folder item"""
        self.is_selected = selected
        self._update_style()
    
    def update_count(self, count):
        """Update the sound count"""
        self.sound_count = count
        self.count_label.setText(f"{count}")
    
    def _update_style(self):
        """Update styling based on selection state"""
        if self.is_selected:
            self.setStyleSheet(f"""
                FolderItem {{
                    background-color: {COLORS['folder_selected']};
                    border-radius: 6px;
                }}
            """)
            self.name_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
            self.icon_label.setStyleSheet(f"color: {COLORS['accent']}; font-size: 16px;")
        else:
            self.setStyleSheet(f"""
                FolderItem {{
                    background-color: transparent;
                    border-radius: 6px;
                }}
                FolderItem:hover {{
                    background-color: {COLORS['folder_hover']};
                }}
            """)
            self.name_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px;")
            self.icon_label.setStyleSheet(f"color: {COLORS['folder_icon']}; font-size: 16px;")


class FolderView(QWidget):
    """
    Widget for displaying and managing folders
    """
    folder_selected = pyqtSignal(str)  # Emits folder_id when a folder is selected
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.folders = {}  # Dictionary to store folder items {folder_id: FolderItem}
        self.current_folder_id = None
        
        self._setup_ui()
        self._populate_sample_folders()  # Add some sample folders for demonstration
    
    def _setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(15, 10, 15, 5)
        header_layout.setSpacing(10)
        
        # Title
        title_label = QLabel("Folders")
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 18px;
            font-weight: bold;
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Add folder button
        self.add_folder_btn = QPushButton("+ New")
        self.add_folder_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card_bg']};
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 4px 10px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['button_hover']};
                color: {COLORS['text_primary']};
            }}
        """)
        header_layout.addWidget(self.add_folder_btn)
        
        main_layout.addLayout(header_layout)
        
        # Scroll area for folders
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background: {COLORS['scrollbar_bg']};
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['scrollbar_handle']};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Container for folder items
        self.folders_container = QWidget()
        self.folders_layout = QVBoxLayout(self.folders_container)
        self.folders_layout.setContentsMargins(10, 5, 10, 15)
        self.folders_layout.setSpacing(5)
        self.folders_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll_area.setWidget(self.folders_container)
        main_layout.addWidget(self.scroll_area)
        
        # Set styling for the folder view
        self.setStyleSheet(f"""
            FolderView {{
                background-color: {COLORS['sidebar_bg']};
                border-right: 1px solid {COLORS['divider']};
            }}
        """)
    
    def _populate_sample_folders(self):
        """Add sample folders for demonstration"""
        sample_folders = [
            {"id": "folder1", "name": "Sound Effects", "count": 12},
            {"id": "folder2", "name": "Music", "count": 8},
            {"id": "folder3", "name": "Voice Clips", "count": 5},
            {"id": "folder4", "name": "Memes", "count": 15},
            {"id": "folder5", "name": "Stream Alerts", "count": 9},
            {"id": "folder6", "name": "Custom", "count": 3},
            {"id": "folder7", "name": "Gaming", "count": 7},
            {"id": "folder8", "name": "Soundscapes", "count": 4},
            {"id": "folder9", "name": "Animals", "count": 10},
            {"id": "folder10", "name": "Instruments", "count": 6}
        ]
        
        for folder in sample_folders:
            self.add_folder(folder["id"], folder["name"], folder["count"])
    
    def add_folder(self, folder_id, folder_name, sound_count=0):
        """Add a new folder to the view"""
        folder_item = FolderItem(folder_name, folder_id, sound_count)
        folder_item.clicked.connect(self._on_folder_clicked)
        
        self.folders[folder_id] = folder_item
        self.folders_layout.addWidget(folder_item)
        
        return folder_item
    
    def remove_folder(self, folder_id):
        """Remove a folder from the view"""
        if folder_id in self.folders:
            folder_item = self.folders.pop(folder_id)
            self.folders_layout.removeWidget(folder_item)
            folder_item.deleteLater()
            
            # If we removed the current folder, deselect it
            if self.current_folder_id == folder_id:
                self.current_folder_id = None
    
    def select_folder(self, folder_id):
        """Programmatically select a folder"""
        self._on_folder_clicked(folder_id)
    
    def _on_folder_clicked(self, folder_id):
        """Handle folder selection"""
        # Deselect current folder if any
        if self.current_folder_id and self.current_folder_id in self.folders:
            self.folders[self.current_folder_id].set_selected(False)
        
        # Select new folder
        if folder_id in self.folders:
            self.current_folder_id = folder_id
            self.folders[folder_id].set_selected(True)
            self.folder_selected.emit(folder_id)
        else:
            self.current_folder_id = None
    
    def update_folder_count(self, folder_id, count):
        """Update sound count for a folder"""
        if folder_id in self.folders:
            self.folders[folder_id].update_count(count) 