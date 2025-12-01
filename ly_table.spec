# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller 빌드 설정

PRD 섹션 7 "Deployment & Distribution"에 정의된 설정을 적용합니다.

빌드 명령어:
    pyinstaller ly_table.spec
"""

block_cipher = None


a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.styles',
        'openpyxl.utils',
        'openpyxl.worksheet',
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pytest',
        'pytest-cov',
        'mypy',
        'pylint',
        'black',
        'flake8'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LY_Table_Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI 앱이므로 콘솔 숨김
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico'  # 아이콘 파일 (옵션)
)
