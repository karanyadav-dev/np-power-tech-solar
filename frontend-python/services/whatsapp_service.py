"""
NP POWER TECH SOLAR - WhatsApp Service
Generates WhatsApp deep links for sending PDFs and messages.
"""

from config.settings import settings
from typing import Optional


class WhatsAppService:
    """Generate WhatsApp deep links."""

    @staticmethod
    def _clean_phone(phone: str) -> str:
        """Convert phone to WhatsApp format (country code, no symbols)."""
        digits = "".join(c for c in phone if c.isdigit())
        # If starts with 0, remove it
        if digits.startswith("0"):
            digits = digits[1:]
        # If 10 digits, add 91 (India)
        if len(digits) == 10:
            digits = "91" + digits
        return digits

    @staticmethod
    def send_quotation_pdf(phone: str, quotation_number: str, pdf_url: str, amount: float = None):
        """Generate WhatsApp link to send quotation PDF."""
        clean = WhatsAppService._clean_phone(phone)

        message = (
            f"Namaste! 🙏\n\n"
            f"Aapki solar quotation ready hai.\n\n"
            f"📋 Quotation No: {quotation_number}\n"
        )
        if amount:
            message += f"💰 Final Amount: ₹{amount:,.0f}\n"

        message += (
            f"\n📄 PDF Download: {pdf_url}\n\n"
            f"Koi bhi sawaal ho toh reply karein.\n\n"
            f"🙏 {settings.APP_TITLE}\n"
            f"📞 {settings.PUBLIC_COMPANY_PHONE}"
        )

        encoded = message.replace(" ", "%20").replace("\n", "%0A")
        return f"https://wa.me/{clean}?text={encoded}"

    @staticmethod
    def send_custom(phone: str, message: str):
        """Send custom WhatsApp message."""
        clean = WhatsAppService._clean_phone(phone)
        encoded = message.replace(" ", "%20").replace("\n", "%0A")
        return f"https://wa.me/{clean}?text={encoded}"

    @staticmethod
    def contact_us():
        """Contact the company via WhatsApp."""
        phone = settings.PUBLIC_COMPANY_WHATSAPP or settings.PUBLIC_COMPANY_PHONE
        clean = WhatsAppService._clean_phone(phone)
        message = "Namaste! Mujhe solar panel ke baare mein jaankari chahiye."
        encoded = message.replace(" ", "%20")
        return f"https://wa.me/{clean}?text={encoded}"


whatsapp_service = WhatsAppService()