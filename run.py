import uvicorn
import os

def main():
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8002))
    print(f"Starting AI Hotkeys App...")
    print(f"Dashboard available at: http://{host}:{port}")
    uvicorn.run("backend.main:app", host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()

