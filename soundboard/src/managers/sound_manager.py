"""Sound manager for the soundboard application"""

import os
import uuid
from typing import Dict, List, Optional, Any, Callable
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QFileDialog

# Import the sound model and audio player
from models.sound_model import SoundModel
from managers.audio_player import AudioPlayer

class SoundManager(QObject):
    """Manager for handling sound operations"""
    
    # Define signals
    sound_added = pyqtSignal(str, dict)  # sound_id, sound_data
    sound_removed = pyqtSignal(str)  # sound_id
    sound_updated = pyqtSignal(str, dict)  # sound_id, sound_data
    favorite_added = pyqtSignal(str)  # sound_id
    favorite_removed = pyqtSignal(str)  # sound_id
    sound_played = pyqtSignal(str)  # sound_id
    
    def __init__(self, data_file: str = None):
        """Initialize the sound manager
        
        Args:
            data_file: Path to the JSON file for storing sound data
        """
        super().__init__()
        self.model = SoundModel(data_file)
        self.audio_player = AudioPlayer()
        self.current_playing: Optional[str] = None
        
        # Connect audio player signals
        self.audio_player.playback_started.connect(self._on_playback_started)
        self.audio_player.playback_stopped.connect(self._on_playback_stopped)
        self.audio_player.playback_error.connect(self._on_playback_error)
    
    def add_sound(self, sound_id: str, sound_data: Dict[str, Any]) -> None:
        """Add or update a sound
        
        Args:
            sound_id: Unique identifier for the sound
            sound_data: Dictionary containing sound data
        """
        self.model.add_sound(sound_id, sound_data)
        self.sound_added.emit(sound_id, sound_data)
        
    def select_and_add_sound_file(self, parent=None) -> Optional[str]:
        """Open a file dialog to select a sound file and add it to the collection
        
        Args:
            parent: Parent widget for the file dialog
            
        Returns:
            The sound_id of the added sound, or None if cancelled
        """
        # Open file dialog to select sound file
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Select Sound File",
            "",
            "Audio Files (*.mp3 *.wav *.ogg *.flac);;All Files (*)"
        )
        
        if not file_path:
            return None  # User cancelled
            
        # Generate a unique ID for the sound
        sound_id = str(uuid.uuid4())
        
        # Get file information
        file_name = os.path.basename(file_path)
        name, _ = os.path.splitext(file_name)
        
        # Create sound data
        sound_data = {
            "title": name,
            "category": 1,  # Default category
            "file_path": file_path,
            "favorite": False
        }
        
        # Try to load the sound to get its duration
        if self.audio_player.load_sound(sound_id, file_path):
            duration = self.audio_player.get_duration(sound_id)
            if duration:
                sound_data["duration"] = self.audio_player.format_duration(duration)
            
        # Add the sound to the collection
        self.add_sound(sound_id, sound_data)
        
        return sound_id
    
    def remove_sound(self, sound_id: str) -> bool:
        """Remove a sound
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound was removed, False otherwise
        """
        if self.model.remove_sound(sound_id):
            self.sound_removed.emit(sound_id)
            return True
        return False
    
    def get_sound(self, sound_id: str) -> Optional[Dict[str, Any]]:
        """Get a sound by its ID
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            Sound data dictionary or None if not found
        """
        return self.model.get_sound(sound_id)
    
    def get_all_sounds(self) -> Dict[str, Dict[str, Any]]:
        """Get all sounds
        
        Returns:
            Dictionary of all sounds
        """
        return self.model.get_all_sounds()
    
    def toggle_favorite(self, sound_id: str) -> bool:
        """Toggle a sound's favorite status
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound is now a favorite, False otherwise
        """
        is_favorite = self.model.toggle_favorite(sound_id)
        
        # Emit the appropriate signal
        if is_favorite:
            self.favorite_added.emit(sound_id)
        else:
            self.favorite_removed.emit(sound_id)
        
        # Also emit sound updated signal with updated data
        sound_data = self.model.get_sound(sound_id)
        if sound_data:
            self.sound_updated.emit(sound_id, sound_data)
        
        return is_favorite
    
    def add_to_favorites(self, sound_id: str) -> bool:
        """Add a sound to favorites
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound was added to favorites, False otherwise
        """
        if self.model.add_to_favorites(sound_id):
            self.favorite_added.emit(sound_id)
            
            # Also emit sound updated signal
            sound_data = self.model.get_sound(sound_id)
            if sound_data:
                self.sound_updated.emit(sound_id, sound_data)
            
            return True
        return False
    
    def remove_from_favorites(self, sound_id: str) -> bool:
        """Remove a sound from favorites
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound was removed from favorites, False otherwise
        """
        if self.model.remove_from_favorites(sound_id):
            self.favorite_removed.emit(sound_id)
            
            # Also emit sound updated signal
            sound_data = self.model.get_sound(sound_id)
            if sound_data:
                self.sound_updated.emit(sound_id, sound_data)
            
            return True
        return False
    
    def is_favorite(self, sound_id: str) -> bool:
        """Check if a sound is a favorite
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound is a favorite, False otherwise
        """
        return self.model.is_favorite(sound_id)
    
    def get_favorites(self) -> List[Dict[str, Any]]:
        """Get all favorite sounds
        
        Returns:
            List of favorite sound data dictionaries
        """
        return self.model.get_favorites()
    
    def play_sound(self, sound_id: str) -> bool:
        """Play a sound
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound was played, False otherwise
        """
        sound_data = self.model.get_sound(sound_id)
        if sound_data:
            # Check if the sound has a file path
            if 'file_path' in sound_data and os.path.exists(sound_data['file_path']):
                # If the sound is already loaded, play it
                if self.audio_player.play_sound(sound_id):
                    return True
                    
                # Otherwise, try to load and play it
                if self.audio_player.load_sound(sound_id, sound_data['file_path']):
                    return self.audio_player.play_sound(sound_id)
            else:
                # For sample sounds without real files, just emit the signal
                self.current_playing = sound_id
                self.sound_played.emit(sound_id)
                return True
        return False
    
    def stop_sound(self) -> None:
        """Stop the currently playing sound"""
        self.audio_player.stop_sound()
        self.current_playing = None
        
    def _on_playback_started(self, sound_id: str) -> None:
        """Handle when playback starts
        
        Args:
            sound_id: Unique identifier for the sound
        """
        self.current_playing = sound_id
        self.sound_played.emit(sound_id)
        
    def _on_playback_stopped(self, sound_id: str) -> None:
        """Handle when playback stops
        
        Args:
            sound_id: Unique identifier for the sound
        """
        self.current_playing = None
        
    def _on_playback_error(self, sound_id: str, error_message: str) -> None:
        """Handle playback errors
        
        Args:
            sound_id: Unique identifier for the sound
            error_message: Error message
        """
        print(f"Playback error for sound {sound_id}: {error_message}")
        self.current_playing = None