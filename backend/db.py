import sqlite3
import os
import keyring

DB_PATH = os.path.join(os.path.dirname(__file__), "config.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    # Create models table
    # id, name, base_url, model_name
    c.execute('''
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            base_url TEXT NOT NULL,
            model_name TEXT NOT NULL
        )
    ''')

    # Create hotkeys table
    # id, keys, prefix, model_id
    c.execute('''
        CREATE TABLE IF NOT EXISTS hotkeys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keys TEXT NOT NULL,
            prefix TEXT NOT NULL,
            model_id INTEGER NOT NULL,
            FOREIGN KEY (model_id) REFERENCES models (id)
        )
    ''')
    conn.commit()
    conn.close()

# Keyring wrapper functions
def set_api_key(model_id, api_key):
    keyring.set_password('ai_hotkeys_app', str(model_id), api_key)

def get_api_key(model_id):
    return keyring.get_password('ai_hotkeys_app', str(model_id))

def delete_api_key(model_id):
    try:
        keyring.delete_password('ai_hotkeys_app', str(model_id))
    except keyring.errors.PasswordDeleteError:
        pass

if __name__ == "__main__":
    init_db()
