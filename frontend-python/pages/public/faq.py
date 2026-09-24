"""
NP POWER TECH SOLAR - FAQ Page
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/faq")
def faq_page():
    public_layout(current_page="/faq")

    with ui.column().classes("w-full max-w-4xl mx-auto px-4 py-8 gap-6"):
        ui.label("Frequently Asked Questions").classes("text-4xl font-bold text-gray-900")

        faqs = [
            ("How much does a solar system cost?", "A typical 3kW residential system costs between ₹1,50,000 - ₹1,80,000 before subsidy. Final cost depends on brand, panels, and inverter choice."),
            ("What is the government subsidy for solar?", "Under PM Surya Ghar scheme, you can get up to ₹78,000 subsidy for residential systems. Actual amounts depend on capacity and current government policies."),
            ("How much roof area is needed?", "Approximately 100 sq. ft. per kW. A 3kW system needs about 300 sq. ft. of shadow-free roof area."),
            ("How long does installation take?", "Typically 3-7 days after site survey, depending on system size and site conditions."),
            ("What is the warranty?", "Panels: 25 years performance warranty. Inverter: 5-10 years. Workmanship: 5 years."),
            ("Do you provide AMC?", "Yes, we offer annual maintenance contracts starting from ₹3,000/year."),
            ("Can I get a loan for solar?", "Yes, many banks offer solar loans at attractive interest rates. We can help with documentation."),
            ("What is net metering?", "Net metering lets you export excess solar power to the grid and get credit on your bill."),
        ]

        for q, a in faqs:
            with ui.expansion(q).classes("w-full border rounded"):
                ui.label(a).classes("text-gray-600 p-3")