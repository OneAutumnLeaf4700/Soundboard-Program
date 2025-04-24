"""
Main Window Implementation with Enhanced Modern Design
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStatusBar, QMenuBar, QMenu, QLabel,
    QPushButton, QScrollArea, QFrame, QSizePolicy,
    QStackedWidget, QGraphicsDropShadowEffect, QSlider,
    QLineEdit, QComboBox, QCheckBox, QTreeWidget, QTreeWidgetItem,
    QGridLayout, QButtonGroup
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QPoint
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
        
        # Top section with category, menu and preview
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
        """Toggle favorite status"""
        self.is_favorite = not self.is_favorite
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
        self.sort_combo.addItems(["Recent", "Name", "Duration"])
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
        sorts = ["recent", "name", "duration"]
        if 0 <= index < len(sorts):
            # Emit signal with the selected sort option
            self.sort_changed.emit(sorts[index])

class SoundGridView(QFrame):
    """Main sound grid view"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self):
        self.setStyleSheet(f"""
            SoundGridView {{
                background-color: {COLORS['bg_primary']};
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
        header.addWidget(add_sound_btn)
        
        layout.addLayout(header)
        
        # View controls
        controls_layout = QHBoxLayout()
        view_controls = ViewControls()
        controls_layout.addWidget(view_controls)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Content (sound grid)
        content_area = QScrollArea()
        content_area.setWidgetResizable(True)
        content_area.setFrameShape(QFrame.Shape.NoFrame)
        content_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        content_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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
        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)
        
        # Many sample sounds to demonstrate scrolling
        sample_sounds = [
            ("Epic Bass Drop", 1),
            ("Guitar Riff", 2),
            ("Voice Effect", 3),
            ("Custom Sound", 4),
            ("Drum Roll", 1),
            ("Synth Wave", 2),
            ("Record Scratch", 3),
            ("Crowd Cheer", 4),
            ("Glass Breaking", 1),
            ("Air Horn", 2),
            ("Applause", 3),
            ("Door Slam", 4)
        ]
        
        # Create a proper grid layout
        for i, (title, category) in enumerate(sample_sounds):
            row = i // 4  # 4 cards per row
            col = i % 4
            card = SoundCard(title, category)
            content_layout.addWidget(card, row, col)
        
        content_area.setWidget(content_widget)
        layout.addWidget(content_area)

class FavouritesView(QFrame):
    """View for favourites sounds"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self):
        self.setStyleSheet(f"""
            FavouritesView {{
                background-color: {COLORS['bg_primary']};
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
        header.addWidget(add_sound_btn)
        
        layout.addLayout(header)
        
        # View controls
        controls_layout = QHBoxLayout()
        view_controls = ViewControls()
        controls_layout.addWidget(view_controls)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Content (sound grid)
        content_area = QScrollArea()
        content_area.setWidgetResizable(True)
        content_area.setFrameShape(QFrame.Shape.NoFrame)
        content_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        content_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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
        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)
        
        # Sample favorites
        sample_sounds = [
            ("Favorite Sound 1", 1),
            ("Favorite Sound 2", 2),
            ("Favorite Sound 3", 3),
            ("Favorite Sound 4", 4),
            ("Favorite Sound 5", 1),
            ("Favorite Sound 6", 2)
        ]
        
        # Create a proper grid layout
        for i, (title, category) in enumerate(sample_sounds):
            row = i // 4  # 4 cards per row
            col = i % 4
            card = SoundCard(title, category)
            content_layout.addWidget(card, row, col)
        
        content_area.setWidget(content_widget)
        layout.addWidget(content_area)

class FolderView(QFrame):
    """Folder view for organizing sounds"""
    folder_selected = pyqtSignal(str)  # Emits folder_id when selected
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_view = "grid"  # Default view
        self.current_size = "medium"  # Default size
        self.folders = {}  # Dictionary to store folder data
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
        
        # View controls
        controls_layout = QHBoxLayout()
        self.view_controls = ViewControls()
        self.view_controls.grid_view_toggled.connect(self._toggle_view)
        self.view_controls.size_changed.connect(self._change_size)
        self.view_controls.sort_changed.connect(self._sort_folders)
        controls_layout.addWidget(self.view_controls)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Stacked widget to switch between list and grid views
        self.view_stack = QStackedWidget()
        
        # List view
        self.list_container = QScrollArea()
        self.list_container.setWidgetResizable(True)
        self.list_container.setFrameShape(QFrame.Shape.NoFrame)
        self.list_container.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.list_container.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list_container.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                width: 8px;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background: #404040;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        self.list_content = QWidget()
        self.list_layout = QVBoxLayout(self.list_content)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)
        
        self.list_container.setWidget(self.list_content)
        
        # Grid view
        self.grid_container = QScrollArea()
        self.grid_container.setWidgetResizable(True)
        self.grid_container.setFrameShape(QFrame.Shape.NoFrame)
        self.grid_container.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.grid_container.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.grid_container.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                width: 8px;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background: #404040;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        self.grid_content = QWidget()
        self.grid_layout = QGridLayout(self.grid_content)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(16)
        
        self.grid_container.setWidget(self.grid_content)
        
        # Add views to stack
        self.view_stack.addWidget(self.grid_container)  # Index 0 = Grid view
        self.view_stack.addWidget(self.list_container)  # Index 1 = List view
        
        layout.addWidget(self.view_stack)
    
    def _populate_sample_folders(self):
        """Add sample folders for visualization"""
        # Clear existing folders
        self._clear_views()
        
        # Sample folders
        sample_folders = [
            {"id": "folder1", "name": "Sound Effects", "count": 12},
            {"id": "folder2", "name": "Meme Sounds", "count": 8},
            {"id": "folder3", "name": "Music Clips", "count": 5},
            {"id": "folder4", "name": "Custom Recordings", "count": 3},
            {"id": "folder5", "name": "Voice Mods", "count": 7},
            {"id": "folder6", "name": "Animal Sounds", "count": 9},
            {"id": "folder7", "name": "Instruments", "count": 15},
            {"id": "folder8", "name": "Nature Sounds", "count": 11},
            {"id": "folder9", "name": "Game Sounds", "count": 14},
            {"id": "folder10", "name": "Movie Quotes", "count": 6},
            {"id": "folder11", "name": "Cartoon Effects", "count": 8}
        ]
        
        # Add folders to both views
        for folder in sample_folders:
            self.add_folder(folder["id"], folder["name"], folder["count"])
        
        # Add stretch to list view to push items to top
        self.list_layout.addStretch()
    
    def _clear_views(self):
        """Clear both list and grid views"""
        # Clear list view
        for i in reversed(range(self.list_layout.count())):
            item = self.list_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        # Clear grid view
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        # Clear folders dictionary
        self.folders = {}
    
    def add_folder(self, folder_id, name, sound_count=0):
        """Add a folder to both views"""
        # Store folder data
        self.folders[folder_id] = {
            "name": name,
            "count": sound_count
        }
        
        # Create list view item
        list_item = self._create_folder_list_item(name, sound_count, folder_id)
        self.list_layout.addWidget(list_item)
        
        # Create grid view item
        grid_item = self._create_folder_card(name, folder_id, sound_count)
        
        # Calculate position in grid (4 items per row)
        folder_index = len(self.folders) - 1
        row = folder_index // 4
        col = folder_index % 4
        
        self.grid_layout.addWidget(grid_item, row, col)
    
    def _create_folder_list_item(self, name, sound_count, folder_id):
        """Create a folder item widget for list view"""
        folder_frame = QFrame()
        folder_frame.setObjectName(f"folder_list_{folder_id}")
        folder_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['folder_bg']};
                border-radius: 8px;
            }}
            QFrame:hover {{
                background-color: {COLORS['folder_hover']};
            }}
        """)
        folder_frame.setCursor(Qt.CursorShape.PointingHandCursor)
        folder_frame.setFixedHeight(70)
        folder_frame.mousePressEvent = lambda e, fid=folder_id: self._on_folder_clicked(fid)
        
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
        menu_btn.clicked.connect(lambda: self._show_folder_menu(folder_id, menu_btn))
        folder_layout.addWidget(menu_btn)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        edit_btn = ModernButton("Edit")
        edit_btn.setFixedSize(60, 30)
        edit_btn.clicked.connect(lambda: self._on_folder_action(folder_id, "edit"))
        actions_layout.addWidget(edit_btn)
        
        play_all_btn = ModernButton("Play All")
        play_all_btn.setFixedSize(80, 30)
        play_all_btn.clicked.connect(lambda: self._on_folder_action(folder_id, "play_all"))
        actions_layout.addWidget(play_all_btn)
        
        folder_layout.addLayout(actions_layout)
        
        return folder_frame
    
    def _create_folder_card(self, name, folder_id, sound_count):
        """Create a folder card for grid view"""
        card = FolderCard(name, folder_id, sound_count)
        card.folder_clicked.connect(lambda fid, action: self._on_folder_action(fid, action))
        return card
    
    def _on_folder_clicked(self, folder_id):
        """Handle folder selection"""
        self.folder_selected.emit(folder_id)
    
    def _show_folder_menu(self, folder_id, button):
        """Show context menu for folder"""
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
        edit_action.triggered.connect(lambda: self._on_folder_action(folder_id, "edit"))
        menu.addAction(edit_action)
        
        delete_action = QAction("Delete", menu)
        delete_action.triggered.connect(lambda: self._on_folder_action(folder_id, "delete"))
        menu.addAction(delete_action)
        
        menu.exec(button.mapToGlobal(QPoint(0, button.height())))
    
    def _on_folder_action(self, folder_id, action):
        """Handle folder actions"""
        if action == "open":
            self.folder_selected.emit(folder_id)
        elif action == "edit":
            # TODO: Implement folder editing
            print(f"Edit folder {folder_id}")
        elif action == "delete":
            # TODO: Implement folder deletion
            print(f"Delete folder {folder_id}")
        elif action == "play_all":
            # TODO: Implement play all sounds in folder
            print(f"Play all sounds in folder {folder_id}")
    
    def _toggle_view(self, is_grid_view):
        """Toggle between grid and list views"""
        self.current_view = "grid" if is_grid_view else "list"
        self.view_stack.setCurrentIndex(0 if is_grid_view else 1)
    
    def _change_size(self, size):
        """Change size of cards"""
        self.current_size = size
        # TODO: Implement size changes for cards
    
    def _sort_folders(self, sort_by):
        """Sort folders according to criteria"""
        # TODO: Implement folder sorting

class FolderCard(QFrame):
    """Card-style view for folders in grid view"""
    folder_clicked = pyqtSignal(str, str)  # Emits folder_id and action
    
    def __init__(self, name, folder_id, sound_count=0, parent=None):
        super().__init__(parent)
        self.folder_name = name
        self.folder_id = folder_id
        self.sound_count = sound_count
        self._setup_ui()
    
    def _setup_ui(self):
        self.setFixedSize(200, 180)
        self.setStyleSheet(f"""
            FolderCard {{
                background-color: {COLORS['folder_bg']};
                border-radius: 8px;
                border: 1px solid {COLORS['divider']};
            }}
            FolderCard:hover {{
                background-color: {COLORS['folder_hover']};
                border: 1px solid {COLORS['accent']};
            }}
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(COLORS['shadow']))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        
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
        
        # Folder name
        self.name_label = QLabel(self.folder_name)
        self.name_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 16px;
            font-weight: bold;
        """)
        self.name_label.setWordWrap(True)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label)
        
        layout.addStretch()
        
        # Sound count
        self.count_label = QLabel(f"{self.sound_count} sounds")
        self.count_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 13px;
        """)
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.count_label)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
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
        edit_action.triggered.connect(lambda: self.folder_clicked.emit(self.folder_id, "edit"))
        menu.addAction(edit_action)
        
        delete_action = QAction("Delete", menu)
        delete_action.triggered.connect(lambda: self.folder_clicked.emit(self.folder_id, "delete"))
        menu.addAction(delete_action)
        
        menu.exec(self.mapToGlobal(self.menu_button.pos() + QPoint(0, self.menu_button.height())))
    
    def mousePressEvent(self, event):
        """Handle click event (open folder)"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Ignore clicks on the menu button
            if not self.menu_button.geometry().contains(event.pos()):
                self.folder_clicked.emit(self.folder_id, "open")
        super().mousePressEvent(event)

class FolderContentView(QFrame):
    """View for displaying sounds in a selected folder"""
    def __init__(self, folder_name, parent=None):
        super().__init__(parent)
        self.folder_name = folder_name
        self.current_view = "grid"  # Default to grid view
        self.current_size = "medium"  # Default size
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
                border-radius: 15px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_secondary']};
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
        # TODO: Implement sound sorting
    
    def _on_sound_action(self, sound_id, action):
        """Handle sound actions"""
        # TODO: Implement sound actions
        print(f"Sound {sound_id} action: {action}")

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
        status_bar.addWidget(QLabel("4 sounds loaded"))
        status_bar.addPermanentWidget(QLabel("Version 0.1.0"))