"""
NP POWER TECH SOLAR - Privacy Policy
"""

from nicegui import ui
from layouts.public_layout import public_layout
from config.settings import settings


@ui.page("/privacy-policy")
def privacy_policy_page():
    public_layout(current_page="/privacy-policy")

    with ui.column().classes("w-full max-w-4xl mx-auto px-4 py-8 gap-6"):
        ui.label("Privacy Policy").classes("text-4xl font-bold text-gray-900")
        ui.label("Last updated: September 2025").classes("text-sm text-gray-500")

        sections = [
            ("1. Introduction", f"{settings.APP_TITLE} ('we', 'our', 'us') is committed to protecting your privacy. This Privacy Policy explains how we collect, use, and safeguard your information when you visit our website or use our services."),
            ("2. Information We Collect", "We may collect the following information:\n\n• Personal details: Name, phone number, email, address, pincode\n• Electricity information: Monthly bill, consumption, DISCOM name\n• Site information: Roof area, photos, installation address\n• Device information: IP address, browser type, pages visited\n• Cookies and similar technologies"),
            ("3. How We Use Your Information", "We use your information to:\n\n• Provide solar quotations and site surveys\n• Process orders and schedule installations\n• Apply for government subsidies on your behalf\n• Send service notifications and updates\n• Improve our website and services\n• Comply with legal requirements"),
            ("4. Information Sharing", "We do NOT sell your personal information. We may share information with:\n\n• Installation partners and technicians (for service delivery)\n• Government agencies (for subsidy processing)\n• Payment gateways (for transaction processing)\n• Legal authorities (when required by law)"),
            ("5. Data Security", "We implement industry-standard security measures including encryption, secure servers, and access controls. However, no method of transmission over the internet is 100% secure."),
            ("6. Cookies", "We use cookies to improve your browsing experience and analyze website traffic. You can disable cookies in your browser settings, but this may affect site functionality."),
            ("7. Your Rights", "You have the right to:\n\n• Access your personal data\n• Correct inaccurate information\n• Request deletion of your data\n• Opt-out of marketing communications\n• File a complaint with data protection authorities"),
            ("8. Data Retention", "We retain your data as long as necessary to provide services and comply with legal obligations. After this period, your data is securely deleted."),
            ("9. Children's Privacy", "Our services are not intended for individuals under 18. We do not knowingly collect data from children."),
            ("10. Changes to This Policy", "We may update this Privacy Policy periodically. Changes will be posted on this page with an updated date."),
            ("11. Contact Us", f"For privacy-related questions:\n\nEmail: {settings.PUBLIC_COMPANY_EMAIL or 'contact@example.com'}\nPhone: {settings.PUBLIC_COMPANY_PHONE or '+91-XXXX-XXXXXX'}\nAddress: {settings.PUBLIC_COMPANY_ADDRESS or 'India'}"),
        ]

        for title, content in sections:
            with ui.card().classes("w-full p-6"):
                ui.label(title).classes("text-xl font-bold text-gray-900")
                ui.label(content).classes("text-gray-700 mt-2 whitespace-pre-line")

        ui.separator()
        ui.link("← Back to Home", "/").classes("text-yellow-600 font-semibold")