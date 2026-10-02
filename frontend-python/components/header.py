"""
NP POWER TECH SOLAR - Header Component
Logo embedded as base64 (no path issues).
"""

import base64
from pathlib import Path
from nicegui import ui
from config.settings import settings
from services.settings_service import settings_service


def _get_logo_base64():
    """Read logo file and convert to base64 data URI."""
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
    if logo_path.exists():
        try:
            with open(logo_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{b64}"
        except Exception:
            return None
    return None


def header(current_page: str = "/"):
    """Render the site header with logo on left."""

    logo_uri = _get_logo_base64()

    with ui.header().classes("bg-white shadow-md py-3"):
        with ui.row().classes(
            "w-full max-w-7xl mx-auto items-center justify-between px-4 gap-4"
        ):
            # ---------- Logo + Brand (left) ----------
            with ui.row().classes("items-center gap-3 cursor-pointer shrink-0").on(
                "click", lambda: ui.navigate.to("/")
            ):
                if logo_uri:
                    ui.html(
                        f'<img src="{logo_uri}" style="height: 56px; width: auto;" alt="NP Power Tech Solar Logo" />'
                    )
                else:
                    ui.icon("solar_power", size="2.5rem").classes("text-yellow-500")

                company_name = settings_service.get("company_name", settings.APP_TITLE)
                ui.label(company_name).classes(
                    "text-lg md:text-xl font-bold text-gray-800"
                )

            # ---------- Navigation (right) ----------
            with ui.row().classes("gap-5 items-center"):
                nav_links = [
                    ("Home", "/"),
                    ("About", "/about"),
                    ("Services", "/services"),
                    ("Products", "/products"),
                    ("Projects", "/projects"),
                    ("Calculator", "/calculator"),
                    ("FAQ", "/faq"),
                    ("Contact", "/contact"),
                ]

                for label, path in nav_links:
                    is_active = current_page == path
                    classes = "text-gray-800 font-medium no-underline hover:text-yellow-600 text-sm"
                    if is_active:
                        classes += " border-b-2 border-yellow-500 pb-1"

                    ui.link(label, path).classes(classes)

                ui.button(
                    "Get Quote",
                    on_click=lambda: ui.navigate.to("/get-quote"),
                ).classes("bg-yellow-500 text-white font-semibold ml-2")