import builtins
import types
import sys
import os
import sqlite3
import importlib
from unittest import mock
import pytest

# Target module path
TARGET_MODULE = 'engine.features'


def reload_features_with_mocks(mocks):
    """Import engine.features with provided attribute mocks patched in sys.modules.
    This ensures globals like cursor/conn and other heavy deps are replaced.
    """
    with mock.patch.dict(sys.modules, mocks):
        if TARGET_MODULE in sys.modules:
            del sys.modules[TARGET_MODULE]
        mod = importlib.import_module(TARGET_MODULE)
        return mod


class DummyCursor:
    def __init__(self, data_map=None):
        # data_map: {('sys_command', 'notepad'): [('C:/Windows/notepad.exe',)]}
        self.data_map = data_map or {}
        self.queries = []

    def execute(self, sql, params=()):
        self.queries.append((sql, params))
        self._last_result = []
        # very small SQL router for the specific queries used
        if 'FROM sys_command' in sql:
            name = params[0]
            self._last_result = self.data_map.get(('sys_command', name), [])
        elif 'FROM web_command' in sql:
            name = params[0]
            self._last_result = self.data_map.get(('web_command', name), [])
        elif 'FROM contacts' in sql:
            # Params are like ("%john%", "john%")
            like1, like2 = params
            name = like1.strip('%').lower()
            # Match any key starting with provided like patterns
            for (tbl, key), rows in self.data_map.items():
                if tbl == 'contacts' and (name in key or key.startswith(name)):
                    self._last_result = rows
                    break
        return self

    def fetchall(self):
        return list(self._last_result)


class DummyConn:
    def cursor(self):
        return DummyCursor()


@pytest.fixture()
def feature_module():
    # Build mocks for heavy/external deps
    mocked_sqlite3 = types.SimpleNamespace(connect=lambda *_: DummyConn())
    mocked_eel = types.SimpleNamespace(expose=lambda f: f)
    mocked_pywhatkit = types.SimpleNamespace(playonyt=lambda *_args, **_kw: None)
    mocked_pyaudio = types.SimpleNamespace(PyAudio=lambda: types.SimpleNamespace(open=lambda **kwargs: types.SimpleNamespace(read=lambda n: b"\x00\x00" * n, close=lambda: None), terminate=lambda: None), paInt16=8)
    mocked_pvporcupine = types.SimpleNamespace(create=lambda **kwargs: types.SimpleNamespace(sample_rate=16000, frame_length=512, process=lambda kw: -1, delete=lambda: None))

    mocks = {
        'sqlite3': mocked_sqlite3,
        'eel': mocked_eel,
        'pywhatkit': mocked_pywhatkit,
        'pyaudio': mocked_pyaudio,
        'pvporcupine': mocked_pvporcupine,
        'playsound': types.SimpleNamespace(playsound=lambda *_: None),
        'webbrowser': types.SimpleNamespace(open=lambda *_: None),
        'pyautogui': types.SimpleNamespace(hotkey=lambda *args: None, keyDown=lambda *_: None, keyUp=lambda *_: None, press=lambda *_: None),
        'engine.command': types.SimpleNamespace(speak=lambda *_: None),
        'engine.config': types.SimpleNamespace(ASSISTANT_NAME='jarvis'),
        'engine.helper': types.SimpleNamespace(extract_yt_term=lambda q: q, remove_words=lambda q, words: q),
        'struct': struct,
        'time': time,
        'subprocess': subprocess,
        'os': os,
    }

    mod = reload_features_with_mocks(mocks)
    return mod


# 1. playAssistantSound should call playsound with correct path
def test_play_assistant_sound_calls_playsound(tmp_path, monkeypatch):
    called = {}

    def fake_ps(path):
        called['arg'] = path

    mocks = {
        'sqlite3': types.SimpleNamespace(connect=lambda *_: DummyConn()),
        'eel': types.SimpleNamespace(expose=lambda f: f),
        'pywhatkit': types.SimpleNamespace(playonyt=lambda *_: None),
        'pyaudio': types.SimpleNamespace(PyAudio=lambda: types.SimpleNamespace(open=lambda **kwargs: types.SimpleNamespace(read=lambda n: b"\x00\x00" * n, close=lambda: None), terminate=lambda: None), paInt16=8),
        'pvporcupine': types.SimpleNamespace(create=lambda **kwargs: types.SimpleNamespace(sample_rate=16000, frame_length=512, process=lambda kw: -1, delete=lambda: None)),
        'playsound': types.SimpleNamespace(playsound=fake_ps),
        'webbrowser': types.SimpleNamespace(open=lambda *_: None),
        'pyautogui': types.SimpleNamespace(hotkey=lambda *args: None, keyDown=lambda *_: None, keyUp=lambda *_: None, press=lambda *_: None),
        'engine.command': types.SimpleNamespace(speak=lambda *_: None),
        'engine.config': types.SimpleNamespace(ASSISTANT_NAME='jarvis'),
        'engine.helper': types.SimpleNamespace(extract_yt_term=lambda q: q, remove_words=lambda q, words: q),
        'struct': struct,
        'time': time,
        'subprocess': subprocess,
        'os': os,
    }
    if TARGET_MODULE in sys.modules:
        del sys.modules[TARGET_MODULE]
    with mock.patch.dict(sys.modules, mocks):
        mod = importlib.import_module(TARGET_MODULE)
        mod.playAssistantSound()
    assert called['arg'].endswith('www\\assets\\audio\\www_assets_audio_start_sound.mp3')


# 2. openCommand opens system command via DB hit
@pytest.mark.parametrize('table, row, opener', [
    ('sys_command', ('C:/Windows/notepad.exe',), 'os'),
    ('web_command', ('https://example.com',), 'web'),
])
def test_open_command_uses_db_and_opens(monkeypatch, table, row, opener):
    opened = {'os': None, 'web': None}

    def fake_startfile(path):
        opened['os'] = path

    def fake_webopen(url):
        opened['web'] = url

    cur = DummyCursor({(table, 'notepad'): [row]})

    mocked_sqlite3 = types.SimpleNamespace(connect=lambda *_: types.SimpleNamespace(cursor=lambda: cur))

    mocks = {
        'sqlite3': mocked_sqlite3,
        'eel': types.SimpleNamespace(expose=lambda f: f),
        'pywhatkit': types.SimpleNamespace(playonyt=lambda *_: None),
        'pyaudio': types.SimpleNamespace(PyAudio=lambda: types.SimpleNamespace(open=lambda **kwargs: types.SimpleNamespace(read=lambda n: b"\x00\x00" * n, close=lambda: None), terminate=lambda: None), paInt16=8),
        'pvporcupine': types.SimpleNamespace(create=lambda **kwargs: types.SimpleNamespace(sample_rate=16000, frame_length=512, process=lambda kw: -1, delete=lambda: None)),
        'playsound': types.SimpleNamespace(playsound=lambda *_: None),
        'webbrowser': types.SimpleNamespace(open=fake_webopen),
        'pyautogui': types.SimpleNamespace(hotkey=lambda *args: None, keyDown=lambda *_: None, keyUp=lambda *_: None, press=lambda *_: None),
        'engine.command': types.SimpleNamespace(speak=lambda *_: None),
        'engine.config': types.SimpleNamespace(ASSISTANT_NAME='jarvis'),
        'engine.helper': types.SimpleNamespace(extract_yt_term=lambda q: q, remove_words=lambda q, words: q),
        'struct': struct,
        'time': time,
        'subprocess': subprocess,
        'os': types.SimpleNamespace(startfile=fake_startfile, system=lambda *_: 0),
    }

    if TARGET_MODULE in sys.modules:
        del sys.modules[TARGET_MODULE]
    with mock.patch.dict(sys.modules, mocks):
        mod = importlib.import_module(TARGET_MODULE)
        mod.openCommand('jarvis open notepad')

    if opener == 'os':
        assert opened['os'] == row[0]
    else:
        assert opened['web'] == row[0]


# 3. openCommand falls back to os.system when not found
def test_open_command_falls_back_to_os_system(monkeypatch):
    called = {'cmd': None}

    def fake_system(cmd):
        called['cmd'] = cmd
        return 0

    cur = DummyCursor({})
    mocked_sqlite3 = types.SimpleNamespace(connect=lambda *_: types.SimpleNamespace(cursor=lambda: cur))

    mocks = {
        'sqlite3': mocked_sqlite3,
        'eel': types.SimpleNamespace(expose=lambda f: f),
        'pywhatkit': types.SimpleNamespace(playonyt=lambda *_: None),
        'pyaudio': types.SimpleNamespace(PyAudio=lambda: types.SimpleNamespace(open=lambda **kwargs: types.SimpleNamespace(read=lambda n: b"\x00\x00" * n, close=lambda: None), terminate=lambda: None), paInt16=8),
        'pvporcupine': types.SimpleNamespace(create=lambda **kwargs: types.SimpleNamespace(sample_rate=16000, frame_length=512, process=lambda kw: -1, delete=lambda: None)),
        'playsound': types.SimpleNamespace(playsound=lambda *_: None),
        'webbrowser': types.SimpleNamespace(open=lambda *_: None),
        'pyautogui': types.SimpleNamespace(hotkey=lambda *args: None, keyDown=lambda *_: None, keyUp=lambda *_: None, press=lambda *_: None),
        'engine.command': types.SimpleNamespace(speak=lambda *_: None),
        'engine.config': types.SimpleNamespace(ASSISTANT_NAME='jarvis'),
        'engine.helper': types.SimpleNamespace(extract_yt_term=lambda q: q, remove_words=lambda q, words: q),
        'struct': struct,
        'time': time,
        'subprocess': subprocess,
        'os': types.SimpleNamespace(startfile=lambda *_: None, system=fake_system),
    }

    if TARGET_MODULE in sys.modules:
        del sys.modules[TARGET_MODULE]
    with mock.patch.dict(sys.modules, mocks):
        mod = importlib.import_module(TARGET_MODULE)
        mod.openCommand('jarvis open calc')
    assert called['cmd'] == 'start  calc'


# 4. findContact returns normalized number with +92 prefix
def test_find_contact_returns_number_with_prefix(monkeypatch):
    cur = DummyCursor({('contacts', 'john'): [("3001234567",)]})
    mocked_sqlite3 = types.SimpleNamespace(connect=lambda *_: types.SimpleNamespace(cursor=lambda: cur))

    mocks = {
        'sqlite3': mocked_sqlite3,
        'eel': types.SimpleNamespace(expose=lambda f: f),
        'pywhatkit': types.SimpleNamespace(playonyt=lambda *_: None),
        'pyaudio': types.SimpleNamespace(PyAudio=lambda: types.SimpleNamespace(open=lambda **kwargs: types.SimpleNamespace(read=lambda n: b"\x00\x00" * n, close=lambda: None), terminate=lambda: None), paInt16=8),
        'pvporcupine': types.SimpleNamespace(create=lambda **kwargs: types.SimpleNamespace(sample_rate=16000, frame_length=512, process=lambda kw: -1, delete=lambda: None)),
        'playsound': types.SimpleNamespace(playsound=lambda *_: None),
        'webbrowser': types.SimpleNamespace(open=lambda *_: None),
        'pyautogui': types.SimpleNamespace(hotkey=lambda *args: None, keyDown=lambda *_: None, keyUp=lambda *_: None, press=lambda *_: None),
        'engine.command': types.SimpleNamespace(speak=lambda *_: None),
        'engine.config': types.SimpleNamespace(ASSISTANT_NAME='jarvis'),
        'engine.helper': types.SimpleNamespace(extract_yt_term=lambda q: q, remove_words=lambda q, words: q),
        'struct': struct,
        'time': time,
        'subprocess': subprocess,
        'os': os,
    }

    if TARGET_MODULE in sys.modules:
        del sys.modules[TARGET_MODULE]
    with mock.patch.dict(sys.modules, mocks):
        mod = importlib.import_module(TARGET_MODULE)
        number, name = mod.findContact('jarvis call john')
        assert number == '+923001234567'
        assert 'john' in name


# 5. whatsApp constructs URL and triggers hotkeys
def test_whatsapp_constructs_url_and_triggers_hotkeys(monkeypatch):
    runs = []
    hotkeys = []

    def fake_run(cmd, shell=False):
        runs.append(cmd)
        return types.SimpleNamespace(returncode=0)

    def fake_hotkey(*args):
        hotkeys.append(args)

    mocks = {
        'sqlite3': types.SimpleNamespace(connect=lambda *_: DummyConn()),
        'eel': types.SimpleNamespace(expose=lambda f: f),
        'pywhatkit': types.SimpleNamespace(playonyt=lambda *_: None),
        'pyaudio': types.SimpleNamespace(PyAudio=lambda: types.SimpleNamespace(open=lambda **kwargs: types.SimpleNamespace(read=lambda n: b"\x00\x00" * n, close=lambda: None), terminate=lambda: None), paInt16=8),
        'pvporcupine': types.SimpleNamespace(create=lambda **kwargs: types.SimpleNamespace(sample_rate=16000, frame_length=512, process=lambda kw: -1, delete=lambda: None)),
        'playsound': types.SimpleNamespace(playsound=lambda *_: None),
        'webbrowser': types.SimpleNamespace(open=lambda *_: None),
        'pyautogui': types.SimpleNamespace(hotkey=fake_hotkey, keyDown=lambda *_: None, keyUp=lambda *_: None, press=lambda *_: None),
        'engine.command': types.SimpleNamespace(speak=lambda *_: None),
        'engine.config': types.SimpleNamespace(ASSISTANT_NAME='jarvis'),
        'engine.helper': types.SimpleNamespace(extract_yt_term=lambda q: q, remove_words=lambda q, words: q),
        'struct': struct,
        'time': time,
        'subprocess': types.SimpleNamespace(run=fake_run),
        'os': os,
    }

    if TARGET_MODULE in sys.modules:
        del sys.modules[TARGET_MODULE]
    with mock.patch.dict(sys.modules, mocks):
        mod = importlib.import_module(TARGET_MODULE)
        mod.whatsApp('+923001234567', 'Hello World!', 'message', 'john')

    assert any('whatsapp://send?phone=+923001234567&text=Hello%20World%21' in cmd for cmd in runs)
    assert ('ctrl', 'f') in hotkeys
    # TAB should be pressed multiple times via hotkey, but our fake collects hotkey only
    # Ensure enter is triggered
    assert ('enter',) in hotkeys
