"""
NP POWER TECH SOLAR - Residential Solar Page
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/residential")
def residential_page():
    public_layout(current_page="/residential")

    with ui.column().classes("w-full max-w-6xl mx-auto px-4 py-8 gap-8"):
        # Hero
        with ui.row().classes("w-full items-center justify-between gap-6 flex-wrap"):
            with ui.column().classes("flex-1 min-w-[300px] gap-3"):
                ui.label("Residential Solar").classes("text-4xl font-bold text-gray-900")
                ui.label(
                    "Power your home with clean energy. Reduce electricity bills by up to 90% "
                    "with rooftop solar systems designed for Indian homes."
                ).classes("text-lg text-gray-600")
                with ui.row().classes("gap-3 mt-3"):
                    ui.button("Get Free Quote", on_click=lambda: ui.navigate.to("/get-quote")).classes(
                        "bg-yellow-500 text-white font-semibold px-6 py-3"
                    )
                    ui.button("Solar Calculator", on_click=lambda: ui.navigate.to("/calculator")).props(
                        "outline"
                    ).classes("border-yellow-500 text-yellow-600 px-6 py-3")
            with ui.column().classes("flex-1 min-w-[200px] items-center"):
                ui.icon("home", size="10rem").classes("text-yellow-500")

        ui.separator()

        # System sizes
        ui.label("Choose Your System Size").classes("text-2xl font-bold")
        sizes = [
            ("1 kW", "₹ 45,000 - 60,000", "~120 units/month", "1-2 BHK"),
            ("2 kW", "₹ 90,000 - 1,10,000", "~240 units/month", "2-3 BHK"),
            ("3 kW", "₹ 1,35,000 - 1,65,000", "~360 units/month", "3-4 BHK"),
            ("5 kW", "₹ 2,25,000 - 2,75,000", "~600 units/month", "Large homes"),
            ("10 kW", "₹ 4,50,000 - 5,50,000", "~1200 units/month", "Villas/Bungalows"),
        ]

        with ui.row().classes("w-full gap-4 flex-wrap mt-3"):
            for size, price, gen, ideal in sizes:
                with ui.card().classes("flex-1 min-w-[200px] p-5 hover:shadow-lg"):
                    ui.label(size).classes("text-2xl font-bold text-yellow-500")
                    ui.label(price).classes("text-sm text-gray-700 font-semibold mt-2")
                    ui.separator()
                    ui.label(f"Generation: {gen}").classes("text-sm text-gray-600 mt-2")
                    ui.label(f"Ideal for: {ideal}").classes("text-sm text-gray-500")

        ui.separator()

        # Benefits
        ui.label("Benefits of Home Solar").classes("text-2xl font-bold")
        benefits = [
            ("savings", "Save up to 90% on bills"),
            ("currency_rupee", "Govt. subsidy up to ₹78,000"),
            ("eco", "Reduce carbon footprint"),
            ("trending_up", "Increase property value"),
            ("battery_charging_full", "25-year panel life"),
            ("home", "Zero maintenance"),
        ]
        with ui.row().classes("w-full gap-4 flex-wrap"):
            for icon, text in benefits:
                with ui.card().classes("flex-1 min-w-[200px] p-4 items-center text-center"):
                    ui.icon(icon, size="2.5rem").classes("text-yellow-500")
                    ui.label(text).classes("text-sm text-gray-700 mt-2")

        ui.separator()

        # CTA
        with ui.card().classes("w-full bg-yellow-50 p-6 items-center"):
            ui.label("Ready to Install?").classes("text-2xl font-bold")
            ui.label("Book a free site survey and get a personalized quote.").classes("text-gray-600 mt-2")
            ui.button("Book Free Survey", on_click=lambda: ui.navigate.to("/site-survey")).classes(
                "bg-yellow-500 text-white font-semibold px-6 py-3 mt-3"
            )