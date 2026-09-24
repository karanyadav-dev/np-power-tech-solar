"""
NP POWER TECH SOLAR - Footer Component
Normal flow footer (not fixed) — appears at bottom of content.
"""

from nicegui import ui
from config.settings import settings


def footer():
    """Render the site footer in normal flow (bottom of content)."""

    # Use ui.column (normal flow) — NOT ui.footer (fixed)
    with ui.column().classes("w-full bg-gray-900 text-white py-10 mt-12"):
        with ui.column().classes("w-full max-w-7xl mx-auto px-4 gap-8"):

            # Top section: company + links + contact
            with ui.row().classes("w-full justify-between gap-8 flex-wrap"):

                # Company info
                with ui.column().classes("gap-3 min-w-[250px] flex-1"):
                    with ui.row().classes("items-center gap-2"):
                        ui.icon("solar_power", size="1.8rem").classes("text-yellow-500")
                        ui.label(settings.APP_TITLE).classes("text-xl font-bold text-white")
                    ui.label(
                        "Solar solutions for homes, businesses, and industries."
                    ).classes("text-sm text-gray-400")

                # Quick Links
                with ui.column().classes("gap-2 min-w-[150px]"):
                    ui.label("Quick Links").classes("font-semibold text-white mb-1")
                    ui.link("Home", "/").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("Services", "/services").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("Products", "/products").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("Projects", "/projects").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("Contact", "/contact").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")

                # Services
                with ui.column().classes("gap-2 min-w-[150px]"):
                    ui.label("Services").classes("font-semibold text-white mb-1")
                    ui.link("Residential Solar", "/residential").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("Commercial Solar", "/commercial").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("Industrial Solar", "/industrial").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")
                    ui.link("Solar Calculator", "/calculator").classes("text-gray-400 no-underline hover:text-yellow-500 text-sm")

                # Contact
                with ui.column().classes("gap-2 min-w-[200px]"):
                    ui.label("Contact").classes("font-semibold text-white mb-1")
                    if settings.PUBLIC_COMPANY_PHONE:
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("phone", size="1rem").classes("text-yellow-500")
                            ui.label(settings.PUBLIC_COMPANY_PHONE).classes("text-sm text-gray-400")
                    if settings.PUBLIC_COMPANY_EMAIL:
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("email", size="1rem").classes("text-yellow-500")
                            ui.label(settings.PUBLIC_COMPANY_EMAIL).classes("text-sm text-gray-400")
                    if settings.PUBLIC_COMPANY_ADDRESS:
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("location_on", size="1rem").classes("text-yellow-500")
                            ui.label(settings.PUBLIC_COMPANY_ADDRESS).classes("text-sm text-gray-400")

            # Divider
            ui.separator().classes("bg-gray-700")

            # Bottom row: copyright + legal
            with ui.row().classes("w-full justify-between items-center flex-wrap gap-4"):
                ui.label(f"© 2025 {settings.APP_TITLE}. All rights reserved.").classes(
                    "text-sm text-gray-400"
                )
                with ui.row().classes("gap-4"):
                    ui.link("Privacy Policy", "/privacy-policy").classes(
                        "text-sm text-gray-400 no-underline hover:text-yellow-500"
                    )
                    ui.link("Terms", "/terms").classes(
                        "text-sm text-gray-400 no-underline hover:text-yellow-500"
                    )