"""
NP POWER TECH SOLAR - Footer Component
Logo embedded as base64.
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


def footer():
    """Render the site footer with logo on top, name below."""

    logo_uri = _get_logo_base64()

    company_name = settings_service.get("company_name", settings.APP_TITLE)
    company_phone = settings_service.get("company_phone", settings.PUBLIC_COMPANY_PHONE)
    company_email = settings_service.get("company_email", settings.PUBLIC_COMPANY_EMAIL)
    company_address = settings_service.get("company_address", settings.PUBLIC_COMPANY_ADDRESS)

    with ui.column().classes("w-full bg-gray-900 text-white py-10 mt-12"):
        with ui.column().classes("w-full max-w-7xl mx-auto px-4 gap-8"):
            with ui.row().classes("w-full justify-between gap-12 flex-wrap"):

                # ---------- Column 1: Logo + Name ----------
                with ui.column().classes("gap-3 min-w-[260px]"):
                    if logo_uri:
                        ui.html(
                            f'<img src="{logo_uri}" style="height: 80px; width: auto; background: white; border-radius: 8px; padding: 6px;" alt="NP Power Tech Solar Logo" />'
                        )
                    else:
                        ui.icon("solar_power", size="3rem").classes("text-yellow-500")

                    ui.label(company_name).classes("text-xl font-bold text-white")
                    ui.label("Solar solutions for homes, businesses, and industries.").classes(
                        "text-sm text-gray-400"
                    )

                # ---------- Column 2: Quick Links ----------
                with ui.column().classes("gap-2 min-w-[150px]"):
                    ui.label("Quick Links").classes("text-base font-semibold text-white mb-2")
                    ui.link("Home", "/").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("About", "/about").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("Services", "/services").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("Products", "/products").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("Projects", "/projects").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("Get Quote", "/get-quote").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")

                # ---------- Column 3: Contact ----------
                with ui.column().classes("gap-3 min-w-[280px]"):
                    ui.label("Contact").classes("text-base font-semibold text-white mb-2")

                    if company_phone:
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("phone", size="1rem").classes("text-yellow-500")
                            ui.label(company_phone).classes("text-sm text-gray-400")

                    if company_email:
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("email", size="1rem").classes("text-yellow-500")
                            ui.label(company_email).classes("text-sm text-gray-400")

                    if company_address:
                        with ui.row().classes("items-start gap-2"):
                            ui.icon("location_on", size="1rem").classes("text-yellow-500 mt-1")
                            ui.label(company_address).classes("text-sm text-gray-400")

            ui.separator().classes("bg-gray-700")

            with ui.row().classes(
                "w-full justify-between items-center text-sm text-gray-400 flex-wrap gap-3"
            ):
                ui.label(f"© 2025 {company_name}. All rights reserved.")
                with ui.row().classes("gap-4"):
                    ui.link("Privacy Policy", "/privacy-policy").classes(
                        "text-gray-400 no-underline hover:text-white"
                    )
                    ui.link("Terms", "/terms").classes(
                        "text-gray-400 no-underline hover:text-white"
                    )