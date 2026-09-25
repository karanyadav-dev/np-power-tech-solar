"""
NP POWER TECH SOLAR - Header Component (Dynamic)
Navigation header with settings-driven company name.
"""

from nicegui import ui
from config.settings import settings
from services.settings_service import settings_service


def header(current_page: str = "/"):
    """Render the site header with dynamic company name."""

    # Get company name from settings (with .env fallback)
    company_name = settings_service.get("company_name", settings.APP_TITLE)

    with ui.header().classes("bg-white shadow-md py-2 z-50"):
        with ui.row().classes("w-full max-w-7xl mx-auto items-center justify-between px-4"):
            # Logo / Brand (clickable)
            with ui.row().classes("items-center gap-2 cursor-pointer").on(
                "click", lambda: ui.navigate.to("/")
            ):
                ui.icon("solar_power", size="2rem").classes("text-yellow-500")
                ui.label(company_name).classes("text-xl font-bold text-gray-800")

            # Navigation Links
            with ui.row().classes("gap-6 items-center"):
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
                    classes = "text-gray-800 font-medium no-underline hover:text-yellow-600"
                    if is_active:
                        classes += " border-b-2 border-yellow-500"

                    ui.link(label, path).classes(classes)

                # Login/Get Quote button
                ui.button(
                    "Get Quote",
                    on_click=lambda: ui.navigate.to("/get-quote"),
                ).classes("bg-yellow-500 text-white font-semibold")

            # Mobile Menu Button (optional)
            with ui.row().classes("md:hidden"):
                ui.button(icon="menu").props("flat")