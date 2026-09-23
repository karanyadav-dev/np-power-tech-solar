"""
NP POWER TECH SOLAR - Python + NiceGUI Frontend
Main application entry point.

Run: python app.py
"""

from nicegui import ui

# Import pages (they register routes via @ui.page)
from pages.public import home  # noqa: F401

# Import config
from config.settings import settings


# ---------- Additional placeholder routes ----------
@ui.page("/services")
def services():
    from layouts.public_layout import public_layout
    public_layout(current_page="/services")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Our Services").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")


@ui.page("/products")
def products():
    from layouts.public_layout import public_layout
    public_layout(current_page="/products")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Our Products").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")


@ui.page("/projects")
def projects():
    from layouts.public_layout import public_layout
    public_layout(current_page="/projects")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Our Projects").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")


@ui.page("/calculator")
def calculator():
    from layouts.public_layout import public_layout
    public_layout(current_page="/calculator")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Solar Calculator").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")


@ui.page("/contact")
def contact():
    from layouts.public_layout import public_layout
    public_layout(current_page="/contact")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Contact Us").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")


@ui.page("/get-quote")
def get_quote():
    from layouts.public_layout import public_layout
    public_layout(current_page="/get-quote")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Get a Quote").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")


@ui.page("/site-survey")
def site_survey():
    from layouts.public_layout import public_layout
    public_layout(current_page="/site-survey")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Book Site Survey").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")


# ---------- Run ----------
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        title=settings.APP_TITLE,
        favicon="☀️",
        reload=False,
        show=False,
    )