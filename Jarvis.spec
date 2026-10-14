# -*- mode: python ; coding: utf-8 -*-
# Build with:  pyinstaller --noconfirm Jarvis.spec
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = [("www", "www")]
datas += collect_data_files("eel")            # eel.js
datas += collect_data_files("pvporcupine")    # wake-word models/libs
datas += collect_data_files("pywhatkit")

hiddenimports = []
# Explicit list: importing engine.db at build time would run its script code.
hiddenimports += [
    "engine.chat_history", "engine.command", "engine.config",
    "engine.features", "engine.helper", "engine.login",
    "engine.paths", "engine.reminder", "engine.system_control",
]
hiddenimports += collect_submodules("pvporcupine")
hiddenimports += [
    "bottle_websocket",
    "gevent.ssl",
    "gevent.builtins",
    "geventwebsocket.handler",
    "pyttsx3.drivers",
    "pyttsx3.drivers.sapi5",
    "comtypes.stream",
    "win32com.client",
    "pycaw.pycaw",
    "screen_brightness_control",
]

a = Analysis(
    ["launcher.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Jarvis",
    icon=None,
    console=True,   # set to False once everything works to hide the black window
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name="Jarvis",
)
