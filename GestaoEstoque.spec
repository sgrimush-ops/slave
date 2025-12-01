# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['interface.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('scripts', 'scripts'),
        ('data/colunas.txt', 'data'),
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'pyarrow',
        'requests',
        'tkinter',
        'tkinter.scrolledtext',
        'tkinter.ttk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy.testing',
        'IPython',
        'jupyter',
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
    name='GestaoEstoque',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sem console extra
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Adicione um ícone .ico se tiver
)
