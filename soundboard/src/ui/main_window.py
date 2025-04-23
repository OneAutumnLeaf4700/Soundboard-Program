"""
Main Window Implementation with Enhanced Modern Design
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStatusBar, QMenuBar, QMenu, QLabel,
    QPushButton, QScrollArea, QFrame, QSizePolicy,
    QStackedWidget, QGraphicsDropShadowEffect, QSlider,
    QLineEdit, QComboBox, QCheckBox, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QColor, QPalette, QLinearGradient, QGradient, QPainter, QPainterPath

# Enhanced color scheme
COLORS = {
    'bg_primary': '#121212',
    'bg_secondary': '#181818',
    'bg_elevated': '#282828',
    'accent': '#1DB954',  # Vibrant green
    'accent_gradient_start': '#1DB954',
    'accent_gradient_end': '#169C46',
    'text_primary': '#FFFFFF',
    'text_secondary': '#B3B3B3',
    'card_hover': '#2A2A2A',
    'divider': '#282828',
    'shadow': '#0A0A0A',
    'category_1': '#E13300',  # Orange for effects
    'category_2': '#1E3799',  # Blue for music
    'category_3': '#8E44AD',  # Purple for voice
    'category_4': '#27AE60',   # Green for custom
    'slider_bg': '#404040',
    'slider_handle': '#1DB954',
    'panel_bg': '#202020',
    'search_bg': '#2A2A2A',
    'search_border': '#404040',
    'toggle_active': '#1DB954',
    'toggle_inactive': '#404040',
    'card_gradient_start': '#2A2A2A',
    'card_gradient_end': '#1A1A1A',
    'card_active_glow': '#1DB954',
    'folder_bg': '#2D2D2D',
    'folder_hover': '#353535',
    'folder_active': '#3A3A3A',
    'folder_icon': '#FFC107',  # Amber color for folder icon
    'add_folder_bg': '#383838',
}

class SearchBar(QLineEdit):
    """Modern search bar with icon"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Search sounds...")
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['search_bg']};
                border: 1px solid {COLORS['search_border']};
                border-radius: 20px;
                padding: 8px 16px;
                color: {COLORS['text_primary']};
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 1px solid {COLORS['accent']};
            }}
        """)
        self.setFixedHeight(36)

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
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {COLORS['accent_gradient_start']},
                        stop:1 {COLORS['accent_gradient_end']});
                    color: {COLORS['text_primary']};
                    border: none;
                    border-radius: 20px;
                    padding: 8px 24px;
                    font-weight: bold;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {COLORS['accent']},
                        stop:1 {COLORS['accent']});
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

class SoundCard(QFrame):
    """Modern sound card with enhanced visual elements"""
    def __init__(self, title, category, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.title = title
        self.category = category
        self.is_active = False
        self._setup_ui()
        
    def _setup_ui(self):
        # Set up the main card style
        self.setStyleSheet(f"""
            SoundCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['card_gradient_start']},
                    stop:1 {COLORS['card_gradient_end']});
                border-radius: 8px;
                border: 1px solid {COLORS['divider']};
            }}
            SoundCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['card_hover']},
                    stop:1 {COLORS['bg_elevated']});
                border: 1px solid {COLORS['accent']};
            }}
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(COLORS['shadow']))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Top section with category and preview
        top_section = QHBoxLayout()
        
        # Category indicator
        category_indicator = QFrame()
        category_indicator.setFixedSize(4, 20)
        category_indicator.setStyleSheet(f"""
            background-color: {COLORS[f'category_{self.category}']};
            border-radius: 2px;
        """)
        top_section.addWidget(category_indicator)
        
        # Preview button
        preview_btn = ModernButton("🔊")
        preview_btn.setFixedSize(24, 24)
        preview_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_secondary']};
                border: none;
                border-radius: 12px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent']};
                color: {COLORS['text_primary']};
            }}
        """)
        top_section.addWidget(preview_btn)
        top_section.addStretch()
        
        layout.addLayout(top_section)
        
        # Title with icon
        title_layout = QHBoxLayout()
        
        # Category icon (placeholder)
        category_icon = QLabel("🎵")
        category_icon.setStyleSheet(f"font-size: 16px;")
        title_layout.addWidget(category_icon)
        
        title_label = QLabel(self.title)
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: bold;
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # Waveform placeholder with gradient
        waveform = QFrame()
        waveform.setFixedHeight(60)
        waveform.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['bg_secondary']},
                stop:1 {COLORS['bg_elevated']});
            border-radius: 4px;
        """)
        layout.addWidget(waveform)
        
        # Bottom controls
        controls = QHBoxLayout()
        
        # Play button with gradient
        play_btn = ModernButton("▶")
        play_btn.setFixedSize(32, 32)
        play_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['accent_gradient_start']},
                    stop:1 {COLORS['accent_gradient_end']});
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 16px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['accent']},
                    stop:1 {COLORS['accent']});
            }}
        """)
        controls.addWidget(play_btn)
        
        controls.addStretch()
        
        # Hotkey indicator with gradient
        hotkey_label = QLabel("F1")
        hotkey_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['bg_secondary']},
                stop:1 {COLORS['bg_elevated']});
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
        """)
        controls.addWidget(hotkey_label)
        
        layout.addLayout(controls)
        layout.addStretch()

    def set_active(self, active):
        """Set the card's active state"""
        self.is_active = active
        if active:
            self.setStyleSheet(f"""
                SoundCard {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {COLORS['card_gradient_start']},
                        stop:1 {COLORS['card_gradient_end']});
                    border-radius: 8px;
                    border: 2px solid {COLORS['card_active_glow']};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                SoundCard {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {COLORS['card_gradient_start']},
                        stop:1 {COLORS['card_gradient_end']});
                    border-radius: 8px;
                    border: 1px solid {COLORS['divider']};
                }}
            """)

class ModernSlider(QSlider):
    """Modern styled slider with value display"""
    def __init__(self, parent=None):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.setStyleSheet(f"""
            QSlider {{
                height: 24px;
            }}
            QSlider::groove:horizontal {{
                height: 4px;
                background: {COLORS['slider_bg']};
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {COLORS['slider_handle']};
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }}
            QSlider::sub-page:horizontal {{
                background: {COLORS['accent']};
                border-radius: 2px;
            }}
        """)
        self.setMaximum(100)
        self.setValue(70)

class ModernComboBox(QComboBox):
    """Modern styled combobox"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['bg_elevated']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 8px 16px;
                color: {COLORS['text_primary']};
                font-size: 13px;
            }}
            QComboBox:hover {{
                border: 1px solid {COLORS['accent']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['bg_elevated']};
                border: 1px solid {COLORS['divider']};
                selection-background-color: {COLORS['accent']};
                selection-color: {COLORS['text_primary']};
            }}
        """)

class ModernToggle(QCheckBox):
    """Modern styled toggle switch"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['text_primary']};
                font-size: 13px;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 40px;
                height: 20px;
                border-radius: 10px;
                background-color: {COLORS['toggle_inactive']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS['toggle_active']};
            }}
            QCheckBox::indicator::unchecked {{
                background-color: {COLORS['toggle_inactive']};
            }}
        """)

class ControlPanel(QFrame):
    """Right-side control panel with modern settings"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            ControlPanel {{
                background-color: {COLORS['panel_bg']};
                border-left: 1px solid {COLORS['divider']};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(24)

        # Header
        header = QLabel("Quick Settings")
        header.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 18px;
            font-weight: bold;
            padding-bottom: 8px;
            border-bottom: 1px solid {COLORS['divider']};
        """)
        layout.addWidget(header)

        # Volume Control
        volume_group = QFrame()
        volume_layout = QVBoxLayout(volume_group)
        volume_layout.setSpacing(8)

        volume_header = QHBoxLayout()
        volume_label = QLabel("Output Volume")
        volume_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px;")
        volume_header.addWidget(volume_label)
        volume_value = QLabel("70%")
        volume_value.setStyleSheet(f"color: {COLORS['text_secondary']};")
        volume_header.addWidget(volume_value)
        volume_layout.addLayout(volume_header)

        self.volume_slider = ModernSlider()
        volume_layout.addWidget(self.volume_slider)
        layout.addWidget(volume_group)

        # Audio Devices
        devices_group = QFrame()
        devices_layout = QVBoxLayout(devices_group)
        devices_layout.setSpacing(16)

        # Input Device
        input_label = QLabel("Input Device")
        input_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px;")
        devices_layout.addWidget(input_label)
        self.input_device = ModernComboBox()
        self.input_device.addItems(["Default Microphone", "USB Microphone", "System Audio"])
        devices_layout.addWidget(self.input_device)

        # Output Device
        output_label = QLabel("Output Device")
        output_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px;")
        devices_layout.addWidget(output_label)
        self.output_device = ModernComboBox()
        self.output_device.addItems(["Default Speakers", "Headphones", "System Audio"])
        devices_layout.addWidget(self.output_device)

        layout.addWidget(devices_group)

        # Soundboard Controls
        controls_group = QFrame()
        controls_layout = QVBoxLayout(controls_group)
        controls_layout.setSpacing(16)

        # Active Toggle
        self.active_toggle = ModernToggle("Soundboard Active")
        controls_layout.addWidget(self.active_toggle)

        # Hear Myself Toggle
        self.hear_myself = ModernToggle("Hear Myself")
        controls_layout.addWidget(self.hear_myself)

        layout.addWidget(controls_group)
        layout.addStretch()

class FolderView(QFrame):
    """Folder view for organizing sounds"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._populate_sample_folders()
        
    def _setup_ui(self):
        self.setStyleSheet(f"""
            FolderView {{
                background-color: {COLORS['bg_primary']};
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header with title and add button
        header = QHBoxLayout()
        
        title = QLabel("Folders")
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 24px;
            font-weight: bold;
        """)
        header.addWidget(title)
        
        header.addStretch()
        
        add_folder_btn = ModernButton("+ New Folder", is_primary=True)
        header.addWidget(add_folder_btn)
        
        layout.addLayout(header)
        
        # Folder list (showing visual representation only)
        folders_container = QScrollArea()
        folders_container.setWidgetResizable(True)
        folders_container.setFrameShape(QFrame.Shape.NoFrame)
        folders_container.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
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
        
        folders_widget = QWidget()
        folders_layout = QVBoxLayout(folders_widget)
        folders_layout.setContentsMargins(0, 0, 0, 0)
        folders_layout.setSpacing(10)
        
        folders_container.setWidget(folders_widget)
        layout.addWidget(folders_container)
        
        self.folders_layout = folders_layout
    
    def _populate_sample_folders(self):
        """Add sample folders for visualization"""
        # Clear existing folders
        for i in reversed(range(self.folders_layout.count())):
            item = self.folders_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        # Add new folder button
        new_folder_frame = QFrame()
        new_folder_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['add_folder_bg']};
                border: 1px dashed {COLORS['divider']};
                border-radius: 8px;
            }}
            QFrame:hover {{
                border: 1px dashed {COLORS['accent']};
            }}
        """)
        new_folder_frame.setFixedHeight(60)
        
        new_folder_layout = QHBoxLayout(new_folder_frame)
        new_folder_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        new_folder_label = QLabel("+ Create New Folder")
        new_folder_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 14px;
        """)
        new_folder_layout.addWidget(new_folder_label)
        
        self.folders_layout.addWidget(new_folder_frame)
        
        # Sample folders
        sample_folders = [
            ("Sound Effects", 12),
            ("Meme Sounds", 8),
            ("Music Clips", 5),
            ("Custom Recordings", 3)
        ]
        
        for name, count in sample_folders:
            folder_item = self.create_folder_item(name, count)
            self.folders_layout.addWidget(folder_item)
        
        self.folders_layout.addStretch()
    
    def create_folder_item(self, name, sound_count):
        """Create a folder item widget"""
        folder_frame = QFrame()
        folder_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['folder_bg']};
                border-radius: 8px;
            }}
            QFrame:hover {{
                background-color: {COLORS['folder_hover']};
            }}
        """)
        folder_frame.setFixedHeight(70)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(folder_frame)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(COLORS['shadow']))
        shadow.setOffset(0, 2)
        folder_frame.setGraphicsEffect(shadow)
        
        folder_layout = QHBoxLayout(folder_frame)
        
        # Folder icon
        folder_icon = QLabel("📁")
        folder_icon.setStyleSheet(f"""
            font-size: 24px;
            color: {COLORS['folder_icon']};
        """)
        folder_layout.addWidget(folder_icon)
        
        # Folder info
        folder_info = QVBoxLayout()
        
        folder_name = QLabel(name)
        folder_name.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 16px;
            font-weight: bold;
        """)
        folder_info.addWidget(folder_name)
        
        folder_count = QLabel(f"{sound_count} sounds")
        folder_count.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 12px;
        """)
        folder_info.addWidget(folder_count)
        
        folder_layout.addLayout(folder_info)
        folder_layout.addStretch()
        
        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        edit_btn = ModernButton("Edit")
        edit_btn.setFixedSize(60, 30)
        actions_layout.addWidget(edit_btn)
        
        play_all_btn = ModernButton("Play All")
        play_all_btn.setFixedSize(80, 30)
        actions_layout.addWidget(play_all_btn)
        
        folder_layout.addLayout(actions_layout)
        
        return folder_frame

class FolderContentView(QFrame):
    """View for displaying sounds in a selected folder"""
    def __init__(self, folder_name, parent=None):
        super().__init__(parent)
        self.folder_name = folder_name
        self._setup_ui()
        
    def _setup_ui(self):
        self.setStyleSheet(f"""
            FolderContentView {{
                background-color: {COLORS['bg_primary']};
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header with folder name and actions
        header = QHBoxLayout()
        
        # Back button
        back_btn = ModernButton("← Back")
        header.addWidget(back_btn)
        
        title = QLabel(self.folder_name)
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 24px;
            font-weight: bold;
            margin-left: 10px;
        """)
        header.addWidget(title)
        
        header.addStretch()
        
        add_sound_btn = ModernButton("+ Add Sound", is_primary=True)
        header.addWidget(add_sound_btn)
        
        layout.addLayout(header)
        
        # Folder content (sounds grid)
        content_area = QScrollArea()
        content_area.setWidgetResizable(True)
        content_area.setFrameShape(QFrame.Shape.NoFrame)
        content_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
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
        
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)
        
        # Sample sound cards for this folder
        sample_sounds = [
            ("Folder Sound 1", 1),
            ("Folder Sound 2", 2),
            ("Folder Sound 3", 3)
        ]
        
        for title, category in sample_sounds:
            card = SoundCard(title, category)
            content_layout.addWidget(card)
        
        content_layout.addStretch()
        
        content_area.setWidget(content_widget)
        layout.addWidget(content_area)

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SoundWave")
        self.setMinimumSize(1200, 800)
        
        # Set window style
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['bg_primary']};
            }}
        """)
        
        # Create main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Create content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Initialize UI components
        self._init_ui()

        # Add control panel
        self.control_panel = ControlPanel()
        self.main_layout.addWidget(self.content_area)
        self.main_layout.addWidget(self.control_panel)

    def _init_ui(self):
        """Initialize UI components"""
        self._create_header()
        self._create_main_content()
        self._create_status_bar()
    
    def _create_header(self):
        """Create the modern header area with gradient"""
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['bg_secondary']},
                    stop:1 {COLORS['bg_primary']});
                border-bottom: 1px solid {COLORS['divider']};
            }}
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(0)
        header_layout.setContentsMargins(24, 16, 24, 0)
        
        # Top bar with title and controls
        top_bar = QHBoxLayout()
        
        # Title with accent
        title_layout = QHBoxLayout()
        icon_label = QLabel("🎵")  # Placeholder for app icon
        icon_label.setStyleSheet(f"font-size: 24px;")
        title_layout.addWidget(icon_label)
        
        title = QLabel("SoundWave")
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 24px;
            font-weight: bold;
        """)
        title_layout.addWidget(title)
        top_bar.addLayout(title_layout)
        
        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)
        
        add_sound_btn = ModernButton("+ Add Sound", is_primary=True)
        settings_btn = ModernButton("⚙ Settings")
        
        controls_layout.addWidget(add_sound_btn)
        controls_layout.addWidget(settings_btn)
        
        top_bar.addStretch()
        top_bar.addLayout(controls_layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 16, 0, 0)
        search_bar = SearchBar()
        search_layout.addWidget(search_bar)
        
        # Category tabs
        tabs_layout = QHBoxLayout()
        tabs_layout.setSpacing(4)
        tabs_layout.setContentsMargins(0, 16, 0, 0)
        
        categories = ["All Sounds", "Favourites", "Folders"]
        self.category_buttons = []
        
        for category in categories:
            tab = ModernButton(category)
            tab.setCheckable(True)
            if category == "All Sounds":
                tab.setChecked(True)
            self.category_buttons.append(tab)
            tabs_layout.addWidget(tab)
        
        tabs_layout.addStretch()
        
        # View controls
        controls_right = QHBoxLayout()
        controls_right.setSpacing(8)

        view_toggle = ModernButton("□ Grid View")
        sort_btn = ModernButton("Sort: Recent")

        controls_right.addWidget(view_toggle)
        controls_right.addWidget(sort_btn)
        tabs_layout.addLayout(controls_right)

        header_layout.addLayout(top_bar)
        header_layout.addLayout(search_layout)
        header_layout.addLayout(tabs_layout)
        
        self.content_layout.addWidget(header)
    
    def _create_main_content(self):
        """Create the main content area with stacked views"""
        # Create stacked widget for different views
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"""
            background-color: {COLORS['bg_primary']};
        """)
        
        # Sound grid view (default)
        self.sound_grid_view = self._create_sound_grid_view()
        self.content_stack.addWidget(self.sound_grid_view)
        
        # Folder view 
        self.folder_view = FolderView()
        self.content_stack.addWidget(self.folder_view)
        
        # Folder content view sample
        self.folder_content_view = FolderContentView("Sound Effects")
        self.content_stack.addWidget(self.folder_content_view)
        
        self.content_layout.addWidget(self.content_stack)
    
    def _create_sound_grid_view(self):
        """Create the main sound grid view"""
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
        
        # Sound grid with cards
        grid_widget = QWidget()
        grid_widget.setStyleSheet(f"""
            background-color: {COLORS['bg_primary']};
        """)
        grid_layout = QHBoxLayout(grid_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(16)
        
        # Add some sample sound cards
        sample_sounds = [
            ("Epic Bass", 1),
            ("Guitar Riff", 2),
            ("Voice Effect", 3),
            ("Custom Sound", 4)
        ]
        
        for title, category in sample_sounds:
            card = SoundCard(title, category)
            grid_layout.addWidget(card)
        
        grid_layout.addStretch()
        
        scroll_area.setWidget(grid_widget)
        content_layout.addWidget(scroll_area)
        
        return content_area
    
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
        status_bar.addWidget(QLabel("4 sounds loaded"))
        status_bar.addPermanentWidget(QLabel("Version 0.1.0")) 