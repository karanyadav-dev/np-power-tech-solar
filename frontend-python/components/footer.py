"""
NP POWER TECH SOLAR - Footer Component
Reusable site footer (normal flow, not fixed).
"""

from nicegui import ui
from config.settings import settings


def footer():
    """Render the site footer at the bottom of content (normal flow)."""

    # Normal div (NOT ui.footer) so it flows naturally after content
    with ui.column().classes(
        "w-full bg-gray-900 text-white py-8 mt-12"
    ):
        with ui.column().classes("w-full max-w-7xl mx-auto px-4 gap-6"):
            # Top row
            with ui.row().classes("w-full justify-between gap-8 flex-wrap"):
                # Company info
                with ui.column().classes("gap-2"):
                    ui.label(settings.APP_TITLE).classes("text-xl font-bold")
                    ui.label("Solar solutions for homes, businesses, and industries.").classes(
                        "text-sm text-gray-400"
                    )

                # Quick links
                with ui.column().classes("gap-2"):
                    ui.label("Quick Links").classes("font-semibold")
                    ui.link("Home", "/").classes("text-gray-400 no-underline hover:text-white text-sm")
                    ui.link("Services", "/services").classes("text-gray-400 no-underline hover:text-white text-sm")
                    ui.link("Products", "/products").classes("text-gray-400 no-underline hover:text-white text-sm")
                    ui.link("Contact", "/contact").classes("text-gray-400 no-underline hover:text-white text-sm")

                # Contact info
                with ui.column().classes("gap-2"):
                    ui.label("Contact").classes("font-semibold")
                    if settings.PUBLIC_COMPANY_PHONE:
                        ui.label(f"📞 {settings.PUBLIC_COMPANY_PHONE}").classes("text-sm text-gray-400")
                    if settings.PUBLIC_COMPANY_EMAIL:
                        ui.label(f"✉️ {settings.PUBLIC_COMPANY_EMAIL}").classes("text-sm text-gray-400")
                    if settings.PUBLIC_COMPANY_ADDRESS:
                        ui.label(f"📍 {settings.PUBLIC_COMPANY_ADDRESS}").classes("text-sm text-gray-400")

            # Divider
            ui.separator().classes("bg-gray-700")

            # Bottom row
            with ui.row().classes("w-full justify-between items-center text-sm text-gray-400"):
                ui.label(f"© 2025 {settings.APP_TITLE}. All rights reserved.")
                with ui.row().classes("gap-4"):
                    ui.link("Privacy Policy", "/privacy-policy").classes("text-gray-400 no-underline hover:text-white")
                    ui.link("Terms", "/terms").classes("text-gray-400 no-underline hover:text-white")
                    ui.link("Refund Policy", "/refund-policy").classes("text-gray-400 no-underline hover:text-white")