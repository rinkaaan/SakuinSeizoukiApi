# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['api/run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('static', 'static'),
        ('api/.env.prod', '.'),
    ],
    hiddenimports=[
        'apiflask.settings'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='索引製造機',
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
app = BUNDLE(
    exe,
    name='索引製造機.app',
    icon='dist/Icon.icns',
    bundle_identifier='com.rinkaaan.SakuinSeizouki',
)
