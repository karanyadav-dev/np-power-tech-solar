"""
NP POWER TECH SOLAR - WhatsApp Floating Button
"""

from nicegui import ui
from config.settings import settings


def whatsapp_button(phone: str = None, message: str = "Hi, I'm interested in solar panels"):
    """Floating WhatsApp button — bottom right corner."""
    phone_number = phone or settings.PUBLIC_COMPANY_WHATSAPP or "919999999999"
    # Clean phone (remove spaces, +, dashes)
    clean_phone = "".join(c for c in phone_number if c.isdigit())
    encoded_msg = message.replace(" ", "%20")

    with ui.element("a").props(
        f'href="https://wa.me/{clean_phone}?text={encoded_msg}" target="_blank"'
    ).classes(
        "fixed bottom-6 right-6 z-50 bg-green-500 hover:bg-green-600 "
        "text-white rounded-full p-4 shadow-lg transition-all duration-200 "
        "flex items-center gap-2 no-underline"
    ):
        ui.icon("chat", size="1.8rem")