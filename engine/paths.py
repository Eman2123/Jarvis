"""Path helpers so Jarvis works both from source and as a packaged .exe.

- resource_path(): read-only files shipped with the app (www/, sounds, images).
- DB_PATH: writable SQLite database. When frozen (.exe) it lives in
  %APPDATA%\\Jarvis so it survives updates and does not need admin rights.
  When run from source it stays in the project folder, as before.
"""
import os
import sqlite3
import sys

APP_NAME = "Jarvis"


def is_frozen():
    return getattr(sys, "frozen", False)


def base_dir():
    """Folder that contains www/ and engine/."""
    if is_frozen():
        # PyInstaller one-file extracts to sys._MEIPASS, one-dir uses it too.
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resource_path(*parts):
    return os.path.join(base_dir(), *parts)


def data_dir():
    if is_frozen():
        root = os.environ.get("APPDATA") or os.path.expanduser("~")
        path = os.path.join(root, APP_NAME)
    else:
        path = base_dir()
    os.makedirs(path, exist_ok=True)
    return path


DB_PATH = os.path.join(data_dir(), "jarvis.db")


def init_db():
    """Create tables that other modules query but never create."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS sys_command("
        "id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS web_command("
        "id INTEGER PRIMARY KEY, name VARCHAR(100), url VARCHAR(1000))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS contacts("
        "id INTEGER PRIMARY KEY, name VARCHAR(200), mobile_no VARCHAR(255), "
        "email VARCHAR(255) NULL, address VARCHAR(255) NULL)"
    )
    conn.commit()
    conn.close()
