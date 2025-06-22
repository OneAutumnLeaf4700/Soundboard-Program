# Soundboard Program

A modern, professional soundboard application for Windows, built with Python and PyQt6. Designed for streamers, presenters, and audio enthusiasts, this app makes it easy to play, organize, and customize sounds with a beautiful, intuitive interface.

---

## Table of Contents

- [Features](#features)
- [Technical Overview](#technical-overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)

---

## Features

- 🎵 **Multiple Audio Format Support:** Play MP3, WAV, and more.
- 🖱️ **Modern, User-Friendly Interface:** Clean, responsive design with PyQt6.
- ➕ **Custom Sound Import:** Easily add your own audio files.
- ⌨️ **Hotkey Support:** Trigger sounds instantly with customizable hotkeys.
- 🖥️ **System Tray Integration:** Control the app from your system tray.
- 🎚️ **Multiple Audio Device Support:** Choose your output device.
- 📊 **Sound Visualization:** See real-time audio visualizations.
- 🌗 **Theme Customization:** Light and dark modes for any environment.

---

## Technical Overview

The Soundboard Program is structured for maintainability and scalability:

- **Python & PyQt6:** Leverages PyQt6 for a native Windows look and feel.
- **Modular UI Components:** All UI elements are organized in `src/ui/components.py` and related files.
- **Main Application:** Entry point at `src/main.py`.
- **Audio Management:** Supports multiple formats and devices.
- **Hotkey & Tray Integration:** Uses platform-specific APIs for seamless user experience.

**Directory Structure:**
```
soundboard/
  ├─ src/
  │   ├─ main.py
  │   └─ ui/
  │       ├─ components.py
  │       ├─ folder_view.py
  │       ├─ main_window.py
  │       ├─ sound_card.py
  │       └─ sound_grid.py
  └─ pyproject.toml
```

---

## Requirements

- Python 3.8 or higher
- Windows 10/11

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/soundboard.git
   cd soundboard
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Run the application:**
   ```bash
   poetry run python src/main.py
   ```

---

## Usage

- Launch the app and start adding your favorite sounds.
- Assign hotkeys for quick access.
- Customize the theme and audio output device in settings.

---