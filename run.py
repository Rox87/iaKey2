import uvicorn
import sys
import os

# pythonw define sys.stdout e sys.stderr como None, quebrando o Uvicorn.
# Redirecionamos para um arquivo de log para evitar o crash e permitir depuração:
if sys.stdout is None:
    sys.stdout = open("uvicorn_out.log", "a", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open("uvicorn_err.log", "a", encoding="utf-8")

if __name__ == "__main__":
    print("Starting AI Hotkeys App...")
    print("Dashboard available at: http://localhost:8000")
    is_dev = os.environ.get("NO_EDIT_MODE", "false").lower() == "true"
    if is_dev:
        uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=is_dev, log_level="info")        
    else:
        uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
        