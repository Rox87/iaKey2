import uvicorn
<<<<<<< HEAD
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
    print("Dashboard available at: http://localhost:8001")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8001, reload=False)
        
=======
import os

def main():
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8002))
    print(f"Starting AI Hotkeys App...")
    print(f"Dashboard available at: http://{host}:{port}")
    uvicorn.run("backend.main:app", host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()

>>>>>>> main
