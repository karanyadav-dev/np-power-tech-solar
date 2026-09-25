"""
NP POWER TECH SOLAR - Footer Component (Dynamic)
"""

from nicegui import ui
from config.settings import settings
from services.settings_service import settings_service


def footer():
    """Render footer with dynamic settings."""

    company_name = settings_service.get("company_name", settings.APP_TITLE)
    company_phone = settings_service.get("company_phone", settings.PUBLIC_COMPANY_PHONE)
    company_email = settings_service.get("company_email", settings.PUBLIC_COMPANY_EMAIL)
    company_address = settings_service.get("company_address", settings.PUBLIC_COMPANY_ADDRESS)

    with ui.column().classes("w-full bg-gray-900 text-white py-8 mt-12"):
        with ui.column().classes("w-full max-w-7xl mx-auto px-4 gap-6"):
            with ui.row().classes("w-full justify-between gap-8 flex-wrap"):
                with ui.column().classes("gap-2"):
                    ui.label(company_name).classes("text-xl font-bold")
                    ui.label("Solar solutions for homes, businesses, and industries.").classes(
                        "text-sm text-gray-400"
                    )

                with ui.column().classes("gap-2"):
                    ui.label("Quick Links").classes("font-semibold")
                    ui.link("Home", "/").classes("text-gray-400 no-underline hover:text-white text-sm")
                    ui.link("Services", "/services").classes("text-gray-400 no-underline hover:text-white text-sm")
                    ui.link("Products", "/products").classes("text-gray-400 no-underline hover:text-white text-sm")
                    ui.link("Contact", "/contact").classes("text-gray-400 no-underline hover:text-white text-sm")
                    ui.link("Get Quote", "/get-quote").classes("text-gray-400 no-underline hover:text-white text-sm")

                with ui.column().classes("gap-2"):
                    ui.label("Contact").classes("font-semibold")
                    if company_phone:
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("phone", size="1rem").classes("text-yellow-500")
                            ui.label(company_phone).classes("text-sm text-gray-400")
                    if company_email:
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("email", size="1rem").classes("text-yellow-500")
                            ui.label(company_email).classes("text-sm text-gray-400")
                    if company_address:
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("location_on", size="1rem").classes("text-yellow-500")
                            ui.label(company_address).classes("text-sm text-gray-400")

            ui.separator().classes("bg-gray-700")

            with ui.row().classes("w-full justify-between items-center text-sm text-gray-400 flex-wrap"):
                ui.label(f"© 2025 {company_name}. All rights reserved.")
                with ui.row().classes("gap-4"):
                    ui.link("Privacy Policy", "/privacy-policy").classes("text-gray-400 no-underline hover:text-white")
                    ui.link("Terms", "/terms").classes("text-gray-400 no-underline hover:text-white")