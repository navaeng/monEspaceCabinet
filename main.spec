# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_all, collect_submodules

python_dlls = os.path.join(sys.base_prefix, "DLLs")

pyqt6_binaries = collect_dynamic_libs('PyQt6')
pyqt6_datas = collect_data_files('PyQt6', subdir='Qt6/plugins/platforms')


datas, binaries, hiddenimports = collect_all('PyQt6')
binaries += collect_dynamic_libs('pydantic_core')

a = Analysis(
    ['main.py'],
    pathex=[],

    binaries = binaries + collect_dynamic_libs('pydantic_core') + [
        (os.path.join(python_dlls, "libssl-1_1.dll"), "."),
        (os.path.join(python_dlls, "libcrypto-1_1.dll"), "."),
    ] + pyqt6_binaries,

datas = datas + pyqt6_datas + [
        ('ressources', 'ressources'), 
        ('.env', '.'),  
        (os.path.join(sys.base_prefix, "Lib", "site-packages", "setuptools", "_vendor", "jaraco", "text", "Lorem ipsum.txt"),
         "setuptools/_vendor/jaraco/text"),
    ], 

     hiddenimports=[
        'PyQt6.QtCore', 
        'PyQt6.QtWidgets', 
        'PyQt6.QtGui',
        'docxtpl',
        'jinja2',
        'jinja2.ext',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'docx',
        'docx.oxml',
        'docx.oxml.text',
        'docx.oxml.table',
        'deep_translator',
        'deep_translator.google_translator',
        'deep_translator.deepl',
        'babel',
        'babel.numbers',
        'PIL',
        'PIL.Image',
        'PyPDF2',
        'fitz',  
        'anthropic',
        'groq',
        'requests',
        'beautifulsoup4',
        'bs4',
        'defusedxml',
        'python-dotenv',
        'pydantic_core._pydantic_core',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
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