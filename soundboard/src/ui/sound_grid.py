"""
SoundGrid Component for displaying sound cards in a grid layout
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QGridLayout,
    QLineEdit, QComboBox, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon

# Import from other modules
from soundboard.src.ui.sound_card import SoundCard
from soundboard.src.ui.main_window import COLORS

class SoundGrid(QWidget):
    """
    Grid layout for displaying sound cards
    """
    # Signals
    sound_played = pyqtSignal(str)  # Emits sound_id when a sound is played
    sound_edited = pyqtSignal(str)  # Emits sound_id when a sound is edited
    sound_favorited = pyqtSignal(str, bool)  # Emits sound_id and favorite state
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Properties
        self.sounds = {}  # Dictionary of sound_id -> SoundCard
        self.current_folder_id = None
        self.filter_text = ""
        self.sort_option = "name"  # Options: name, date, duration
        self.size_option = "medium"  # Options: small, medium, large
        self.favorite_filter = False
        
        # UI setup
        self._setup_ui()
    
    def _setup_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(16)
        
        # Header layout (search, filters, sorting)
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(12)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search sounds...")
        self.search_box.setFixedHeight(36)
        self.search_box.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['card_bg']};
                border: 1px solid {COLORS['divider']};
                border-radius: 18px;
                padding: 0 12px;
                color: {COLORS['text_primary']};
            }}
            QLineEdit:focus {{
                border: 1px solid {COLORS['accent']};
            }}
        """)
        self.search_box.textChanged.connect(self._on_filter_changed)
        self.header_layout.addWidget(self.search_box, 1)
        
        # Favorites filter button
        self.favorites_btn = QPushButton("⭐ Favorites")
        self.favorites_btn.setCheckable(True)
        self.favorites_btn.setFixedHeight(36)
        self.favorites_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card_bg']};
                border: 1px solid {COLORS['divider']};
                border-radius: 18px;
                padding: 0 16px;
                color: {COLORS['text_secondary']};
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
            QPushButton:checked {{
                background-color: {COLORS['accent_light']};
                color: {COLORS['accent']};
                border: 1px solid {COLORS['accent']};
            }}
        """)
        self.favorites_btn.toggled.connect(self._on_favorite_filter_toggled)
        self.header_layout.addWidget(self.favorites_btn)
        
        # Sort dropdown
        self.sort_label = QLabel("Sort by:")
        self.sort_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.header_layout.addWidget(self.sort_label)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Name", "Date Added", "Duration"])
        self.sort_combo.setFixedHeight(36)
        self.sort_combo.setFixedWidth(120)
        self.sort_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['card_bg']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 0 8px;
                color: {COLORS['text_primary']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: url(soundboard/assets/icons/dropdown.png);
            }}
        """)
        self.sort_combo.currentIndexChanged.connect(self._on_sort_changed)
        self.header_layout.addWidget(self.sort_combo)
        
        # Size dropdown
        self.size_label = QLabel("Size:")
        self.size_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.header_layout.addWidget(self.size_label)
        
        self.size_combo = QComboBox()
        self.size_combo.addItems(["Small", "Medium", "Large"])
        self.size_combo.setCurrentIndex(1)  # Default to medium
        self.size_combo.setFixedHeight(36)
        self.size_combo.setFixedWidth(90)
        self.size_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['card_bg']};
                border: 1px solid {COLORS['divider']};
                border-radius: 4px;
                padding: 0 8px;
                color: {COLORS['text_primary']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: url(soundboard/assets/icons/dropdown.png);
            }}
        """)
        self.size_combo.currentIndexChanged.connect(self._on_size_changed)
        self.header_layout.addWidget(self.size_combo)
        
        self.main_layout.addLayout(self.header_layout)
        
        # Scroll area for grid
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: transparent;
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLORS['scroll_handle']};
                min-height: 30px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Container widget for grid
        self.grid_container = QWidget()
        self.grid_container.setStyleSheet(f"background-color: transparent;")
        
        # Grid layout for sound cards
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(0, 0, 12, 0)  # Right margin for scrollbar
        self.grid_layout.setSpacing(16)
        
        self.scroll_area.setWidget(self.grid_container)
        self.main_layout.addWidget(self.scroll_area)
        
        # Empty state label
        self.empty_label = QLabel("No sounds found. Add some sounds or try a different filter.")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 16px;
            margin: 40px 0;
        """)
        self.empty_label.setVisible(False)
        self.main_layout.addWidget(self.empty_label)
    
    def add_sound(self, title, category, sound_id, duration=0, favorite=False):
        """
        Add a sound card to the grid
        """
        if sound_id in self.sounds:
            # If sound already exists, update it
            self.sounds[sound_id].title = title
            self.sounds[sound_id].category = category
            self.sounds[sound_id].duration = duration
            self.sounds[sound_id].favorite = favorite
            return
        
        # Create sound card
        sound_card = SoundCard(
            title=title,
            category=category,
            sound_id=sound_id,
            duration=duration,
            favorite=favorite
        )
        
        # Set card size based on current setting
        sound_card.set_size(self.size_option)
        
        # Connect signals
        sound_card.play_clicked.connect(lambda sid: self.sound_played.emit(sid))
        sound_card.edit_clicked.connect(lambda sid: self.sound_edited.emit(sid))
        sound_card.favorite_toggled.connect(lambda sid, state: self.sound_favorited.emit(sid, state))
        
        # Add to dictionary
        self.sounds[sound_id] = sound_card
        
        # Update grid layout
        self._apply_filters()
    
    def remove_sound(self, sound_id):
        """
        Remove a sound card from the grid
        """
        if sound_id in self.sounds:
            # Remove from UI
            sound_card = self.sounds[sound_id]
            self.grid_layout.removeWidget(sound_card)
            sound_card.deleteLater()
            
            # Remove from dictionary
            del self.sounds[sound_id]
            
            # Update grid layout
            self._apply_filters()
    
    def clear_sounds(self):
        """
        Remove all sound cards from the grid
        """
        # Make a copy of keys to avoid modifying during iteration
        sound_ids = list(self.sounds.keys())
        
        for sound_id in sound_ids:
            self.remove_sound(sound_id)
    
    def set_folder(self, folder_id):
        """
        Set the current folder to display sounds from
        """
        self.current_folder_id = folder_id
        self._apply_filters()
    
    def _on_filter_changed(self):
        """
        Handle filter text changes
        """
        self.filter_text = self.search_box.text().lower()
        self._apply_filters()
    
    def _on_favorite_filter_toggled(self, checked):
        """
        Handle favorites filter toggle
        """
        self.favorite_filter = checked
        self._apply_filters()
    
    def _on_sort_changed(self, index):
        """
        Handle sort option changes
        """
        sort_options = ["name", "date", "duration"]
        if index < len(sort_options):
            self.sort_option = sort_options[index]
            self._apply_filters()
    
    def _on_size_changed(self, index):
        """
        Handle card size changes
        """
        size_options = ["small", "medium", "large"]
        if index < len(size_options):
            self.size_option = size_options[index]
            
            # Update all cards with new size
            for sound_card in self.sounds.values():
                sound_card.set_size(self.size_option)
            
            # Refresh layout
            self._apply_filters()
    
    def _apply_filters(self):
        """
        Apply current filters, sorting, and update the grid layout
        """
        # First, remove all widgets from grid
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        # Filter sounds
        filtered_sounds = []
        for sound_id, card in self.sounds.items():
            # Check folder filter (if applicable)
            # This would need to be integrated with the actual folder system
            
            # Check text filter
            title_match = self.filter_text == "" or self.filter_text in card.title.lower()
            category_match = self.filter_text == "" or self.filter_text in card.category.lower()
            
            # Check favorites filter
            favorite_match = not self.favorite_filter or card.favorite
            
            if (title_match or category_match) and favorite_match:
                filtered_sounds.append(card)
        
        # Sort sounds
        if self.sort_option == "name":
            filtered_sounds.sort(key=lambda card: card.title.lower())
        elif self.sort_option == "duration":
            filtered_sounds.sort(key=lambda card: card.duration)
        elif self.sort_option == "date":
            # In a real implementation, each card would have a creation date
            # For now, just maintain the existing order
            pass
        
        # Show empty state if no sounds
        if not filtered_sounds:
            self.empty_label.setVisible(True)
            return
        else:
            self.empty_label.setVisible(False)
        
        # Calculate columns based on container width and card size
        container_width = self.grid_container.width()
        card_width = filtered_sounds[0].card_width if filtered_sounds else 220  # Default medium
        spacing = self.grid_layout.spacing()
        
        # Calculate max columns that fit in the container
        max_columns = max(1, container_width // (card_width + spacing))
        
        # Add cards to grid
        for i, card in enumerate(filtered_sounds):
            row = i // max_columns
            col = i % max_columns
            self.grid_layout.addWidget(card, row, col)
        
        # Update grid container
        self.grid_container.updateGeometry()
    
    def resizeEvent(self, event):
        """
        Handle resize events to adjust the grid layout
        """
        super().resizeEvent(event)
        self._apply_filters()
    
    def populate_sample_sounds(self):
        """
        Add some sample sounds for testing
        """
        sample_data = [
            {"title": "Dog Bark", "category": "Animal", "duration": 3, "favorite": True},
            {"title": "Cat Meow", "category": "Animal", "duration": 2, "favorite": False},
            {"title": "Door Bell", "category": "Effect", "duration": 4, "favorite": False},
            {"title": "Thunder", "category": "Nature", "duration": 8, "favorite": True},
            {"title": "Applause", "category": "Effect", "duration": 5, "favorite": False},
            {"title": "Bird Chirp", "category": "Animal", "duration": 6, "favorite": False},
            {"title": "Car Horn", "category": "Vehicle", "duration": 1, "favorite": False},
            {"title": "Rain", "category": "Nature", "duration": 15, "favorite": True},
            {"title": "Clock Ticking", "category": "Effect", "duration": 7, "favorite": False},
            {"title": "Phone Ring", "category": "Effect", "duration": 4, "favorite": True},
            {"title": "Laughter", "category": "Human", "duration": 5, "favorite": False},
            {"title": "Glass Breaking", "category": "Effect", "duration": 2, "favorite": False},
        ]
        
        for i, data in enumerate(sample_data):
            self.add_sound(
                title=data["title"],
                category=data["category"],
                sound_id=f"sample_{i}",
                duration=data["duration"],
                favorite=data["favorite"]
            ) 