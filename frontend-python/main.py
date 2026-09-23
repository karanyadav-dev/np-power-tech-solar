"""
NP POWER TECH SOLAR - Frontend launcher.
Alternative entry point (mirrors app.py).
"""

from app import APP_TITLE, APP_HOST, APP_PORT  # noqa: F401
from nicegui import ui

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host=APP_HOST,
        port=APP_PORT,
        title=APP_TITLE,
        favicon="☀️",
        reload=False,
        show=False,
    )