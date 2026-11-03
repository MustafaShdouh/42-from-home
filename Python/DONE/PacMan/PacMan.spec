# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller recipe; run from the repository root with make package."""

from PyInstaller.utils.hooks import collect_data_files


analysis = Analysis(
    ["pac-man.py"],
    pathex=[],
    binaries=[],
    datas=[("README.md", ".")] + collect_data_files("ui"),
    hiddenimports=["ui.renderer", "mazegenerator"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["core/packaging_hook.py"],
    excludes=[],
    noarchive=False,
)
archive = PYZ(analysis.pure)
executable = EXE(
    archive,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    name="PacMan",
    debug=False,
    strip=False,
    upx=False,
    console=True,
)
