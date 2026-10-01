import uvicorn
import sys
import os

if __name__ == "__main__":
    print("Starting AI Hotkeys App...")
    print("Dashboard available at: http://localhost:8000")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, log_level="info")