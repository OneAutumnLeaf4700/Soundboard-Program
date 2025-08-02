"""
Main Window Implementation with Enhanced Modern Design
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStatusBar, QMenuBar, QMenu, QLabel,
    QPushButton, QScrollArea, QFrame, QSizePolicy,
    QStackedWidget, QGraphicsDropShadowEffect, QSlider,
    QLineEdit, QComboBox, QCheckBox, QTreeWidget, QTreeWidgetItem,
    QGridLayout, QButtonGroup, QListWidget, QTabWidget, QSpacerItem
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve
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
    'resize_small': '#404040',
    'resize_medium': '#505050',
    'resize_large': '#606060',
    'button_hover': '#353535',  # Add button hover color
    'accent_light': '#2A4A3C',  # Add accent light color for hover effects
    'accent_hover': '#1ED760',  # Add accent hover color
    'scrollbar_bg': '#1A1A1A',  # Add scrollbar background color
    'scrollbar_handle': '#404040',  # Add scrollbar handle color
    'count_badge_bg': '#383838',  # Add count badge background color
    'favorite_color': '#FFD700',  # Gold color for favorites
    'favorite_hover': '#FFC107',  # Lighter gold for hover
    'delete_color': '#E53935',  # Red color for delete button
    'accent_color': '#1DB954',  # Add accent color for folder icon
}

class SearchBar(QLineEdit):
    """Modern search bar with icon"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Search...")
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
        self.setFixedWidth(300)
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
    sound_clicked = pyqtSignal(str, str)  # Emits sound_id and action
    
    def __init__(self, title, category, sound_id="", is_favorite=False, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.title = title
        self.category = category
        self.sound_id = sound_id
        self.is_active = False
        self.is_favorite = is_favorite
        
        # Import here to avoid circular imports
        from managers.sound_manager import SoundManager
        self.sound_manager = SoundManager()
        
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
        
        # Top section with category, title and menu
        top_section = QHBoxLayout()
        
        # Category indicator
        category_indicator = QFrame()
        category_indicator.setFixedSize(4, 20)
        category_indicator.setStyleSheet(f"""
            background-color: {COLORS[f'category_{self.category}']};
            border-radius: 2px;
        """)
        top_section.addWidget(category_indicator)
        
        # Sound title at top left
        title_label = QLabel(self.title)
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: bold;
            margin-left: 4px;
        """)
        top_section.addWidget(title_label)
        
        top_section.addStretch()
        
        # Menu button (3 vertical dots)
        self.menu_button = QPushButton("⋮")
        self.menu_button.setFixedSize(24, 24)
        self.menu_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.menu_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border-radius: 12px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
        """)
        self.menu_button.clicked.connect(self._show_context_menu)
        top_section.addWidget(self.menu_button)
        
        layout.addLayout(top_section)
        
        # Waveform placeholder with gradient
        waveform = QFrame()
        waveform.setFixedHeight(80)
        waveform.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['bg_secondary']},
                stop:1 {COLORS['bg_elevated']});
            border-radius: 4px;
        """)
        layout.addWidget(waveform)
        
        # Bottom controls
        controls = QHBoxLayout()
        
        # Play button with improved icon
        play_btn = ModernButton("▶ Play")
        play_btn.setFixedHeight(32)
        play_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['accent_gradient_start']},
                    stop:1 {COLORS['accent_gradient_end']});
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 16px;
                font-size: 12px;
                font-weight: bold;
                padding: 4px 12px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['accent']},
                    stop:1 {COLORS['accent']});
            }}
        """)
        controls.addWidget(play_btn)
        
        controls.addStretch()
        
        # Favorite button
        self.favorite_btn = QPushButton()
        self.favorite_btn.setFixedSize(24, 24)
        self._update_favorite_button()
        self.favorite_btn.clicked.connect(self._toggle_favorite)
        controls.addWidget(self.favorite_btn)
        
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
    
    def _update_favorite_button(self):
        """Update favorite button appearance based on state"""
        if self.is_favorite:
            # Filled star for favorite
            self.favorite_btn.setText("★")
            self.favorite_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: gold;
                    border: none;
                    font-size: 16px;
                }}
                QPushButton:hover {{
                    color: #FFC107;
                }}
            """)
        else:
            # Empty star for non-favorite
            self.favorite_btn.setText("☆")
            self.favorite_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {COLORS['text_secondary']};
                    border: none;
                    font-size: 16px;
                }}
                QPushButton:hover {{
                    color: gold;
                }}
            """)
    
    def _toggle_favorite(self):
        """Toggle favorite status using sound manager"""
        # Use the sound manager to toggle favorite status
        if self.sound_id:
            self.is_favorite = self.sound_manager.toggle_favorite(self.sound_id)
            self._update_favorite_button()
            self.sound_clicked.emit(self.sound_id, "favorite" if self.is_favorite else "unfavorite")
    
    def _show_context_menu(self):
        """Show context menu with actions"""
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {COLORS['bg_elevated']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 16px;
                color: {COLORS['text_primary']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['card_hover']};
                color: {COLORS['accent']};
            }}
        """)
        
        edit_action = QAction("Edit", menu)
        edit_action.triggered.connect(lambda: self.sound_clicked.emit(self.sound_id, "edit"))
        menu.addAction(edit_action)
        
        delete_action = QAction("Delete", menu)
        delete_action.triggered.connect(lambda: self.sound_clicked.emit(self.sound_id, "delete"))
        menu.addAction(delete_action)
        
        # Add favorite/unfavorite option
        if self.is_favorite:
            unfav_action = QAction("Remove from Favorites", menu)
            unfav_action.triggered.connect(self._toggle_favorite)
            menu.addAction(unfav_action)
        else:
            fav_action = QAction("Add to Favorites", menu)
            fav_action.triggered.connect(self._toggle_favorite)
            menu.addAction(fav_action)
        
        menu.exec(self.mapToGlobal(self.menu_button.pos() + QPoint(0, self.menu_button.height())))

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
    
    def mousePressEvent(self, event):
        """Handle click event (play sound)"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Ignore clicks on buttons
            if not self.menu_button.geometry().contains(event.pos()) and not self.favorite_btn.geometry().contains(event.pos()):
                self.sound_clicked.emit(self.sound_id, "play")
        super().mousePressEvent(event)

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

class SizeButton(QFrame):
    """Button for changing sound card size"""
    def __init__(self, size_name, is_active=False, parent=None):
        super().__init__(parent)
        self.size_name = size_name
        self.is_active = is_active
        self._setup_ui()
        
    def _setup_ui(self):
        self.setFixedSize(24, 24)
        
        # Set base style based on size
        if self.size_name == "small":
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['resize_small']};
                    border-radius: 4px;
                    border: 1px solid {COLORS['divider']};
                }}
                QFrame:hover {{
                    background-color: {COLORS['card_hover']};
                    border: 1px solid {COLORS['accent']};
                }}
            """)
        elif self.size_name == "medium":
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['resize_medium']};
                    border-radius: 4px;
                    border: 1px solid {COLORS['divider']};
                }}
                QFrame:hover {{
                    background-color: {COLORS['card_hover']};
                    border: 1px solid {COLORS['accent']};
                }}
            """)
        else:  # large
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['resize_large']};
                    border-radius: 4px;
                    border: 1px solid {COLORS['divider']};
                }}
                QFrame:hover {{
                    background-color: {COLORS['card_hover']};
                    border: 1px solid {COLORS['accent']};
                }}
            """)
        
        # If active, highlight with accent color
        if self.is_active:
            self.setStyleSheet(self.styleSheet() + f"""
                QFrame {{
                    border: 2px solid {COLORS['accent']};
                }}
            """)

class ViewControls(QFrame):
    """Controls for view options (grid/list, size)"""
    # Add signals
    grid_view_toggled = pyqtSignal(bool)
    size_changed = pyqtSignal(str)
    sort_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # View label
        view_label = QLabel("View:")
        view_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(view_label)
        
        # View toggle buttons
        self.view_toggle_group = QButtonGroup(self)
        
        view_buttons_layout = QHBoxLayout()
        view_buttons_layout.setSpacing(4)
        
        # Grid view button
        self.grid_btn = QPushButton("Grid")
        self.grid_btn.setCheckable(True)
        self.grid_btn.setChecked(True)
        self.grid_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.grid_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['divider']};
                border-top-left-radius: 4px;
                border-bottom-left-radius: 4px;
                padding: 4px 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
            QPushButton:checked {{
                background-color: {COLORS['accent']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['accent']};
            }}
        """)
        self.view_toggle_group.addButton(self.grid_btn)
        view_buttons_layout.addWidget(self.grid_btn)
        
        # List view button
        self.list_btn = QPushButton("List")
        self.list_btn.setCheckable(True)
        self.list_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.list_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['divider']};
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
                padding: 4px 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
            QPushButton:checked {{
                background-color: {COLORS['accent']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['accent']};
            }}
        """)
        self.view_toggle_group.addButton(self.list_btn)
        view_buttons_layout.addWidget(self.list_btn)
        
        layout.addLayout(view_buttons_layout)
        
        # Add some spacing
        layout.addSpacing(8)
        
        # Size label
        size_label = QLabel("Size:")
        size_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(size_label)
        
        # Size combobox
        self.size_combo = QComboBox()
        self.size_combo.addItems(["Small", "Medium", "Large"])
        self.size_combo.setCurrentIndex(1)  # Medium by default
        self.size_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 4px 8px;
                min-width: 100px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['divider']};
                selection-background-color: {COLORS['accent']};
            }}
        """)
        self.size_combo.currentIndexChanged.connect(self._on_size_changed)
        layout.addWidget(self.size_combo)
        
        # Add some spacing
        layout.addSpacing(8)
        
        # Sort label
        sort_label = QLabel("Sort:")
        sort_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(sort_label)
        
        # Sort combobox
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Default", "Name", "Sound Count"])
        self.sort_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 4px 8px;
                min-width: 100px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['divider']};
                selection-background-color: {COLORS['accent']};
            }}
        """)
        self.sort_combo.currentIndexChanged.connect(self._on_sort_changed)
        layout.addWidget(self.sort_combo)
        
        # Connect signals
        self.grid_btn.toggled.connect(self._on_view_toggled)
        self.list_btn.toggled.connect(lambda checked: self._on_view_toggled(not checked))
    
    def _on_view_toggled(self, is_grid_view):
        """Handle view toggle buttons"""
        if is_grid_view:
            self.grid_btn.setChecked(True)
            self.list_btn.setChecked(False)
        else:
            self.grid_btn.setChecked(False)
            self.list_btn.setChecked(True)
        
        # Emit signal with the current state
        self.grid_view_toggled.emit(is_grid_view)
    
    def _on_size_changed(self, index):
        """Handle size combo box change"""
        sizes = ["small", "medium", "large"]
        if 0 <= index < len(sizes):
            # Emit signal with the selected size
            self.size_changed.emit(sizes[index])
    
    def _on_sort_changed(self, index):
        """Handle sort combo box change"""
        sorts = ["default", "name", "sound_count"]
        if 0 <= index < len(sorts):
            # Emit signal with the selected sort option
            self.sort_changed.emit(sorts[index])

class SoundGridView(QFrame):
    """Main sound grid view"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sounds = []
        self.sound_manager = None  # Will be set by MainWindow
        self._setup_ui()
        
    def set_sound_manager(self, sound_manager):
        """Set the sound manager for this view"""
        self.sound_manager = sound_manager
        
    def _on_add_sound_clicked(self):
        """Handle add sound button click"""
        if not self.sound_manager:
            # Import here to avoid circular imports if sound_manager not set
            from managers.sound_manager import SoundManager
            sound_manager = SoundManager()
        else:
            sound_manager = self.sound_manager
            
        # Open file dialog and add sound
        sound_id = sound_manager.select_and_add_sound_file(self)
        if sound_id:
            # Refresh the view
            self._refresh_sounds()
    
    def _refresh_sounds(self):
        """Refresh the sounds display"""
        if not self.sound_manager:
            return
            
        # Clear current sounds
        self.sounds = []
        
        # Get all sounds from the sound manager
        all_sounds = self.sound_manager.get_all_sounds()
        
        # Convert to list format for our view
        for sound_id, sound_data in all_sounds.items():
            # Add sound_id to the data
            sound_item = sound_data.copy()
            sound_item["id"] = sound_id
            self.sounds.append(sound_item)
            
        # Clear current grid
        while self.sound_grid.count():
            item = self.sound_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Clear current list view (except the stretch at the end)
        for i in range(self.sound_list_layout.count() - 1, -1, -1):
            item = self.sound_list_layout.itemAt(i)
            if item and not isinstance(item, QSpacerItem):
                widget = item.widget()
                if widget:
                    self.sound_list_layout.removeWidget(widget)
                    widget.deleteLater()
        
        # Recreate sound cards and list items
        for i, sound in enumerate(self.sounds):
            self._create_sound_card(i, sound)
            self._create_sound_list_item(sound["id"], sound["title"], sound["category"], sound.get("is_favorite", False))
        
    def _setup_ui(self):
        self.setStyleSheet(f"""
            SoundGridView {{
                background-color: {COLORS['bg_primary']};
                border: none;
            }}
            QFrame#sound_item:hover, QFrame#sound_card:hover {{
                background-color: {COLORS['card_hover']};
                border: 1px solid {COLORS['accent']};
            }}
            QLabel, QPushButton {{
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header with title, search bar and add button
        header = QHBoxLayout()
        
        title = QLabel("All Sounds")
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 24px;
            font-weight: bold;
        """)
        header.addWidget(title)
        
        header.addStretch()
        
        # Search bar
        search_bar = SearchBar()
        header.addWidget(search_bar)
        
        # Add sound button
        add_sound_btn = ModernButton("+ Add Sound", is_primary=True)
        add_sound_btn.clicked.connect(self._on_add_sound_clicked)
        header.addWidget(add_sound_btn)
        
        layout.addLayout(header)
        
        # View controls
        controls_layout = QHBoxLayout()
        self.view_controls = ViewControls()
        # Customize sort options for sounds
        self.view_controls.sort_combo.clear()
        self.view_controls.sort_combo.addItems(["Recent", "Name", "Duration"])
        self.view_controls.grid_view_toggled.connect(self._toggle_view)
        self.view_controls.size_changed.connect(self._change_size)
        self.view_controls.sort_changed.connect(self._sort_sounds)
        controls_layout.addWidget(self.view_controls)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Create stacked widget for different views
        self.view_stack = QStackedWidget()
        
        # Grid view for sounds
        self.grid_view = self._create_grid_view()
        self.view_stack.addWidget(self.grid_view)
        
        # List view for sounds
        self.list_view = self._create_list_view()
        self.view_stack.addWidget(self.list_view)
        
        # Add the stacked widget to the main layout
        layout.addWidget(self.view_stack)
        
        # Set default view
        self.view_stack.setCurrentIndex(0)  # Start with grid view
        
    def _create_grid_view(self):
        """Create the grid view for sounds"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
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
        
        self.grid_content = QWidget()
        self.sound_grid = QGridLayout(self.grid_content)
        self.sound_grid.setContentsMargins(0, 0, 0, 0)
        self.sound_grid.setSpacing(16)
        
        scroll_area.setWidget(self.grid_content)
        return scroll_area
        
    def _create_list_view(self):
        """Create the list view for sounds"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
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
        
        list_container = QWidget()
        self.sound_list_layout = QVBoxLayout(list_container)
        self.sound_list_layout.setContentsMargins(0, 0, 0, 0)
        self.sound_list_layout.setSpacing(8)
        self.sound_list_layout.addStretch()
        
        scroll_area.setWidget(list_container)
        return scroll_area
    
    def _populate_sample_sounds(self):
        """Add sample sounds for visualization"""
        # Sample sounds
        sample_sounds = [
            {"id": "sound1", "title": "Epic Bass Drop", "category": 1, "duration": "0:30", "favorite": False},
            {"id": "sound2", "title": "Guitar Riff", "category": 2, "duration": "0:15", "favorite": True},
            {"id": "sound3", "title": "Voice Effect", "category": 3, "duration": "0:10", "favorite": False},
            {"id": "sound4", "title": "Custom Sound", "category": 4, "duration": "0:22", "favorite": False},
            {"id": "sound5", "title": "Drum Roll", "category": 1, "duration": "0:08", "favorite": False},
            {"id": "sound6", "title": "Synth Wave", "category": 2, "duration": "0:45", "favorite": True},
            {"id": "sound7", "title": "Record Scratch", "category": 3, "duration": "0:02", "favorite": False},
            {"id": "sound8", "title": "Crowd Cheer", "category": 4, "duration": "0:12", "favorite": False},
            {"id": "sound9", "title": "Glass Breaking", "category": 1, "duration": "0:03", "favorite": False},
            {"id": "sound10", "title": "Air Horn", "category": 2, "duration": "0:05", "favorite": False},
            {"id": "sound11", "title": "Applause", "category": 3, "duration": "0:10", "favorite": True},
            {"id": "sound12", "title": "Door Slam", "category": 4, "duration": "0:02", "favorite": False}
        ]
        
        # Store sound data
        self.sounds = sample_sounds
        
        # Create sound cards for grid view and list items for list view
        for i, sound in enumerate(self.sounds):
            self._create_sound_card(i, sound)
            self._create_sound_list_item(sound)
    
    def _create_sound_card(self, index, sound_data):
        """Create a sound card widget and add it to the grid"""
        columns = 4  # Default column count
        row = index // columns
        col = index % columns
        
        # Create the sound card
        card = SoundCard(sound_data["title"], sound_data["category"], sound_data["id"], sound_data["favorite"])
        card.setObjectName("sound_card")  # Set object name for styling
        card.sound_clicked.connect(self._on_sound_action)
        
        # Add to grid
        self.sound_grid.addWidget(card, row, col)
    
    def _create_sound_list_item(self, sound_data):
        """Create a list item for a sound in list view"""
        item = QFrame()
        item.setObjectName("sound_item")
        item.setCursor(Qt.CursorShape.PointingHandCursor)
        item.setFixedHeight(60)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(16, 8, 16, 8)
        
        # Category color indicator
        category_color = COLORS.get(f'category_{sound_data["category"]}', COLORS['accent'])
        color_indicator = QFrame()
        color_indicator.setFixedSize(4, 20)
        color_indicator.setStyleSheet(f"""
            background-color: {category_color};
            border-radius: 2px;
        """)
        layout.addWidget(color_indicator)
        
        # Sound icon
        icon_label = QLabel("🔊")
        icon_label.setStyleSheet(f"""
            font-size: 18px;
            color: {category_color};
            margin-left: 4px;
        """)
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(sound_data["title"])
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: bold;
            margin-left: 8px;
        """)
        layout.addWidget(title_label, 1)
        
        # Duration
        duration_label = QLabel(sound_data["duration"])
        duration_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 12px;
        """)
        layout.addWidget(duration_label)
        
        # Favorite button
        fav_btn = QPushButton("★" if sound_data["favorite"] else "☆")
        fav_btn.setFixedSize(24, 24)
        fav_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        fav_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {('gold' if sound_data["favorite"] else COLORS['text_secondary'])};
                border: none;
                font-size: 16px;
            }}
            QPushButton:hover {{
                color: gold;
            }}
        """)
        fav_btn.clicked.connect(lambda: self._on_sound_action(sound_data["id"], "favorite"))
        layout.addWidget(fav_btn)
        
        # Play button
        play_btn = QPushButton("▶")
        play_btn.setFixedSize(30, 30)
        play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        play_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: {COLORS['text_primary']};
                border-radius: 15px;
                border: none;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gradient_start']};
            }}
        """)
        play_btn.clicked.connect(lambda: self._on_sound_action(sound_data["id"], "play"))
        layout.addWidget(play_btn)
        
        # Menu button (3 dots)
        menu_btn = QPushButton("⋮")
        menu_btn.setFixedSize(30, 30)
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border-radius: 12px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
        """)
        menu_btn.clicked.connect(lambda: self._show_sound_menu(sound_data["id"], menu_btn))
        layout.addWidget(menu_btn)
        
        # Add to list
        self.sound_list_layout.insertWidget(self.sound_list_layout.count() - 1, item)
        
    def _show_sound_menu(self, sound_id, button):
        """Show context menu for sound"""
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {COLORS['bg_elevated']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 16px;
                color: {COLORS['text_primary']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['card_hover']};
                color: {COLORS['accent']};
            }}
        """)
        
        edit_action = QAction("Edit", menu)
        edit_action.triggered.connect(lambda: self._on_sound_action(sound_id, "edit"))
        menu.addAction(edit_action)
        
        delete_action = QAction("Delete", menu)
        delete_action.triggered.connect(lambda: self._on_sound_action(sound_id, "delete"))
        menu.addAction(delete_action)
        
        menu.exec(button.mapToGlobal(QPoint(0, button.height())))
    
    def _toggle_view(self, is_grid_view):
        """Toggle between grid and list view"""
        self.view_stack.setCurrentIndex(0 if is_grid_view else 1)
    
    def _change_size(self, size):
        """Change the size of sound cards in grid view"""
        self.current_size = size
        
        sizes = {
            "small": (160, 140),
            "medium": (200, 180),
            "large": (240, 220)
        }
        
        if size in sizes:
            # Adjust size of all sound cards in the folder content view
            for i in range(self.sound_grid.count()):
                item = self.sound_grid.itemAt(i)
                if item and item.widget():
                    card = item.widget()
                    card.setFixedSize(*sizes[size])
            
            # Adjust columns in grid based on size to prevent overflow
            columns = 4  # Default for small and medium
            if size == "large":
                columns = 3
            
            # Rearrange items in grid with new column count
            widgets = []
            while self.sound_grid.count():
                item = self.sound_grid.takeAt(0)
                if item.widget():
                    widgets.append(item.widget())
            
            for i, widget in enumerate(widgets):
                row = i // columns
                col = i % columns
                self.sound_grid.addWidget(widget, row, col)
    
    def _sort_sounds(self, sort_by):
        """Sort sounds according to criteria"""
        print(f"Sorting sounds by: {sort_by}")
        
        # Get a copy of sound data to sort
        sorted_sounds = self.sounds.copy()
        
        if sort_by == "name":
            sorted_sounds.sort(key=lambda s: s["title"])
        elif sort_by == "duration":
            sorted_sounds.sort(key=lambda s: s["duration"])
        # Default is "recent" (original order)
        
        # Clear current grid
        while self.sound_grid.count():
            item = self.sound_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Clear current list view (except the stretch at the end)
        for i in range(self.sound_list_layout.count() - 1, -1, -1):
            item = self.sound_list_layout.itemAt(i)
            if item and not isinstance(item, QSpacerItem):
                widget = item.widget()
                if widget:
                    self.sound_list_layout.removeWidget(widget)
                    widget.deleteLater()
        
        # Recreate sound cards and list items in sorted order
        for i, sound in enumerate(sorted_sounds):
            self._create_sound_card(i, sound)
            self._create_sound_list_item(sound)
            
    def _on_sound_action(self, sound_id, action):
        """Handle sound actions"""
        print(f"Sound {sound_id} action: {action}")
        
        if not self.sound_manager:
            # Import here to avoid circular imports if sound_manager not set
            from managers.sound_manager import SoundManager
            sound_manager = SoundManager()
        else:
            sound_manager = self.sound_manager
        
        if action == "favorite" or action == "unfavorite":
            # Toggle favorite status
            is_favorite = sound_manager.toggle_favorite(sound_id)
            
            # Update UI
            self._update_sound_favorite_status(sound_id, is_favorite)
            
        elif action == "play":
            # Play the sound
            sound_manager.play_sound(sound_id)
        elif action == "delete":
            # Remove the sound
            if sound_manager.remove_sound(sound_id):
                # Refresh the view
                self._refresh_sounds()
        elif action == "edit":
            # Edit sound functionality would go here
            pass
            
    def _on_add_sound_clicked(self):
        """Handle add sound button click"""
        if not self.sound_manager:
            # Import here to avoid circular imports if sound_manager not set
            from managers.sound_manager import SoundManager
            sound_manager = SoundManager()
        else:
            sound_manager = self.sound_manager
            
        # Open file dialog and add sound
        sound_id = sound_manager.select_and_add_sound_file(self)
        if sound_id:
            # Refresh the view to show the new sound
            self._refresh_sounds()
            
    def _refresh_sounds(self):
        """Refresh the sounds display"""
        if not self.sound_manager:
            return
            
        # Clear current sounds
        self.sounds = []
        
        # Get all sounds from the sound manager
        all_sounds = self.sound_manager.get_all_sounds()
        
        # Convert to list format for our view
        for sound_id, sound_data in all_sounds.items():
            # Add sound_id to the data
            sound_item = sound_data.copy()
            sound_item["id"] = sound_id
            self.sounds.append(sound_item)
            
        # Clear current grid
        while self.sound_grid.count():
            item = self.sound_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Clear current list view (except the stretch at the end)
        for i in range(self.sound_list_layout.count() - 1, -1, -1):
            item = self.sound_list_layout.itemAt(i)
            if item and not isinstance(item, QSpacerItem):
                widget = item.widget()
                if widget:
                    self.sound_list_layout.removeWidget(widget)
                    widget.deleteLater()
        
        # Recreate sound cards and list items
        for i, sound in enumerate(self.sounds):
            self._create_sound_card(i, sound)
            self._create_sound_list_item(sound)
    
    def _update_sound_favorite_status(self, sound_id, is_favorite):
        """Update the UI to reflect the favorite status of a sound"""
        # Update in grid view
        for i in range(self.sound_grid.count()):
            item = self.sound_grid.itemAt(i)
            if item and item.widget():
                card = item.widget()
                if hasattr(card, 'sound_id') and card.sound_id == sound_id:
                    card.is_favorite = is_favorite
                    card._update_favorite_button()
        
        # Update in list view
        for i in range(self.sound_list_layout.count()):
            item = self.sound_list_layout.itemAt(i)
            if item and item.widget() and not isinstance(item, QSpacerItem):
                list_item = item.widget()
                # Find the favorite button in the list item
                for child in list_item.children():
                    if isinstance(child, QPushButton) and child.text() in ["★", "☆"]:
                        # Update the favorite button
                        child.setText("★" if is_favorite else "☆")
                        child.setStyleSheet(f"""
                            QPushButton {{
                                background-color: transparent;
                                color: {('gold' if is_favorite else COLORS['text_secondary'])};
                                border: none;
                                font-size: 16px;
                            }}
                            QPushButton:hover {{
                                color: gold;
                            }}
                        """)
                        break
                        
    def _update_sound(self, sound_id, sound_data):
        """Update a sound's data in the UI
        
        Args:
            sound_id: The ID of the sound to update
            sound_data: The updated sound data
        """
        # Check if the sound exists in our list
        found = False
        for i, sound in enumerate(self.sounds):
            if sound["id"] == sound_id:
                # Update the sound data
                self.sounds[i] = sound_data.copy()
                self.sounds[i]["id"] = sound_id
                found = True
                break
                
        if not found:
            # If the sound is not in our list, add it
            sound_item = sound_data.copy()
            sound_item["id"] = sound_id
            self.sounds.append(sound_item)
            
        # Update the UI
        # First, update favorite status if it changed
        if "favorite" in sound_data:
            self._update_sound_favorite_status(sound_id, sound_data["favorite"])
            
        # For more complex changes, refresh the entire view
        # This is a simple approach - for better performance, you could update just the affected widgets
        self._refresh_sounds()

class FavoriteSoundCard(SoundCard):
    """Modified SoundCard for the favorites view without the favorite button"""
    def __init__(self, title, category, sound_id="", parent=None):
        super().__init__(title, category, sound_id, True, parent)
        
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
        
        # Top section with category, title and menu
        top_section = QHBoxLayout()
        
        # Category indicator
        category_indicator = QFrame()
        category_indicator.setFixedSize(4, 20)
        category_indicator.setStyleSheet(f"""
            background-color: {COLORS[f'category_{self.category}']};
            border-radius: 2px;
        """)
        top_section.addWidget(category_indicator)
        
        # Sound title at top left
        title_label = QLabel(self.title)
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: bold;
            margin-left: 4px;
        """)
        top_section.addWidget(title_label)
        
        top_section.addStretch()
        
        # Menu button (3 vertical dots)
        self.menu_button = QPushButton("⋮")
        self.menu_button.setFixedSize(24, 24)
        self.menu_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.menu_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border-radius: 12px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
        """)
        self.menu_button.clicked.connect(self._show_context_menu)
        top_section.addWidget(self.menu_button)
        
        layout.addLayout(top_section)
        
        # Waveform placeholder with gradient
        waveform = QFrame()
        waveform.setFixedHeight(80)
        waveform.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['bg_secondary']},
                stop:1 {COLORS['bg_elevated']});
            border-radius: 4px;
        """)
        layout.addWidget(waveform)
        
        # Bottom controls
        controls = QHBoxLayout()
        
        # Play button with improved icon
        play_btn = ModernButton("▶ Play")
        play_btn.setFixedHeight(32)
        play_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['accent_gradient_start']},
                    stop:1 {COLORS['accent_gradient_end']});
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 16px;
                font-size: 12px;
                font-weight: bold;
                padding: 4px 12px;
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
    
    def _show_context_menu(self):
        """Show context menu with actions (without favorite option)"""
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {COLORS['bg_elevated']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 16px;
                color: {COLORS['text_primary']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['card_hover']};
                color: {COLORS['accent']};
            }}
        """)
        
        edit_action = QAction("Edit", menu)
        edit_action.triggered.connect(lambda: self.sound_clicked.emit(self.sound_id, "edit"))
        menu.addAction(edit_action)
        
        delete_action = QAction("Delete", menu)
        delete_action.triggered.connect(lambda: self.sound_clicked.emit(self.sound_id, "delete"))
        menu.addAction(delete_action)
        
        # No favorite/unfavorite option in favorites view
        
        menu.exec(self.mapToGlobal(self.menu_button.pos() + QPoint(0, self.menu_button.height())))

class FavouritesView(QFrame):
    """View for favourites sounds"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.favorite_sounds = []
        self.sound_manager = None  # Will be set by MainWindow
        self._setup_ui()
        
    def _setup_ui(self):
        self.setStyleSheet(f"""
            FavouritesView {{
                background-color: {COLORS['bg_primary']};
                border: none;
            }}
            QFrame#favorite_item:hover, QFrame#favorite_card:hover {{
                background-color: {COLORS['card_hover']};
                border: 1px solid {COLORS['accent']};
            }}
            QLabel, QPushButton {{
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header with title, search bar and add button
        header = QHBoxLayout()
        
        title = QLabel("Favourites")
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 24px;
            font-weight: bold;
        """)
        header.addWidget(title)
        
        header.addStretch()
        
        # Search bar
        search_bar = SearchBar()
        header.addWidget(search_bar)
        
        # Add sound button
        add_sound_btn = ModernButton("+ Add Sound", is_primary=True)
        add_sound_btn.clicked.connect(self._on_add_sound_clicked)
        header.addWidget(add_sound_btn)
        
        layout.addLayout(header)
        
        # View controls
        controls_layout = QHBoxLayout()
        self.view_controls = ViewControls()
        # Customize sort options for favorites
        self.view_controls.sort_combo.clear()
        self.view_controls.sort_combo.addItems(["Recent", "Name", "Duration"])
        self.view_controls.grid_view_toggled.connect(self._toggle_view)
        self.view_controls.size_changed.connect(self._change_size)
        self.view_controls.sort_changed.connect(self._sort_favorites)
        controls_layout.addWidget(self.view_controls)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Create stacked widget for different views
        self.view_stack = QStackedWidget()
        
        # Grid view for favorites
        self.grid_view = self._create_grid_view()
        self.view_stack.addWidget(self.grid_view)
        
        # List view for favorites
        self.list_view = self._create_list_view()
        self.view_stack.addWidget(self.list_view)
        
        # Add the stacked widget to the main layout
        layout.addWidget(self.view_stack)
        
        # Set default view
        self.view_stack.setCurrentIndex(0)  # Start with grid view
        
    def _create_grid_view(self):
        """Create the grid view for favorite sounds"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
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
        
        self.grid_content = QWidget()
        self.favorites_grid = QGridLayout(self.grid_content)
        self.favorites_grid.setContentsMargins(0, 0, 0, 0)
        self.favorites_grid.setSpacing(16)
        
        scroll_area.setWidget(self.grid_content)
        return scroll_area
        
    def _create_list_view(self):
        """Create the list view for favorite sounds"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
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
        
        list_container = QWidget()
        self.favorites_list_layout = QVBoxLayout(list_container)
        self.favorites_list_layout.setContentsMargins(0, 0, 0, 0)
        self.favorites_list_layout.setSpacing(8)
        self.favorites_list_layout.addStretch()
        
        scroll_area.setWidget(list_container)
        return scroll_area
    
    def _populate_sample_favorites(self):
        """Add sample favorite sounds for visualization"""
        # Sample favorite sounds
        sample_favorites = [
            {"id": "fav1", "title": "Favorite Sound 1", "category": 1, "duration": "0:20", "favorite": True},
            {"id": "fav2", "title": "Favorite Sound 2", "category": 2, "duration": "0:15", "favorite": True},
            {"id": "fav3", "title": "Favorite Sound 3", "category": 3, "duration": "0:30", "favorite": True},
            {"id": "fav4", "title": "Favorite Sound 4", "category": 4, "duration": "0:10", "favorite": True},
            {"id": "fav5", "title": "Favorite Sound 5", "category": 1, "duration": "0:25", "favorite": True},
            {"id": "fav6", "title": "Favorite Sound 6", "category": 2, "duration": "0:18", "favorite": True}
        ]
        
        # Store favorite sound data
        self.favorite_sounds = sample_favorites
        
        # Create favorite sound cards for grid view and list items for list view
        for i, sound in enumerate(self.favorite_sounds):
            self._create_favorite_card(i, sound)
            self._create_favorite_list_item(sound)
    
    def _create_favorite_card(self, index, sound_data):
        """Create a favorite sound card widget and add it to the grid"""
        columns = 4  # Default column count
        row = index // columns
        col = index % columns
        
        # Create the favorite sound card
        card = FavoriteSoundCard(sound_data["title"], sound_data["category"], sound_data["id"])
        card.setObjectName("favorite_card")  # Set object name for styling
        card.sound_clicked.connect(self._on_favorite_action)
        
        # Add to grid
        self.favorites_grid.addWidget(card, row, col)
    
    def _on_add_sound_clicked(self):
        """Handle add sound button click"""
        if not self.sound_manager:
            # Import here to avoid circular imports if sound_manager not set
            from managers.sound_manager import SoundManager
            sound_manager = SoundManager()
        else:
            sound_manager = self.sound_manager
            
        # Open file dialog and add sound
        sound_id = sound_manager.select_and_add_sound_file(self)
        if sound_id:
            # Add to favorites
            sound_manager.add_to_favorites(sound_id)
            # Refresh the view
            self.update_favorites()
    
    def _create_favorite_list_item(self, sound_data):
        """Create a list item for a favorite sound in list view"""
        item = QFrame()
        item.setObjectName("favorite_item")
        item.setCursor(Qt.CursorShape.PointingHandCursor)
        item.setFixedHeight(60)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(16, 8, 16, 8)
        
        # Category color indicator
        category_color = COLORS.get(f'category_{sound_data["category"]}', COLORS['accent'])
        color_indicator = QFrame()
        color_indicator.setFixedSize(4, 20)
        color_indicator.setStyleSheet(f"""
            background-color: {category_color};
            border-radius: 2px;
        """)
        layout.addWidget(color_indicator)
        
        # Sound icon
        icon_label = QLabel("🔊")
        icon_label.setStyleSheet(f"""
            font-size: 18px;
            color: {category_color};
            margin-left: 4px;
        """)
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(sound_data["title"])
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: bold;
            margin-left: 8px;
        """)
        layout.addWidget(title_label, 1)
        
        # Duration
        duration_label = QLabel(sound_data["duration"])
        duration_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 12px;
        """)
        layout.addWidget(duration_label)
        
        # Play button
        play_btn = QPushButton("▶")
        play_btn.setFixedSize(30, 30)
        play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        play_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: {COLORS['text_primary']};
                border-radius: 15px;
                border: none;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gradient_start']};
            }}
        """)
        play_btn.clicked.connect(lambda: self._on_favorite_action(sound_data["id"], "play"))
        layout.addWidget(play_btn)
        
        # Menu button (3 dots)
        menu_btn = QPushButton("⋮")
        menu_btn.setFixedSize(30, 30)
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border-radius: 12px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
        """)
        menu_btn.clicked.connect(lambda: self._show_favorite_menu(sound_data["id"], menu_btn))
        layout.addWidget(menu_btn)
        
        # Add to list
        self.favorites_list_layout.insertWidget(self.favorites_list_layout.count() - 1, item)
        
    def _show_favorite_menu(self, sound_id, button):
        """Show context menu for favorite sound"""
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {COLORS['bg_elevated']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 16px;
                color: {COLORS['text_primary']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['card_hover']};
                color: {COLORS['accent']};
            }}
        """)
        
        edit_action = QAction("Edit", menu)
        edit_action.triggered.connect(lambda: self._on_favorite_action(sound_id, "edit"))
        menu.addAction(edit_action)
        
        remove_action = QAction("Remove from Favorites", menu)
        remove_action.triggered.connect(lambda: self._on_favorite_action(sound_id, "unfavorite"))
        menu.addAction(remove_action)
        
        delete_action = QAction("Delete", menu)
        delete_action.triggered.connect(lambda: self._on_favorite_action(sound_id, "delete"))
        menu.addAction(delete_action)
        
        menu.exec(button.mapToGlobal(QPoint(0, button.height())))
    
    def _toggle_view(self, is_grid_view):
        """Toggle between grid and list view"""
        self.view_stack.setCurrentIndex(0 if is_grid_view else 1)
    
    def _change_size(self, size):
        """Change the size of favorite sound cards in grid view"""
        print(f"Changed favorites size to: {size}")
        self.current_size = size
        
        sizes = {
            "small": (160, 140),
            "medium": (200, 180),
            "large": (240, 220)
        }
        
        if size in sizes:
            # Adjust size of all favorite sound cards
            for i in range(self.favorites_grid.count()):
                item = self.favorites_grid.itemAt(i)
                if item and item.widget():
                    card = item.widget()
                    card.setFixedSize(*sizes[size])
            
            # Adjust columns in grid based on size to prevent overflow
            columns = 4  # Default for small and medium
            if size == "large":
                columns = 3
            
            # Rearrange items in grid with new column count
            widgets = []
            while self.favorites_grid.count():
                item = self.favorites_grid.takeAt(0)
                if item.widget():
                    widgets.append(item.widget())
            
            for i, widget in enumerate(widgets):
                if i < len(widgets):  # Safety check
                    row = i // columns
                    col = i % columns
                    self.favorites_grid.addWidget(widget, row, col)
    
    def _sort_favorites(self, sort_by):
        """Sort favorite sounds according to criteria"""
        print(f"Sorting favorites by: {sort_by}")
        self.current_sort = sort_by
        
        # Get a copy of favorite sound data to sort
        sorted_favorites = self.favorite_sounds.copy()
        
        if sort_by == "name":
            sorted_favorites.sort(key=lambda s: s["title"].lower())
        elif sort_by == "duration":
            sorted_favorites.sort(key=lambda s: s["duration"])
        # Default is "recent" (original order)
        
        # Update the favorite_sounds with the sorted version
        self.favorite_sounds = sorted_favorites
        
        # Clear current grid
        while self.favorites_grid.count():
            item = self.favorites_grid.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
                
        # Clear current list view (except the stretch at the end)
        for i in range(self.favorites_list_layout.count() - 1, -1, -1):
            item = self.favorites_list_layout.itemAt(i)
            if item and not isinstance(item, QSpacerItem):
                widget = item.widget()
                if widget:
                    self.favorites_list_layout.removeWidget(widget)
                    widget.deleteLater()
        
        # Recreate favorite sound cards and list items in sorted order
        for i, sound in enumerate(sorted_favorites):
            self._create_favorite_card(i, sound)
            self._create_favorite_list_item(sound)
    
    def _on_favorite_action(self, sound_id, action):
        """Handle favorite sound actions"""
        if self.sound_manager:
            if action == "play":
                self.sound_manager.play_sound(sound_id)
            elif action == "edit":
                # Handle edit action
                pass
            elif action == "delete":
                # Remove the sound from favorites
                if self.sound_manager.remove_from_favorites(sound_id):
                    # Refresh the view
                    self.update_favorites()
        else:
            print(f"Favorite sound {sound_id}: {action}")
            
    def update_favorites(self):
        """Update the favorites display with current data from sound manager"""
        if not self.sound_manager:
            return
            
        # Get all favorites from the sound manager
        self.favorite_sounds = self.sound_manager.get_favorites()
        
        # Clear current grid
        while self.favorites_grid.count():
            item = self.favorites_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Clear current list view (except the stretch at the end)
        for i in range(self.favorites_list_layout.count() - 1, -1, -1):
            item = self.favorites_list_layout.itemAt(i)
            if item and not isinstance(item, QSpacerItem):
                widget = item.widget()
                if widget:
                    self.favorites_list_layout.removeWidget(widget)
                    widget.deleteLater()
        
        # Create favorite sound cards for grid view and list items for list view
        for i, sound in enumerate(self.favorite_sounds):
            self._create_favorite_card(i, sound)
            self._create_favorite_list_item(sound)
            
    def set_sound_manager(self, sound_manager):
        """Set the sound manager for this view"""
        self.sound_manager = sound_manager
        
    def _update_sound(self, sound_id, sound_data):
        """Update a specific sound in the favorites view"""
        # Check if this sound is in our favorites list
        for i, sound in enumerate(self.favorite_sounds):
            if sound.get('id') == sound_id:
                # Update the sound data
                self.favorite_sounds[i] = sound_data.copy()
                self.favorite_sounds[i]['id'] = sound_id
                # Refresh the display
                self.update_favorites()
                break

class FolderView(QFrame):
    """Folder view for organizing sounds"""
    folder_selected = pyqtSignal(str)  # Emits folder_id when selected
    folder_clicked = pyqtSignal(str, str)  # Emits folder_id and action
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("folder_view")
        
        # Store folder data
        self.folders = {}
        
        # Current folder tracking
        self.current_folder_id = None
        self.parent_folders = {}  # Maps folder_id to parent_id
        
        # Default folder attributes
        self.folder_name = "Folders"
        self.sound_count = 0
        self.folder_id = "root"
        
        # Sound manager will be set by MainWindow
        self.sound_manager = None
        
        # Setup UI
        self._setup_ui()
        
        # Populate with sample data
        self._populate_sample_folders()
        
    def set_sound_manager(self, sound_manager):
        """Set the sound manager for this view"""
        self.sound_manager = sound_manager
        
    def _setup_ui(self):
        self.setStyleSheet(f"""
            FolderView {{
                background-color: {COLORS['bg_primary']};
                border: none;
            }}
            QFrame#folder_item:hover, QFrame#folder_card:hover {{
                background-color: {COLORS['folder_hover']};
                border: 1px solid {COLORS['accent']};
            }}
            QFrame#folder_item, QFrame#folder_card {{
                background-color: {COLORS['folder_bg']};
                border-radius: 8px;
                border: 1px solid {COLORS['divider']};
            }}
            QLabel, QPushButton {{
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header with title and add folder button
        header = QHBoxLayout()
        
        title = QLabel("Folders")
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 24px;
            font-weight: bold;
        """)
        header.addWidget(title)
        
        header.addStretch()
        
        # Search bar
        search_bar = SearchBar()
        header.addWidget(search_bar)
        
        # Add folder button
        add_folder_btn = ModernButton("+ Add Folder", is_primary=True)
        header.addWidget(add_folder_btn)
        
        layout.addLayout(header)
        
        # View controls
        controls_layout = QHBoxLayout()
        self.view_controls = ViewControls()
        self.view_controls.sort_combo.clear()
        self.view_controls.sort_combo.addItems(["Default", "Name", "Sound Count"])
        self.view_controls.grid_view_toggled.connect(self._toggle_view)
        self.view_controls.size_changed.connect(self._change_size)
        self.view_controls.sort_changed.connect(self._sort_folders)
        controls_layout.addWidget(self.view_controls)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Create stacked widget for different views
        self.view_stack = QStackedWidget()
        
        # Grid view for folders
        self.grid_view = self._create_grid_view()
        self.view_stack.addWidget(self.grid_view)
        
        # List view for folders
        self.list_view = self._create_list_view()
        self.view_stack.addWidget(self.list_view)
        
        # Add the stacked widget to the main layout
        layout.addWidget(self.view_stack)
        
        # Set default view
        self.view_stack.setCurrentIndex(0)  # Start with grid view
        
    def _create_grid_view(self):
        """Create the grid view for folders"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
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
        
        self.content_widget = QWidget()
        self.folder_grid = QGridLayout(self.content_widget)
        self.folder_grid.setContentsMargins(0, 0, 0, 0)
        self.folder_grid.setSpacing(16)
        
        scroll_area.setWidget(self.content_widget)
        return scroll_area
        
    def _create_list_view(self):
        """Create the list view for folders"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
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
        
        list_container = QWidget()
        self.folder_list_layout = QVBoxLayout(list_container)
        self.folder_list_layout.setContentsMargins(0, 0, 0, 0)
        self.folder_list_layout.setSpacing(8)
        self.folder_list_layout.addStretch()
        
        scroll_area.setWidget(list_container)
        return scroll_area
    
    def _populate_sample_folders(self):
        """Add sample folders for visualization"""
        # Just visual samples for UI demonstration
        sample_folders = [
            {"id": "folder1", "name": "Sound Effects", "count": 12},
            {"id": "folder2", "name": "Music Clips", "count": 8},
            {"id": "folder3", "name": "Voice Lines", "count": 15},
            {"id": "folder4", "name": "Notifications", "count": 6},
            {"id": "folder5", "name": "Custom Sounds", "count": 9}
        ]
        
        # Store folder data and create folder cards
        for i, folder in enumerate(sample_folders):
            self.folders[folder["id"]] = folder
            self._create_folder_card(i, folder)
            self._create_folder_list_item(folder)
            
    def _create_folder_card(self, index, folder_data):
        """Create a folder card widget and add it to the grid"""
        row = index // 4  # 4 folders per row
        col = index % 4
        
        # Create the folder card
        card = QFrame()
        card.setFixedSize(200, 180)
        card.setObjectName(f"folder_card")  # Set common object name for styling
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(COLORS['shadow']))
        shadow.setOffset(0, 2)
        card.setGraphicsEffect(shadow)
        
        # Card layout
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)
        
        # Top section with folder icon and menu
        top_section = QHBoxLayout()
        
        # Folder icon
        folder_icon = QLabel("📁")
        folder_icon.setStyleSheet(f"""
            font-size: 28px;
            color: {COLORS['folder_icon']};
        """)
        top_section.addWidget(folder_icon)
        
        top_section.addStretch()
        
        # Menu button (3 vertical dots)
        menu_button = QPushButton("⋮")
        menu_button.setFixedSize(24, 24)
        menu_button.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border-radius: 12px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
        """)
        # Connect menu button to show context menu
        menu_button.clicked.connect(lambda: self._show_context_menu(folder_data['id'], menu_button))
        top_section.addWidget(menu_button)
        
        card_layout.addLayout(top_section)
        
        # Folder name
        name_label = QLabel(folder_data['name'])
        name_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 16px;
            font-weight: bold;
        """)
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(name_label)
        
        card_layout.addStretch()
        
        # Sound count
        count_label = QLabel(f"{folder_data['count']} sounds")
        count_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 13px;
        """)
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(count_label)
        
        # Connect card click to emit folder selected signal
        card.mousePressEvent = lambda event: self._on_folder_click(event, folder_data['id'], menu_button)
        
        # Add to grid
        self.folder_grid.addWidget(card, row, col)
        
    def _create_folder_list_item(self, folder_data):
        """Create a list item for a folder in list view"""
        item = QFrame()
        item.setObjectName("folder_item")  # Set object name for styling
        item.setCursor(Qt.CursorShape.PointingHandCursor)
        item.setFixedHeight(60)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(16, 8, 16, 8)
        
        # Folder icon
        folder_icon = QLabel("📁")
        folder_icon.setStyleSheet(f"""
            font-size: 20px;
            color: {COLORS['folder_icon']};
        """)
        layout.addWidget(folder_icon)
        
        # Folder name with bold formatting
        name_label = QLabel(folder_data['name'])
        name_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: bold;
            margin-left: 8px;
        """)
        layout.addWidget(name_label, 1)  # 1 is the stretch factor
        
        # Sound count
        count_label = QLabel(f"{folder_data['count']} sounds")
        count_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 12px;
            margin-right: 12px;
        """)
        layout.addWidget(count_label)
        
        # Menu button (3 dots)
        menu_btn = QPushButton("⋮")
        menu_btn.setFixedSize(24, 24)
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border-radius: 12px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
        """)
        menu_btn.clicked.connect(lambda: self._show_context_menu(folder_data['id'], menu_btn))
        layout.addWidget(menu_btn)
        
        # Connect click to emit folder signals
        item.mousePressEvent = lambda event: self._on_folder_click(event, folder_data['id'], menu_btn)
        
        # Add to list
        self.folder_list_layout.insertWidget(self.folder_list_layout.count() - 1, item)  # Insert before the stretch
    
    def _on_folder_click(self, event, folder_id, menu_button):
        """Handle folder click"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Ignore clicks on the menu button
            if not menu_button.geometry().contains(event.pos()):
                self.folder_clicked.emit(folder_id, "open")
                self.folder_selected.emit(folder_id)
        # Call parent class implementation
        QFrame.mousePressEvent(self, event)
    
    def _toggle_view(self, is_grid_view):
        """Toggle between grid and list view"""
        self.view_stack.setCurrentIndex(0 if is_grid_view else 1)
    
    def _change_size(self, size):
        """Change the size of folder cards in grid view"""
        self.current_size = size
        
        sizes = {
            "small": (160, 140),
            "medium": (200, 180),
            "large": (240, 220)
        }
        
        if size in sizes:
            # Adjust size of all folder cards
            for i in range(self.folder_grid.count()):
                item = self.folder_grid.itemAt(i)
                if item and item.widget():
                    card = item.widget()
                    card.setFixedSize(*sizes[size])
            
            # Adjust columns in grid based on size to prevent overflow
            columns = 4  # Default for small and medium
            if size == "large":
                columns = 3
            
            # Rearrange items in grid with new column count
            widgets = []
            while self.folder_grid.count():
                item = self.folder_grid.takeAt(0)
                if item.widget():
                    widgets.append(item.widget())
            
            for i, widget in enumerate(widgets):
                row = i // columns
                col = i % columns
                self.folder_grid.addWidget(widget, row, col)
    
    def _sort_folders(self, sort_by):
        """Sort folders according to criteria"""
        print(f"Sorting folders by: {sort_by}")
        
        # Get folder data and sort it
        folder_list = list(self.folders.values())
        
        if sort_by == "name":
            folder_list.sort(key=lambda f: f["name"])
        elif sort_by == "sound_count":
            folder_list.sort(key=lambda f: f["count"], reverse=True)
        # Default is to sort by ID (original order)
        
        # Clear current grid
        while self.folder_grid.count():
            item = self.folder_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Clear current list view (except the stretch at the end)
        for i in range(self.folder_list_layout.count() - 1, -1, -1):
            item = self.folder_list_layout.itemAt(i)
            if item and not isinstance(item, QSpacerItem):
                widget = item.widget()
                if widget:
                    self.folder_list_layout.removeWidget(widget)
                    widget.deleteLater()
        
        # Recreate folder cards and list items in sorted order
        for i, folder in enumerate(folder_list):
            self._create_folder_card(i, folder)
            self._create_folder_list_item(folder)

    def _show_context_menu(self, folder_id, menu_button):
        """Show context menu with actions for a specific folder"""
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {COLORS['bg_elevated']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 16px;
                color: {COLORS['text_primary']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['card_hover']};
                color: {COLORS['accent']};
            }}
        """)
        
        edit_action = QAction("Edit", menu)
        edit_action.triggered.connect(lambda: self.folder_clicked.emit(folder_id, "edit"))
        menu.addAction(edit_action)
        
        delete_action = QAction("Delete", menu)
        delete_action.triggered.connect(lambda: self.folder_clicked.emit(folder_id, "delete"))
        menu.addAction(delete_action)
        
        menu.exec(self.mapToGlobal(menu_button.pos() + QPoint(0, menu_button.height())))

class FolderContentView(QFrame):
    """View for displaying sounds in a selected folder"""
    def __init__(self, folder_name, parent=None):
        super().__init__(parent)
        self.folder_name = folder_name
        self.current_view = "grid"  # Default to grid view
        self.current_size = "medium"  # Default size
        self.sounds = []  # Initialize sounds list
        self.sound_manager = None  # Will be set by MainWindow
        self._setup_ui()
        
    def set_sound_manager(self, sound_manager):
        """Set the sound manager for this view"""
        self.sound_manager = sound_manager
        
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
        add_sound_btn.clicked.connect(self._on_add_sound_clicked)
        header.addWidget(add_sound_btn)
        
        layout.addLayout(header)
        
        # View controls
        controls_layout = QHBoxLayout()
        self.view_controls = ViewControls()
        self.view_controls.grid_view_toggled.connect(self._toggle_view)
        self.view_controls.size_changed.connect(self._change_size)
        self.view_controls.sort_changed.connect(self._sort_sounds)
        controls_layout.addWidget(self.view_controls)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Create stacked widget for different views
        self.view_stack = QStackedWidget()
        
        # Grid view (card view)
        self.grid_view = self._create_grid_view()
        self.view_stack.addWidget(self.grid_view)
        
        # List view
        self.list_view = self._create_list_view()
        self.view_stack.addWidget(self.list_view)
        
        layout.addWidget(self.view_stack)
        
        # Set default view
        self._toggle_view(True)  # Start with grid view
        
    def _create_grid_view(self):
        """Create the grid view with cards"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
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
        self.grid_layout = QGridLayout(content_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(16)
        
        # Sample sound cards for this folder
        sample_sounds = [
            {"id": "sound1", "title": "Folder Sound 1", "category": 1, "favorite": True},
            {"id": "sound2", "title": "Folder Sound 2", "category": 2, "favorite": False},
            {"id": "sound3", "title": "Folder Sound 3", "category": 3, "favorite": False},
            {"id": "sound4", "title": "Folder Sound 4", "category": 4, "favorite": True},
            {"id": "sound5", "title": "Folder Sound 5", "category": 1, "favorite": False},
            {"id": "sound6", "title": "Folder Sound 6", "category": 2, "favorite": False},
            {"id": "sound7", "title": "Folder Sound 7", "category": 3, "favorite": False}
        ]
        
        # Create a proper grid layout
        for i, sound in enumerate(sample_sounds):
            row = i // 4  # 4 cards per row
            col = i % 4
            card = SoundCard(
                sound["title"], 
                sound["category"], 
                sound["id"],
                sound["favorite"]
            )
            card.sound_clicked.connect(self._on_sound_action)
            self.grid_layout.addWidget(card, row, col)
        
        scroll_area.setWidget(content_widget)
        return scroll_area
        
    def _create_list_view(self):
        """Create the list view"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
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
        list_layout = QVBoxLayout(content_widget)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(8)
        
        # Sample sound items for this folder
        sample_sounds = [
            {"id": "sound1", "title": "Folder Sound 1", "category": 1, "favorite": True},
            {"id": "sound2", "title": "Folder Sound 2", "category": 2, "favorite": False},
            {"id": "sound3", "title": "Folder Sound 3", "category": 3, "favorite": False},
            {"id": "sound4", "title": "Folder Sound 4", "category": 4, "favorite": True},
            {"id": "sound5", "title": "Folder Sound 5", "category": 1, "favorite": False},
            {"id": "sound6", "title": "Folder Sound 6", "category": 2, "favorite": False},
            {"id": "sound7", "title": "Folder Sound 7", "category": 3, "favorite": False}
        ]
        
        # Create list items
        for sound in sample_sounds:
            item = self._create_sound_list_item(
                sound["id"],
                sound["title"], 
                sound["category"],
                sound["favorite"]
            )
            list_layout.addWidget(item)
        
        list_layout.addStretch()
        scroll_area.setWidget(content_widget)
        return scroll_area
    
    def _create_sound_list_item(self, sound_id, title, category, is_favorite):
        """Create a list item for a sound in list view"""
        item = QFrame()
        item.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_elevated']};
                border-radius: 6px;
                border: 1px solid {COLORS['divider']};
            }}
            QFrame:hover {{
                background-color: {COLORS['card_hover']};
            }}
        """)
        item.setCursor(Qt.CursorShape.PointingHandCursor)
        item.setFixedHeight(60)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # Category color indicator
        category_color = COLORS.get(f'category_{category}', COLORS['accent'])
        color_indicator = QFrame()
        color_indicator.setFixedSize(4, 20)
        color_indicator.setStyleSheet(f"""
            background-color: {category_color};
            border-radius: 2px;
        """)
        layout.addWidget(color_indicator)
        
        # Sound icon
        icon_label = QLabel("🔊")
        icon_label.setStyleSheet(f"""
            font-size: 18px;
            color: {category_color};
            margin-left: 4px;
        """)
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: bold;
            margin-left: 8px;
        """)
        layout.addWidget(title_label, 1)
        
        # Duration
        duration_label = QLabel("0:30")
        duration_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 12px;
        """)
        layout.addWidget(duration_label)
        
        # Favorite button
        fav_btn = QPushButton("★" if is_favorite else "☆")
        fav_btn.setFixedSize(24, 24)
        fav_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        fav_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {('gold' if is_favorite else COLORS['text_secondary'])};
                border: none;
                font-size: 16px;
            }}
            QPushButton:hover {{
                color: gold;
            }}
        """)
        fav_btn.clicked.connect(lambda: self._on_sound_action(sound_id, "favorite"))
        layout.addWidget(fav_btn)
        
        # Play button
        play_btn = QPushButton("▶")
        play_btn.setFixedSize(30, 30)
        play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        play_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: {COLORS['text_primary']};
                border-radius: 15px;
                border: none;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gradient_start']};
            }}
        """)
        play_btn.clicked.connect(lambda: self._on_sound_action(sound_id, "play"))
        layout.addWidget(play_btn)
        
        # Menu button (3 dots)
        menu_btn = QPushButton("⋮")
        menu_btn.setFixedSize(30, 30)
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border-radius: 12px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
        """)
        menu_btn.clicked.connect(lambda: self._show_sound_menu(sound_id, menu_btn))
        layout.addWidget(menu_btn)
        
        return item
    
    def _show_sound_menu(self, sound_id, button):
        """Show context menu for sound"""
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {COLORS['bg_elevated']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 16px;
                color: {COLORS['text_primary']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['card_hover']};
                color: {COLORS['accent']};
            }}
        """)
        
        edit_action = QAction("Edit", menu)
        edit_action.triggered.connect(lambda: self._on_sound_action(sound_id, "edit"))
        menu.addAction(edit_action)
        
        delete_action = QAction("Delete", menu)
        delete_action.triggered.connect(lambda: self._on_sound_action(sound_id, "delete"))
        menu.addAction(delete_action)
        
        menu.exec(button.mapToGlobal(QPoint(0, button.height())))
    
    def _toggle_view(self, is_grid_view):
        """Toggle between grid and list view"""
        self.current_view = "grid" if is_grid_view else "list"
        self.view_stack.setCurrentIndex(0 if is_grid_view else 1)
    
    def _change_size(self, size):
        """Change the size of cards in grid view"""
        self.current_size = size
        # TODO: Implement size adjustment
    
    def _sort_sounds(self, sort_by):
        """Sort sounds according to criteria"""
        print(f"Sorting folder content sounds by: {sort_by}")
        self.current_sort = sort_by
        
        # Get a copy of sound data to sort
        sorted_sounds = self.sounds.copy() if hasattr(self, 'sounds') else []
        
        if sort_by == "name":
            sorted_sounds.sort(key=lambda s: s["title"].lower())
        elif sort_by == "duration":
            sorted_sounds.sort(key=lambda s: s["duration"])
        # Default is "recent" (original order)
        
        # Update the sounds list with the sorted version
        self.sounds = sorted_sounds
        
        # Clear current grid
        while self.sound_grid.count():
            item = self.sound_grid.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
                
        # Clear current list view (except the stretch at the end)
        for i in range(self.sound_list_layout.count() - 1, -1, -1):
            item = self.sound_list_layout.itemAt(i)
            if item and not isinstance(item, QSpacerItem):
                widget = item.widget()
                if widget:
                    self.sound_list_layout.removeWidget(widget)
                    widget.deleteLater()
        
        # Recreate sound cards and list items in sorted order
        for i, sound in enumerate(sorted_sounds):
            self._create_sound_card(i, sound)
            self._create_sound_list_item(sound["id"], sound["title"], sound["category"], sound.get("is_favorite", False))

    def _populate_sample_sounds(self):
        """Add sample sounds to the folder for visualization"""
        # Sample sounds in this folder
        sample_sounds = [
            {"id": "f1s1", "title": "Folder Sound 1", "category": 1, "duration": "0:18", "is_favorite": False},
            {"id": "f1s2", "title": "Folder Sound 2", "category": 2, "duration": "0:12", "is_favorite": True},
            {"id": "f1s3", "title": "Folder Sound 3", "category": 3, "duration": "0:25", "is_favorite": False},
            {"id": "f1s4", "title": "Folder Sound 4", "category": 1, "duration": "0:08", "is_favorite": False},
            {"id": "f1s5", "title": "Folder Sound 5", "category": 4, "duration": "0:22", "is_favorite": True}
        ]
        
        # Store sound data
        self.sounds = sample_sounds
        
        # Create sound cards for grid view and list items for list view
        for i, sound in enumerate(self.sounds):
            self._create_sound_card(i, sound)
            self._create_sound_list_item(sound["id"], sound["title"], sound["category"], sound.get("is_favorite", False))

    def _create_sound_card(self, index, sound_data):
        """Create a sound card widget and add it to the grid"""
        columns = 4  # Default column count
        if self.current_size == "large":
            columns = 3
        
        row = index // columns
        col = index % columns
        
        # Create the sound card
        card = SoundCard(
            sound_data["title"], 
            sound_data["category"], 
            sound_data["id"], 
            sound_data.get("is_favorite", False)
        )
        card.setObjectName("sound_card")  # Set object name for styling
        card.sound_clicked.connect(self._on_sound_action)
        
        # Apply current size
        sizes = {
            "small": (160, 140),
            "medium": (200, 180),
            "large": (240, 220)
        }
        if self.current_size in sizes:
            card.setFixedSize(*sizes[self.current_size])
        
        # Add to grid
        self.sound_grid.addWidget(card, row, col)

    def _on_sound_action(self, sound_id, action):
        """Handle sound actions"""
        if not self.sound_manager:
            print(f"Sound {sound_id} action: {action} - No sound manager available")
            return
            
        if action == "play":
            # Play the sound
            self.sound_manager.play_sound(sound_id)
        elif action == "favorite":
            # Toggle favorite status
            if self.sound_manager.is_favorite(sound_id):
                self.sound_manager.remove_from_favorites(sound_id)
            else:
                self.sound_manager.add_to_favorites(sound_id)
            # Update UI
            self._refresh_sounds()
        elif action == "delete":
            # Remove the sound
            self.sound_manager.remove_sound(sound_id)
            # Update UI
            self._refresh_sounds()
        elif action == "edit":
            # TODO: Implement sound editing
            pass
        else:
            print(f"Sound {sound_id} action: {action} - Not implemented")

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SoundWave")
        self.setMinimumSize(1200, 800)
        
        # Initialize sound manager
        from managers.sound_manager import SoundManager
        self.sound_manager = SoundManager()
        
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
        
        # Connect sound manager signals
        self._connect_sound_manager_signals()

    def _init_ui(self):
        """Initialize UI components"""
        self._create_header()
        self._create_content()
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
        header_layout.setContentsMargins(24, 16, 24, 16)
        
        # Top bar with title and settings
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
        
        top_bar.addStretch()
        
        # Settings button only
        settings_btn = ModernButton("⚙ Settings")
        top_bar.addWidget(settings_btn)
        
        # Category tabs
        tabs_layout = QHBoxLayout()
        tabs_layout.setSpacing(4)
        tabs_layout.setContentsMargins(0, 16, 0, 0)
        
        categories = ["All Sounds", "Favourites", "Folders"]
        self.category_buttons = []
        
        for i, category in enumerate(categories):
            tab = ModernButton(category)
            tab.setCheckable(True)
            tab.setChecked(i == 0)  # Check the first one by default
            
            # Set onclick to update which tab is checked
            tab.clicked.connect(lambda checked, btn=tab: self._handle_tab_click(btn))
            
            self.category_buttons.append(tab)
            tabs_layout.addWidget(tab)
        
        tabs_layout.addStretch()
        
        # Remove the view controls from here as they'll be in each view

        header_layout.addLayout(top_bar)
        header_layout.addLayout(tabs_layout)
        
        self.content_layout.addWidget(header)
    
    def _handle_tab_click(self, clicked_button):
        """Handle tab button clicks to ensure only one is checked"""
        for button in self.category_buttons:
            if button != clicked_button:
                button.setChecked(False)
            else:
                button.setChecked(True)
    
    def _create_content(self):
        """Create the main content area"""
        # Create a stacked widget to hold different views
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"""
            background-color: {COLORS['bg_primary']};
        """)
        
        # All Sounds view
        self.all_sounds_view = SoundGridView()
        self.content_stack.addWidget(self.all_sounds_view)
        
        # Favorites view
        self.favorites_view = FavouritesView()
        self.content_stack.addWidget(self.favorites_view)
        
        # Folders view
        self.folders_view = FolderView()
        self.content_stack.addWidget(self.folders_view)
        
        # Add the stacked widget to the main layout
        self.content_layout.addWidget(self.content_stack)
        
        # Connect tab buttons to switch views
        self.category_buttons[0].clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        self.category_buttons[1].clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        self.category_buttons[2].clicked.connect(lambda: self.content_stack.setCurrentIndex(2))
    
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
        self.status_label = QLabel("4 sounds loaded")
        status_bar.addWidget(self.status_label)
        status_bar.addPermanentWidget(QLabel("Version 0.1.0"))
    
    def _connect_sound_manager_signals(self):
        """Connect sound manager signals to update UI"""
        # Connect signals from sound manager to update UI
        self.sound_manager.favorite_added.connect(self._on_favorite_added)
        self.sound_manager.favorite_removed.connect(self._on_favorite_removed)
        self.sound_manager.sound_updated.connect(self._on_sound_updated)
        self.sound_manager.sound_played.connect(self._on_sound_played)
        
        # Set sound manager for views
        self.favorites_view.set_sound_manager(self.sound_manager)
        self.all_sounds_view.set_sound_manager(self.sound_manager)
        self.folders_view.set_sound_manager(self.sound_manager)
    
    def _on_favorite_added(self, sound_id):
        """Handle when a sound is added to favorites"""
        # Update favorites view
        self.favorites_view.update_favorites()
        
        # Update status bar
        self.status_bar_message(f"Sound added to favorites")
    
    def _on_favorite_removed(self, sound_id):
        """Handle when a sound is removed from favorites"""
        # Update favorites view
        self.favorites_view.update_favorites()
        
        # Update status bar
        self.status_bar_message(f"Sound removed from favorites")
    
    def _on_sound_updated(self, sound_id, sound_data):
        """Handle when a sound is updated"""
        # Update all views
        self.all_sounds_view._update_sound(sound_id, sound_data)
        self.favorites_view._update_sound(sound_id, sound_data)
        
        # Update status bar
        self.status_bar_message(f"Sound updated: {sound_data.get('title', 'Unknown')}")
    
    def _on_sound_played(self, sound_id):
        """Handle when a sound is played"""
        # Update status bar
        sound_data = self.sound_manager.get_sound(sound_id)
        if sound_data:
            self.status_bar_message(f"Playing: {sound_data.get('title', 'Unknown')}")
    
    def status_bar_message(self, message, timeout=3000):
        """Show a message in the status bar"""
        self.statusBar().showMessage(message, timeout)