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
    # Create providers table
    c.execute('''
        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            base_url TEXT NOT NULL
        )
    ''')

    # Create models table
    # id, name, provider_id, model_name
    c.execute('''
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            provider_id INTEGER NOT NULL,
            model_name TEXT NOT NULL,
            FOREIGN KEY (provider_id) REFERENCES providers (id)
        )
    ''')
    
    # Try to add provider_id in case the table already exists from an older version
    try:
        c.execute('ALTER TABLE models ADD COLUMN provider_id INTEGER NOT NULL DEFAULT 0')
    except sqlite3.OperationalError:
        pass

    # Create hotkeys table
    # id, keys, prefix, model_id, description
    c.execute('''
        CREATE TABLE IF NOT EXISTS hotkeys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keys TEXT NOT NULL,
            prefix TEXT NOT NULL,
            model_id INTEGER NOT NULL,
            description TEXT,
            FOREIGN KEY (model_id) REFERENCES models (id)
        )
    ''')
    
    try:
        c.execute('ALTER TABLE hotkeys ADD COLUMN description TEXT DEFAULT ""')
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

# Keyring wrapper functions
def set_api_key(provider_id, api_key):
    keyring.set_password('ai_hotkeys_app_prov', str(provider_id), api_key)

def get_api_key(provider_id):
    return keyring.get_password('ai_hotkeys_app_prov', str(provider_id))

def delete_api_key(provider_id):
    try:
        keyring.delete_password('ai_hotkeys_app_prov', str(provider_id))
    except keyring.errors.PasswordDeleteError:
        pass

if __name__ == "__main__":
    init_db()
