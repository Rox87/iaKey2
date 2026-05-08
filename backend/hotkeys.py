import keyboard
import pyperclip
import time
import threading
from openai import OpenAI
from . import db

# To ensure smooth replacement
DELAY_AFTER_COPY = 0.2
DELAY_AFTER_PASTE = 0.2

active_hotkeys = {}

def process_ai_request(text: str, prefix: str, model_info: dict, api_key: str):
    try:
        client = OpenAI(
            base_url=model_info['base_url'],
            api_key=api_key,
            max_retries=1
        )
        prompt = f"{prefix}\n\n{text}"
        response = client.chat.completions.create(
            model=model_info['model_name'],
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in AI request: {e}")
        return "Request Fail"


def hotkey_callback(hotkey_config):
    # Simulate copy (Ctrl+C/Cmd+C)
    # Using Ctrl+X since user wanted to "recortar"
    keyboard.send('ctrl+x')
    time.sleep(DELAY_AFTER_COPY)

    # Get text from clipboard
    copied_text = pyperclip.paste()

    if not copied_text.strip():
        return

    # Paste "Processando..."
    pyperclip.copy("Processando...")
    keyboard.send('ctrl+v')
    time.sleep(DELAY_AFTER_PASTE)

    # Run API request in a separate thread so we don't block the listener
    def run_request():
        conn = db.get_db()
        c = conn.cursor()
        c.execute("SELECT id, name, base_url, model_name FROM models WHERE id = ?", (hotkey_config['model_id'],))
        model_info = c.fetchone()
        conn.close()

        if not model_info:
            result = "Request Fail"
        else:
            api_key = db.get_api_key(model_info['id'])
            if not api_key:
                result = "Request Fail"
            else:
                result = process_ai_request(copied_text, hotkey_config['prefix'], dict(model_info), api_key)

        # Paste result
        pyperclip.copy(result)
        keyboard.send('ctrl+v')

    threading.Thread(target=run_request).start()


def reload_hotkeys():
    global active_hotkeys

    # Remove existing
    for hk, handler in active_hotkeys.items():
        try:
            keyboard.remove_hotkey(handler)
        except KeyError:
            pass

    active_hotkeys.clear()

    conn = db.get_db()
    c = conn.cursor()
    c.execute("SELECT id, keys, prefix, model_id FROM hotkeys")
    hotkeys = [dict(row) for row in c.fetchall()]
    conn.close()

    for hk in hotkeys:
        keys_combo = hk['keys']
        # Bind hotkey dynamically
        # Need to capture the loop variable correctly
        handler = keyboard.add_hotkey(keys_combo, lambda config=hk: hotkey_callback(config))
        active_hotkeys[keys_combo] = handler
        print(f"Registered hotkey: {keys_combo}")

def start_listener():
    reload_hotkeys()
    # keyboard listener runs in background automatically after add_hotkey
