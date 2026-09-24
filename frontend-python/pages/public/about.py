"""
NP POWER TECH SOLAR - About Page
"""

from nicegui import ui
from layouts.public_layout import public_layout
from config.settings import settings


@ui.page("/about")
def about_page():
    public_layout(current_page="/about")

    with ui.column().classes("w-full max-w-5xl mx-auto px-4 py-8 gap-8"):
        ui.label("About Us").classes("text-4xl font-bold text-gray-900")
        ui.label(
            f"{settings.APP_TITLE} is committed to making solar energy accessible and affordable "
            "for every home and business."
        ).classes("text-lg text-gray-600")

        with ui.row().classes("w-full gap-6 flex-wrap mt-6"):
            with ui.card().classes("flex-1 min-w-[250px] p-6"):
                ui.icon("flag", size="3rem").classes("text-yellow-500")
                ui.label("Our Mission").classes("text-xl font-bold mt-2")
                ui.label("To accelerate India's transition to clean, renewable energy.").classes("text-gray-600 mt-2")

            with ui.card().classes("flex-1 min-w-[250px] p-6"):
                ui.icon("visibility", size="3rem").classes("text-yellow-500")
                ui.label("Our Vision").classes("text-xl font-bold mt-2")
                ui.label("A future where every rooftop generates clean power.").classes("text-gray-600 mt-2")

            with ui.card().classes("flex-1 min-w-[250px] p-6"):
                ui.icon("handshake", size="3rem").classes("text-yellow-500")
                ui.label("Our Values").classes("text-xl font-bold mt-2")
                ui.label("Integrity, quality, and customer-first service.").classes("text-gray-600 mt-2")

        ui.separator()
        ui.label("Why Choose Us?").classes("text-2xl font-bold mt-4")
        with ui.column().classes("gap-3"):
            points = [
                "✅ MNRE-certified solar installations",
                "✅ End-to-end service — survey to commissioning",
                "✅ 25-year panel warranty",
                "✅ Government subsidy assistance",
                "✅ Experienced, trained technicians",
                "✅ Transparent pricing, no hidden costs",
            ]
            for p in points:
                ui.label(p).classes("text-gray-700")