"""
NP POWER TECH SOLAR - Floating Call Button
"""

from nicegui import ui
from config.settings import settings


def call_button(phone: str = None):
    """Floating call button — bottom-left corner."""
    phone_number = phone or settings.PUBLIC_COMPANY_PHONE or "+9196109 91048"
    clean_phone = "".join(c for c in phone_number if c.isdigit() or c == "+")

    with ui.element("a").props(f'href="tel:{clean_phone}"').classes(
        "fixed bottom-6 left-6 z-50 bg-blue-500 hover:bg-blue-600 "
        "text-white rounded-full p-4 shadow-lg transition-all duration-200 "
        "flex items-center gap-2 no-underline"
    ):
        ui.icon("phone", size="1.8rem")