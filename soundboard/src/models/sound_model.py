"""Sound data model for the soundboard application"""

import os
import json
from typing import Dict, List, Optional, Any

class SoundModel:
    """Model for managing sound data including favorites"""
    
    def __init__(self, data_file: str = None):
        """Initialize the sound model
        
        Args:
            data_file: Path to the JSON file for storing sound data
        """
        self.sounds: Dict[str, Dict[str, Any]] = {}
        self.favorites: List[str] = []
        self.data_file = data_file or os.path.join(os.path.expanduser("~"), ".soundboard", "sounds.json")
        self._ensure_data_dir()
        self._load_data()
    
    def _ensure_data_dir(self) -> None:
        """Ensure the data directory exists"""
        data_dir = os.path.dirname(self.data_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_data(self) -> None:
        """Load sound data from the JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.sounds = data.get('sounds', {})
                    self.favorites = data.get('favorites', [])
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading sound data: {e}")
    
    def _save_data(self) -> None:
        """Save sound data to the JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'sounds': self.sounds,
                    'favorites': self.favorites
                }, f, indent=2)
        except IOError as e:
            print(f"Error saving sound data: {e}")
    
    def add_sound(self, sound_id: str, sound_data: Dict[str, Any]) -> None:
        """Add or update a sound in the collection
        
        Args:
            sound_id: Unique identifier for the sound
            sound_data: Dictionary containing sound data
        """
        self.sounds[sound_id] = sound_data
        self._save_data()
    
    def remove_sound(self, sound_id: str) -> bool:
        """Remove a sound from the collection
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound was removed, False otherwise
        """
        if sound_id in self.sounds:
            del self.sounds[sound_id]
            # Also remove from favorites if present
            if sound_id in self.favorites:
                self.favorites.remove(sound_id)
            self._save_data()
            return True
        return False
    
    def get_sound(self, sound_id: str) -> Optional[Dict[str, Any]]:
        """Get a sound by its ID
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            Sound data dictionary or None if not found
        """
        return self.sounds.get(sound_id)
    
    def get_all_sounds(self) -> Dict[str, Dict[str, Any]]:
        """Get all sounds
        
        Returns:
            Dictionary of all sounds
        """
        return self.sounds
    
    def add_to_favorites(self, sound_id: str) -> bool:
        """Add a sound to favorites
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound was added to favorites, False otherwise
        """
        if sound_id in self.sounds and sound_id not in self.favorites:
            self.favorites.append(sound_id)
            self._save_data()
            return True
        return False
    
    def remove_from_favorites(self, sound_id: str) -> bool:
        """Remove a sound from favorites
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound was removed from favorites, False otherwise
        """
        if sound_id in self.favorites:
            self.favorites.remove(sound_id)
            self._save_data()
            return True
        return False
    
    def toggle_favorite(self, sound_id: str) -> bool:
        """Toggle a sound's favorite status
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound is now a favorite, False otherwise
        """
        if sound_id in self.favorites:
            self.remove_from_favorites(sound_id)
            return False
        else:
            self.add_to_favorites(sound_id)
            return True
    
    def is_favorite(self, sound_id: str) -> bool:
        """Check if a sound is a favorite
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound is a favorite, False otherwise
        """
        return sound_id in self.favorites
    
    def get_favorites(self) -> List[Dict[str, Any]]:
        """Get all favorite sounds
        
        Returns:
            List of favorite sound data dictionaries with sound_id included
        """
        favorites_list = []
        for sound_id in self.favorites:
            if sound_id in self.sounds:
                sound_data = self.sounds[sound_id].copy()
                sound_data['id'] = sound_id
                favorites_list.append(sound_data)
        return favorites_list