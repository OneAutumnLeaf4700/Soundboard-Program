class ViewControls(QWidget):
    """Controls for changing view mode and card size"""
    grid_view_toggled = pyqtSignal(bool)
    size_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # View label
        view_label = QLabel("View:")
        view_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(view_label)
        
        # View selector
        self.view_combo = QComboBox()
        self.view_combo.addItems(["Grid View", "List View"])
        self.view_combo.setCurrentIndex(0)  # Grid view by default
        self.view_combo.setStyleSheet(f"""
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
        self.view_combo.currentIndexChanged.connect(self._on_view_changed)
        layout.addWidget(self.view_combo)
        
        # Size selector
        size_label = QLabel("Size:")
        size_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(size_label)
        
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
        
        # Sort selector
        sort_label = QLabel("Sort:")
        sort_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(sort_label)
        
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
        layout.addWidget(self.sort_combo)
    
    def _on_view_changed(self, index):
        """Handle view combo box change"""
        # Emit signal with the current state (True for grid, False for list)
        self.grid_view_toggled.emit(index == 0)
    
    def _on_size_changed(self, index):
        """Handle size combo box change"""
        sizes = ["small", "medium", "large"]
        if 0 <= index < len(sizes):
            # Emit signal with the selected size
            self.size_changed.emit(sizes[index])