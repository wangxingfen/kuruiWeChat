import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# 添加数据文件
datas = [
    ('settings.json', '.'),  # 配置文件
]

a = Analysis(
    ['APP.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'openai',
        'tkinter',
        'wxauto',
        'json',
        'threading',
        'requests',
        'uuid',
        'os',
        'time',
        'ramdom'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='酷睿微信助手3.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version.txt',
    icon='icon.ico'
)
