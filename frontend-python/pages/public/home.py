"""
NP POWER TECH SOLAR - Homepage
"""

from nicegui import ui
from layouts.public_layout import public_layout
from config.settings import settings


@ui.page("/")
def home_page():
    """Render the homepage."""
    public_layout(current_page="/")

    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-12"):
        # ---------- Hero Section ----------
        with ui.row().classes("w-full items-center justify-between gap-8 flex-wrap"):
            with ui.column().classes("gap-4 flex-1 min-w-[300px]"):
                ui.label("Power Your Future with Solar").classes(
                    "text-5xl font-bold text-gray-900 leading-tight"
                )
                ui.label(
                    "Save on electricity bills, reduce carbon footprint, and get government subsidies. "
                    "End-to-end solar solutions for homes, businesses, and industries."
                ).classes("text-lg text-gray-600")

                with ui.row().classes("gap-4 mt-4"):
                    ui.button(
                        "Get Free Quote",
                        on_click=lambda: ui.navigate.to("/get-quote"),
                    ).classes("bg-yellow-500 text-white font-semibold px-6 py-3")

                    ui.button(
                        "Solar Calculator",
                        on_click=lambda: ui.navigate.to("/calculator"),
                    ).props("outline").classes("border-yellow-500 text-yellow-600 px-6 py-3")

            with ui.column().classes("flex-1 min-w-[300px] items-center"):
                ui.icon("solar_power", size="12rem").classes("text-yellow-400")

        # ---------- Trust Badges ----------
        ui.separator()
        with ui.row().classes("w-full justify-around items-center gap-4 flex-wrap"):
            badges = [
                ("✓", "MNRE Certified"),
                ("✓", "25-Year Warranty"),
                ("✓", "Govt. Subsidy Available"),
                ("✓", "Free Site Survey"),
            ]
            for icon, label in badges:
                with ui.row().classes("items-center gap-2"):
                    ui.label(icon).classes("text-green-500 text-xl font-bold")
                    ui.label(label).classes("text-gray-700 font-medium")

        # ---------- Services ----------
        ui.label("Our Services").classes("text-3xl font-bold text-gray-900 mt-8")
        with ui.row().classes("w-full gap-6 flex-wrap"):
            services = [
                ("Residential Solar", "Home rooftop solar systems from 1kW to 10kW."),
                ("Commercial Solar", "Offices, shops, and commercial buildings."),
                ("Industrial Solar", "Large-scale solar for factories and industries."),
                ("Solar Water Heater", "Efficient water heating solutions."),
            ]
            for title, desc in services:
                with ui.card().classes("flex-1 min-w-[250px] p-6 hover:shadow-lg transition-shadow"):
                    ui.label(title).classes("text-xl font-semibold text-gray-900")
                    ui.label(desc).classes("text-gray-600 mt-2")

        # ---------- CTA Section ----------
        with ui.card().classes("w-full bg-yellow-50 p-8 mt-8 items-center"):
            ui.label("Ready to Go Solar?").classes("text-3xl font-bold text-gray-900")
            ui.label("Get a free site survey and personalized quote today.").classes(
                "text-gray-600 mt-2"
            )
            ui.button(
                "Book Free Survey",
                on_click=lambda: ui.navigate.to("/site-survey"),
            ).classes("bg-yellow-500 text-white font-semibold px-6 py-3 mt-4")