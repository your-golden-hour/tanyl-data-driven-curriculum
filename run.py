"""Точка входа: python run.py  →  http://localhost:8000"""
import os

from app.web import app

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        debug=os.getenv("DEBUG", "0") == "1",
    )
