"""
NP POWER TECH SOLAR - Services Page
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/services")
def services_page():
    public_layout(current_page="/services")

    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-8"):
        ui.label("Our Services").classes("text-4xl font-bold text-gray-900")
        ui.label("Complete solar solutions for every need.").classes("text-gray-600")

        services = [
            {
                "icon": "home",
                "title": "Residential Solar",
                "desc": "Rooftop solar systems for homes — 1kW to 10kW. Reduce your electricity bill by up to 90%.",
                "price": "Starting from ₹45,000",
            },
            {
                "icon": "business",
                "title": "Commercial Solar",
                "desc": "Solar for offices, shops, and commercial buildings. Tax benefits under accelerated depreciation.",
                "price": "Custom quotes",
            },
            {
                "icon": "factory",
                "title": "Industrial Solar",
                "desc": "Large-scale solar plants for factories and industries. High ROI, quick payback.",
                "price": "Custom quotes",
            },
            {
                "icon": "water_drop",
                "title": "Solar Water Heater",
                "desc": "Efficient solar water heating solutions for homes and commercial establishments.",
                "price": "Starting from ₹18,000",
            },
            {
                "icon": "battery_charging_full",
                "title": "Battery & Storage",
                "desc": "On-grid, off-grid, and hybrid systems with battery backup options.",
                "price": "Custom quotes",
            },
            {
                "icon": "build",
                "title": "AMC & Maintenance",
                "desc": "Annual maintenance contracts to keep your solar system running at peak efficiency.",
                "price": "From ₹3,000/year",
            },
        ]

        with ui.row().classes("w-full gap-6 flex-wrap"):
            for s in services:
                with ui.card().classes("w-full md:w-96 p-6 hover:shadow-lg transition-shadow"):
                    ui.icon(s["icon"], size="3rem").classes("text-yellow-500")
                    ui.label(s["title"]).classes("text-xl font-bold text-gray-900 mt-3")
                    ui.label(s["desc"]).classes("text-gray-600 mt-2")
                    ui.label(s["price"]).classes("text-sm font-semibold text-green-600 mt-3")

                    ui.button(
                        "Get Quote",
                        on_click=lambda: ui.navigate.to("/get-quote"),
                    ).classes("bg-yellow-500 text-white mt-3")