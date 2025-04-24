"""
SoundCard Implementation for the Soundboard
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QProgressBar, QMenu,
    QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QColor, QAction

# Import from other modules
from soundboard.src.ui.main_window import COLORS

class SoundCard(QWidget):
    """
    Widget representing a sound clip card in the grid
    """
    # Signals
    play_clicked = pyqtSignal(str)  # Emits sound_id when play button is clicked
    edit_clicked = pyqtSignal(str)  # Emits sound_id when edit button is clicked
    favorite_toggled = pyqtSignal(str, bool)  # Emits sound_id and favorite state
    
    def __init__(self, title, category, sound_id, duration=0, favorite=False, parent=None):
        super().__init__(parent)
        
        # Properties
        self.title = title
        self.category = category
        self.sound_id = sound_id
        self.duration = duration
        self.favorite = favorite
        self.is_playing = False
        self.hotkey = None
        
        # Card size values (default: medium)
        self.card_width = 220
        self.card_height = 140
        self.title_font_size = 15
        self.category_font_size = 12
        self.duration_font_size = 11
        self.button_size = 36
        
        self._setup_ui()
    
    def _setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Card frame
        self.card_frame = QFrame()
        self.card_frame.setObjectName("card_frame")
        self.card_frame.setFixedSize(self.card_width, self.card_height)
        self.card_frame.setStyleSheet(f"""
            QFrame#card_frame {{
                background-color: {COLORS['card_bg']};
                border-radius: 8px;
                border: 1px solid {COLORS['divider']};
            }}
        """)
        
        # Card layout
        card_layout = QVBoxLayout(self.card_frame)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(8)
        
        # Category row
        category_row = QHBoxLayout()
        category_row.setContentsMargins(0, 0, 0, 0)
        category_row.setSpacing(6)
        
        self.category_label = QLabel(self.category)
        self.category_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: {self.category_font_size}px;
        """)
        category_row.addWidget(self.category_label)
        
        category_row.addStretch()
        
        # Favorite indicator
        self.favorite_label = QLabel("⭐" if self.favorite else "")
        self.favorite_label.setStyleSheet(f"""
            color: {COLORS['favorite']};
            font-size: {self.category_font_size}px;
        """)
        category_row.addWidget(self.favorite_label)
        
        # Hotkey label (if set)
        self.hotkey_label = QLabel("")
        self.hotkey_label.setStyleSheet(f"""
            color: {COLORS['accent']};
            font-size: {self.category_font_size}px;
            padding: 2px 6px;
            background-color: {COLORS['accent_light']};
            border-radius: 3px;
        """)
        self.hotkey_label.setVisible(False)
        category_row.addWidget(self.hotkey_label)
        
        card_layout.addLayout(category_row)
        
        # Title row
        self.title_label = QLabel(self.title)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: {self.title_font_size}px;
            font-weight: bold;
        """)
        card_layout.addWidget(self.title_label)
        
        # Add stretch to push controls to bottom
        card_layout.addStretch()
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {COLORS['progress_bg']};
                border-radius: 2px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['accent']};
                border-radius: 2px;
            }}
        """)
        self.progress_bar.setVisible(False)
        card_layout.addWidget(self.progress_bar)
        
        # Controls row
        controls_row = QHBoxLayout()
        controls_row.setContentsMargins(0, 0, 0, 0)
        controls_row.setSpacing(8)
        
        # Duration label
        duration_text = self._format_duration(self.duration)
        self.duration_label = QLabel(duration_text)
        self.duration_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: {self.duration_font_size}px;
        """)
        controls_row.addWidget(self.duration_label)
        
        controls_row.addStretch()
        
        # Play button
        self.play_button = QPushButton()
        self.play_button.setFixedSize(self.button_size, self.button_size)
        self.play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                border-radius: {self.button_size // 2}px;
                border: none;
                image: url(soundboard/assets/icons/play.png);
                image-position: center;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_hover']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['accent_pressed']};
            }}
        """)
        self.play_button.clicked.connect(self._on_play_clicked)
        controls_row.addWidget(self.play_button)
        
        # Menu button (for edit, favorite, etc.)
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
                background-color: {COLORS['button_hover']};
            }}
        """)
        self.menu_button.clicked.connect(self._show_context_menu)
        controls_row.addWidget(self.menu_button)
        
        card_layout.addLayout(controls_row)
        
        # Add card to main layout
        main_layout.addWidget(self.card_frame)
        
        # Set up focus and hover styling
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        
        # Set up context menu
        self._setup_context_menu()
    
    def _setup_context_menu(self):
        """Set up the context menu for the card"""
        self.context_menu = QMenu(self)
        
        # Edit action
        edit_action = QAction("Edit", self)
        edit_action.triggered.connect(lambda: self.edit_clicked.emit(self.sound_id))
        self.context_menu.addAction(edit_action)
        
        # Toggle favorite action
        self.favorite_action = QAction("Remove from Favorites" if self.favorite else "Add to Favorites", self)
        self.favorite_action.triggered.connect(self._toggle_favorite)
        self.context_menu.addAction(self.favorite_action)
        
        # Set hotkey action
        self.hotkey_action = QAction("Remove Hotkey" if self.hotkey else "Set Hotkey", self)
        self.hotkey_action.triggered.connect(self._toggle_hotkey)
        self.context_menu.addAction(self.hotkey_action)
        
        # Separator
        self.context_menu.addSeparator()
        
        # Delete action
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: print(f"Delete sound {self.sound_id}"))  # To be connected later
        self.context_menu.addAction(delete_action)
    
    def _show_context_menu(self):
        """Show the context menu when menu button is clicked"""
        # Update action text based on current state
        self.favorite_action.setText("Remove from Favorites" if self.favorite else "Add to Favorites")
        self.hotkey_action.setText("Remove Hotkey" if self.hotkey else "Set Hotkey")
        
        # Show the menu at button position
        self.context_menu.exec(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))
    
    def _on_play_clicked(self):
        """Handle play button click"""
        self.set_playing(True)
        self.play_clicked.emit(self.sound_id)
    
    def _toggle_favorite(self):
        """Toggle favorite state"""
        self.favorite = not self.favorite
        self.favorite_label.setText("⭐" if self.favorite else "")
        self.favorite_toggled.emit(self.sound_id, self.favorite)
    
    def _toggle_hotkey(self):
        """Handle hotkey toggle"""
        if self.hotkey:
            # Remove hotkey
            self.set_hotkey(None)
        else:
            # In a real implementation, this would show a dialog to set hotkey
            # For now, just set a dummy hotkey
            self.set_hotkey("F1")
    
    def set_playing(self, is_playing):
        """Set the playing state of the card"""
        self.is_playing = is_playing
        
        # Show/hide progress bar
        self.progress_bar.setVisible(is_playing)
        
        # Update play button style to show playing state
        if is_playing:
            self.card_frame.setStyleSheet(f"""
                QFrame#card_frame {{
                    background-color: {COLORS['card_bg']};
                    border-radius: 8px;
                    border: 2px solid {COLORS['accent']};
                }}
            """)
            
            self.play_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent_pressed']};
                    border-radius: {self.button_size // 2}px;
                    border: none;
                    image: url(soundboard/assets/icons/pause.png);
                    image-position: center;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['accent_hover']};
                }}
            """)
        else:
            self.card_frame.setStyleSheet(f"""
                QFrame#card_frame {{
                    background-color: {COLORS['card_bg']};
                    border-radius: 8px;
                    border: 1px solid {COLORS['divider']};
                }}
            """)
            
            self.play_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent']};
                    border-radius: {self.button_size // 2}px;
                    border: none;
                    image: url(soundboard/assets/icons/play.png);
                    image-position: center;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['accent_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {COLORS['accent_pressed']};
                }}
            """)
    
    def update_progress(self, progress):
        """Update the progress bar value (0-100)"""
        self.progress_bar.setValue(progress)
    
    def set_hotkey(self, hotkey):
        """Set or remove hotkey"""
        self.hotkey = hotkey
        
        if hotkey:
            self.hotkey_label.setText(hotkey)
            self.hotkey_label.setVisible(True)
        else:
            self.hotkey_label.setText("")
            self.hotkey_label.setVisible(False)
    
    def set_size(self, size):
        """Set the card size (small, medium, large)"""
        if size == "small":
            self.card_width = 160
            self.card_height = 110
            self.title_font_size = 13
            self.category_font_size = 11
            self.duration_font_size = 10
            self.button_size = 32
        elif size == "medium":
            self.card_width = 220
            self.card_height = 140
            self.title_font_size = 15
            self.category_font_size = 12
            self.duration_font_size = 11
            self.button_size = 36
        elif size == "large":
            self.card_width = 280
            self.card_height = 170
            self.title_font_size = 16
            self.category_font_size = 13
            self.duration_font_size = 12
            self.button_size = 40
        
        # Update UI with new sizes
        self.card_frame.setFixedSize(self.card_width, self.card_height)
        self.title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: {self.title_font_size}px;
            font-weight: bold;
        """)
        self.category_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: {self.category_font_size}px;
        """)
        self.favorite_label.setStyleSheet(f"""
            color: {COLORS['favorite']};
            font-size: {self.category_font_size}px;
        """)
        self.hotkey_label.setStyleSheet(f"""
            color: {COLORS['accent']};
            font-size: {self.category_font_size}px;
            padding: 2px 6px;
            background-color: {COLORS['accent_light']};
            border-radius: 3px;
        """)
        self.duration_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: {self.duration_font_size}px;
        """)
        self.play_button.setFixedSize(self.button_size, self.button_size)
        
        # Update play button border radius
        play_btn_style = self.play_button.styleSheet()
        play_btn_style = play_btn_style.replace(
            f"border-radius: {self.button_size // 2 - 2}px;", 
            f"border-radius: {self.button_size // 2}px;"
        )
        self.play_button.setStyleSheet(play_btn_style)
    
    def _format_duration(self, seconds):
        """Format seconds into mm:ss format"""
        minutes = seconds // 60
        seconds %= 60
        
        if minutes > 0:
            return f"{minutes}:{seconds:02d}"
        else:
            return f"{seconds}s"
    
    def enterEvent(self, event):
        """Handle mouse enter event for hover effect"""
        if not self.is_playing:
            self.card_frame.setStyleSheet(f"""
                QFrame#card_frame {{
                    background-color: {COLORS['card_hover']};
                    border-radius: 8px;
                    border: 1px solid {COLORS['divider']};
                }}
            """)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave event to remove hover effect"""
        if not self.is_playing:
            self.card_frame.setStyleSheet(f"""
                QFrame#card_frame {{
                    background-color: {COLORS['card_bg']};
                    border-radius: 8px;
                    border: 1px solid {COLORS['divider']};
                }}
            """)
        super().leaveEvent(event)
    
    def contextMenuEvent(self, event):
        """Show context menu on right-click"""
        self._show_context_menu()
        event.accept() 