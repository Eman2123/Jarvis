
import sqlite3
import os
from datetime import datetime

# Jarvis project ka main folder
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Database file ka path
DB_PATH = os.path.join(BASE_DIR, "jarvis.db")


def get_connection():
    """Database connection return karega."""
    return sqlite3.connect(DB_PATH)


def create_chat_history_table():
    """Chat history ke tables create karega."""

    with get_connection() as conn:
        cursor = conn.cursor()

        # Conversations ki list
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL DEFAULT 'New Chat',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Har conversation ke messages
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE
            )
        """)

        conn.commit()


def create_conversation(title="New Chat"):
    """Nayi conversation create karke uski ID return karega."""

    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conversations
                (title, created_at, updated_at)
            VALUES (?, ?, ?)
        """, (title, now, now))

        return cursor.lastrowid


def save_chat_message(conversation_id, role, message):
    """User ya Jarvis ka message permanently save karega."""

    if role not in ("user", "assistant"):
        raise ValueError("Role must be user or assistant.")

    if not message or not str(message).strip():
        return False

    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO chat_messages
                (conversation_id, role, message, created_at)
            VALUES (?, ?, ?, ?)
        """, (conversation_id, role, str(message).strip(), now))

        # Conversation ki latest activity update karein
        cursor.execute("""
            UPDATE conversations
            SET updated_at = ?
            WHERE id = ?
        """, (now, conversation_id))

        # Agar title abhi New Chat hai to pehle user message se title banayein
        if role == "user":
            cursor.execute("""
                UPDATE conversations
                SET title = ?
                WHERE id = ? AND title = 'New Chat'
            """, (str(message).strip()[:50], conversation_id))

    return True


def get_all_conversations():
    """Purani conversations latest activity ke hisaab se return karega."""

    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.id,
                c.title,
                c.created_at,
                c.updated_at,
                (
                    SELECT message
                    FROM chat_messages m
                    WHERE m.conversation_id = c.id
                    ORDER BY m.id DESC
                    LIMIT 1
                ) AS last_message
            FROM conversations c
            ORDER BY c.updated_at DESC, c.id DESC
        """)

        return [dict(row) for row in cursor.fetchall()]


def get_conversation_messages(conversation_id):
    """Selected conversation ke tamam messages return karega."""

    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, conversation_id, role, message, created_at
            FROM chat_messages
            WHERE conversation_id = ?
            ORDER BY id ASC
        """, (conversation_id,))

        return [dict(row) for row in cursor.fetchall()]


# Current active conversation
_current_conversation_id = None


def set_current_conversation(conversation_id):
    global _current_conversation_id
    _current_conversation_id = conversation_id


def get_current_conversation():
    return _current_conversation_id


def save_current_message(role, message):
    global _current_conversation_id

    if not message or not str(message).strip():
        return False

    if _current_conversation_id is None:
        _current_conversation_id = create_conversation()

    return save_chat_message(
        _current_conversation_id,
        role,
        message
    )
