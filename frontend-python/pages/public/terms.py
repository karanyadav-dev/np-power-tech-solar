"""
NP POWER TECH SOLAR - Terms of Service
"""

from nicegui import ui
from layouts.public_layout import public_layout
from config.settings import settings


@ui.page("/terms")
def terms_page():
    public_layout(current_page="/terms")

    with ui.column().classes("w-full max-w-4xl mx-auto px-4 py-8 gap-6"):
        ui.label("Terms of Service").classes("text-4xl font-bold text-gray-900")
        ui.label("Last updated: September 2025").classes("text-sm text-gray-500")

        sections = [
            ("1. Acceptance of Terms", f"By accessing or using {settings.APP_TITLE} website and services, you agree to be bound by these Terms of Service. If you disagree, please do not use our services."),
            ("2. Services", "We provide solar system consulting, site survey, quotation, installation, and after-sales support. All services are subject to availability and site feasibility."),
            ("3. Quotations", "All quotations are estimates based on the information provided and initial site assessment. Final pricing is confirmed only after:\n\n• Site survey completion\n• Final system configuration\n• Customer approval\n\nQuotations are valid for 30 days unless otherwise stated."),
            ("4. Government Subsidy", "Subsidy amounts mentioned on our website are indicative and based on current government schemes. Actual subsidy is subject to:\n\n• Eligibility criteria\n• Scheme availability\n• DISCOM approval\n• Timely application processing\n\nWe assist with applications but do not guarantee approval or timeline."),
            ("5. Orders and Payment", "Orders are confirmed only after receipt of advance payment as specified in the quotation. Payment terms are clearly stated in each quotation."),
            ("6. Installation", "Installation timelines are estimates. Delays may occur due to weather, material availability, DISCOM approvals, or site conditions. We will keep you informed of any changes."),
            ("7. Warranty", "Product warranties are provided by manufacturers. Installation warranty covers workmanship for the specified period. Warranty does not cover:\n\n• Physical damage\n• Misuse or negligence\n• Force majeure events\n• Unauthorized modifications"),
            ("8. AMC (Annual Maintenance Contract)", "AMC contracts are optional and separate from the initial purchase. Terms of AMC are provided separately at the time of enrollment."),
            ("9. Intellectual Property", "All content on this website — text, graphics, logos, images — is our property or that of our licensors and is protected by copyright laws."),
            ("10. Limitation of Liability", "Our total liability for any claim is limited to the amount paid by you for the specific service. We are not liable for indirect, incidental, or consequential damages."),
            ("11. Cancellation", "Order cancellation is subject to our refund policy. Cancellation after material procurement may attract charges."),
            ("12. Force Majeure", "We are not liable for delays or failures caused by events beyond our control — natural disasters, strikes, government actions, pandemics, etc."),
            ("13. Governing Law", "These terms are governed by Indian law. Disputes are subject to the exclusive jurisdiction of courts in the location of our registered office."),
            ("14. Changes to Terms", "We may modify these Terms at any time. Continued use of our services after changes constitutes acceptance."),
            ("15. Contact", f"For questions about these Terms:\n\nEmail: {settings.PUBLIC_COMPANY_EMAIL or 'contact@example.com'}\nPhone: {settings.PUBLIC_COMPANY_PHONE or '+91-XXXX-XXXXXX'}"),
        ]

        for title, content in sections:
            with ui.card().classes("w-full p-6"):
                ui.label(title).classes("text-xl font-bold text-gray-900")
                ui.label(content).classes("text-gray-700 mt-2 whitespace-pre-line")

        ui.separator()
        ui.link("← Back to Home", "/").classes("text-yellow-600 font-semibold")