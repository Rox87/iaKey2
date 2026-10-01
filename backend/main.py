from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
from . import db

app = FastAPI()

# Providers
class ProviderCreate(BaseModel):
    name: str
    base_url: str
    api_key: str

class ProviderResponse(BaseModel):
    id: int
    name: str
    base_url: str

# Models
class ModelCreate(BaseModel):
    name: str
    provider_id: int
    model_name: str

class ModelResponse(BaseModel):
    id: int
    name: str
    provider_id: int
    model_name: str

class HotkeyCreate(BaseModel):
    keys: str
    prefix: str
    model_id: int

class HotkeyResponse(BaseModel):
    id: int
    keys: str
    prefix: str
    model_id: int

# Ensure DB is initialized
db.init_db()

# --- API Endpoints ---

@app.get("/api/providers", response_model=List[ProviderResponse])
def get_providers():
    conn = db.get_db()
    c = conn.cursor()
    c.execute("SELECT id, name, base_url FROM providers")
    providers = [dict(row) for row in c.fetchall()]
    conn.close()
    return providers

@app.post("/api/providers", response_model=ProviderResponse)
def create_provider(provider: ProviderCreate):
    conn = db.get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO providers (name, base_url) VALUES (?, ?)",
        (provider.name, provider.base_url)
    )
    conn.commit()
    provider_id = c.lastrowid
    conn.close()

    db.set_api_key(provider_id, provider.api_key)

    return {
        "id": provider_id,
        "name": provider.name,
        "base_url": provider.base_url
    }

@app.delete("/api/providers/{provider_id}")
def delete_provider(provider_id: int):
    conn = db.get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as count FROM models WHERE provider_id = ?", (provider_id,))
    if c.fetchone()['count'] > 0:
        conn.close()
        raise HTTPException(status_code=400, detail="Cannot delete provider, it is used by models.")

    c.execute("DELETE FROM providers WHERE id = ?", (provider_id,))
    conn.commit()
    conn.close()

    db.delete_api_key(provider_id)
    return {"status": "success"}

@app.get("/api/models", response_model=List[ModelResponse])
def get_models():
    conn = db.get_db()
    c = conn.cursor()
    c.execute("SELECT id, name, provider_id, model_name FROM models")
    models = [dict(row) for row in c.fetchall()]
    conn.close()
    return models

@app.post("/api/models", response_model=ModelResponse)
def create_model(model: ModelCreate):
    conn = db.get_db()
    c = conn.cursor()
    c.execute("PRAGMA table_info(models)")
    cols = [r['name'] for r in c.fetchall()]
    
    if 'base_url' in cols:
        c.execute(
            "INSERT INTO models (name, provider_id, model_name, base_url) VALUES (?, ?, ?, '')",
            (model.name, model.provider_id, model.model_name)
        )
    else:
        c.execute(
            "INSERT INTO models (name, provider_id, model_name) VALUES (?, ?, ?)",
            (model.name, model.provider_id, model.model_name)
        )
    conn.commit()
    model_id = c.lastrowid
    conn.close()

    return {
        "id": model_id,
        "name": model.name,
        "provider_id": model.provider_id,
        "model_name": model.model_name
    }

@app.delete("/api/models/{model_id}")
def delete_model(model_id: int):
    conn = db.get_db()
    c = conn.cursor()
    # Check if used by hotkeys
    c.execute("SELECT COUNT(*) as count FROM hotkeys WHERE model_id = ?", (model_id,))
    if c.fetchone()['count'] > 0:
        conn.close()
        raise HTTPException(status_code=400, detail="Cannot delete model, it is used by hotkeys.")

    c.execute("DELETE FROM models WHERE id = ?", (model_id,))
    conn.commit()
    conn.close()

    return {"status": "success"}

@app.get("/api/hotkeys", response_model=List[HotkeyResponse])
def get_hotkeys():
    conn = db.get_db()
    c = conn.cursor()
    c.execute("SELECT id, keys, prefix, model_id FROM hotkeys")
    hotkeys = [dict(row) for row in c.fetchall()]
    conn.close()
    return hotkeys

@app.post("/api/hotkeys", response_model=HotkeyResponse)
def create_hotkey(hotkey: HotkeyCreate):
    conn = db.get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO hotkeys (keys, prefix, model_id) VALUES (?, ?, ?)",
        (hotkey.keys, hotkey.prefix, hotkey.model_id)
    )
    conn.commit()
    hotkey_id = c.lastrowid
    conn.close()

    # We should reload the hotkeys in the background thread here
    # This will be implemented when we wire up the hotkey listener
    from . import hotkeys as hk
    if hasattr(hk, 'reload_hotkeys'):
        hk.reload_hotkeys()

    return {
        "id": hotkey_id,
        "keys": hotkey.keys,
        "prefix": hotkey.prefix,
        "model_id": hotkey.model_id
    }

@app.delete("/api/hotkeys/{hotkey_id}")
def delete_hotkey(hotkey_id: int):
    conn = db.get_db()
    c = conn.cursor()
    c.execute("DELETE FROM hotkeys WHERE id = ?", (hotkey_id,))
    conn.commit()
    conn.close()

    # We should reload the hotkeys in the background thread here
    from . import hotkeys as hk
    if hasattr(hk, 'reload_hotkeys'):
        hk.reload_hotkeys()

    return {"status": "success"}

# --- Static Files ---
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if not os.path.exists(frontend_dir):
    os.makedirs(frontend_dir)
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

@app.on_event("startup")
def startup_event():
    from . import hotkeys as hk
    hk.start_listener()
