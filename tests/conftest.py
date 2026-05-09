"""Shared pytest configuration."""

import os
import sys

# Use Qt's offscreen platform plugin so QFileDialog / QObject construction
# doesn't require a display server in CI or on headless machines.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# pytest.ini's pythonpath= already adds soundboard/src, but we re-assert here
# so direct invocations (e.g. `python -m pytest tests/test_x.py`) work too.
SRC = os.path.join(os.path.dirname(__file__), "..", "soundboard", "src")
if SRC not in sys.path:
    sys.path.insert(0, os.path.abspath(SRC))


import pytest


@pytest.fixture(scope="session", autouse=True)
def _qcore_app():
    """A single QCoreApplication keeps Qt signal/slot machinery happy across tests."""
    from PyQt6.QtCore import QCoreApplication
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv or [""])
    return app
