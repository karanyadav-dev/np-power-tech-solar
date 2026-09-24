"""
NP POWER TECH SOLAR - Footer Component
Reusable site footer (always at bottom of page).
"""

from nicegui import ui
from config.settings import settings


def footer():
    """Render the site footer at the bottom of content."""

    # Use normal flow — footer at end of content, page min-height ensures bottom
    with ui.element("footer").classes(
        "w-full bg-gray-900 text-white py-8 mt-auto"
    ):
        with ui.column().classes("w-full max-w-7xl mx-auto px-4 gap-6"):
            # Top row
            with ui.row().classes("w-full justify-between gap-8 flex-wrap"):
                # Company info
                with ui.column().classes("gap-2 max-w-md"):
                    ui.label(settings.APP_TITLE).classes("text-xl font-bold")
                    ui.label(
                        "Solar solutions for homes, businesses, and industries."
                    ).classes("text-sm text-gray-400")

                # Quick links
                with ui.column().classes("gap-2"):
                    ui.label("Quick Links").classes("font-semibold text-white")
                    ui.link("Home", "/").classes("text-gray-400 no-underline hover:text-white text-sm")
                    ui.link("About", "/about").classes("text-gray-400 no-underline hover:text-white text-sm")
                    ui.link("Services", "/services").classes("text-gray-400 no-underline hover:text-white text-sm")
                    ui.link("Products", "/products").classes("text-gray-400 no-underline hover:text-white text-sm")
                    ui.link("Contact", "/contact").classes("text-gray-400 no-underline hover:text-white text-sm")

                # Contact info
                with ui.column().classes("gap-2"):
                    ui.label("Contact").classes("font-semibold text-white")
                    with ui.row().classes("items-center gap-2"):
                        ui.icon("phone", size="1rem").classes("text-yellow-500")
                        ui.label(
                            settings.PUBLIC_COMPANY_PHONE or "+91-XXXX-XXXXXX"
                        ).classes("text-sm text-gray-400")
                    with ui.row().classes("items-center gap-2"):
                        ui.icon("email", size="1rem").classes("text-yellow-500")
                        ui.label(
                            settings.PUBLIC_COMPANY_EMAIL or "contact@nppowertech.com"
                        ).classes("text-sm text-gray-400")

            # Divider
            ui.separator().classes("bg-gray-700")

            # Bottom row
            with ui.row().classes(
                "w-full justify-between items-center text-sm text-gray-400 flex-wrap gap-2"
            ):
                ui.label(f"© 2025 {settings.APP_TITLE}. All rights reserved.")
                with ui.row().classes("gap-4 flex-wrap"):
                    ui.link("Privacy Policy", "/privacy-policy").classes(
                        "text-gray-400 no-underline hover:text-white"
                    )
                    ui.link("Terms", "/terms").classes(
                        "text-gray-400 no-underline hover:text-white"
                    )
                    ui.link("Refund Policy", "/refund-policy").classes(
                        "text-gray-400 no-underline hover:text-white"
                    )