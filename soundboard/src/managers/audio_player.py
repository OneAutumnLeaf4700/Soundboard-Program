"""Audio player for the soundboard application"""

import os
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from typing import Optional, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal

class AudioPlayer(QObject):
    """Audio player for playing sound files"""
    
    # Define signals
    playback_started = pyqtSignal(str)  # sound_id
    playback_stopped = pyqtSignal(str)  # sound_id
    playback_error = pyqtSignal(str, str)  # sound_id, error_message
    
    def __init__(self):
        """Initialize the audio player"""
        super().__init__()
        self.current_playing: Optional[str] = None
        self.loaded_sounds: Dict[str, Dict[str, Any]] = {}
    
    def load_sound(self, sound_id: str, file_path: str) -> bool:
        """Load a sound file
        
        Args:
            sound_id: Unique identifier for the sound
            file_path: Path to the sound file
            
        Returns:
            True if the sound was loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                print(f"Sound file not found: {file_path}")
                return False
                
            # Load the audio file using pydub
            audio = AudioSegment.from_file(file_path)
            
            # Store the audio data
            self.loaded_sounds[sound_id] = {
                'file_path': file_path,
                'audio': audio,
                'duration': len(audio) / 1000  # Duration in seconds
            }
            
            return True
        except Exception as e:
            print(f"Error loading sound: {e}")
            self.playback_error.emit(sound_id, str(e))
            return False
    
    def play_sound(self, sound_id: str) -> bool:
        """Play a sound
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            True if the sound was played, False otherwise
        """
        if sound_id not in self.loaded_sounds:
            print(f"Sound not loaded: {sound_id}")
            return False
            
        try:
            # Stop any currently playing sound
            if self.current_playing:
                self.stop_sound()
            
            # Get the audio data
            sound_data = self.loaded_sounds[sound_id]
            audio = sound_data['audio']
            
            # Convert to numpy array for sounddevice
            samples = np.array(audio.get_array_of_samples())
            
            # Play the sound
            sd.play(samples, audio.frame_rate)
            
            # Update current playing
            self.current_playing = sound_id
            self.playback_started.emit(sound_id)
            
            return True
        except Exception as e:
            print(f"Error playing sound: {e}")
            self.playback_error.emit(sound_id, str(e))
            return False
    
    def stop_sound(self) -> None:
        """Stop the currently playing sound"""
        if self.current_playing:
            sd.stop()
            self.playback_stopped.emit(self.current_playing)
            self.current_playing = None
    
    def get_duration(self, sound_id: str) -> Optional[float]:
        """Get the duration of a sound in seconds
        
        Args:
            sound_id: Unique identifier for the sound
            
        Returns:
            Duration in seconds or None if not found
        """
        if sound_id in self.loaded_sounds:
            return self.loaded_sounds[sound_id]['duration']
        return None
    
    def format_duration(self, seconds: float) -> str:
        """Format duration in seconds to MM:SS format
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string
        """
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02d}"