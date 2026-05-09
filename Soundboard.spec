# PyInstaller spec for Soundboard
# Build with: pyinstaller Soundboard.spec
# SPECPATH is a PyInstaller-defined variable for the spec file's directory.

from pathlib import Path

project_root = Path(SPECPATH)
src_root = project_root / "soundboard" / "src"


a = Analysis(
    [str(src_root / "main.py")],
    pathex=[str(src_root)],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'scipy',
        'tkinter',
        'PyQt5',
        'PySide2',
        'PySide6',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Soundboard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
