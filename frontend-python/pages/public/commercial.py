"""
NP POWER TECH SOLAR - Commercial Solar Page
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/commercial")
def commercial_page():
    public_layout(current_page="/commercial")

    with ui.column().classes("w-full max-w-6xl mx-auto px-4 py-8 gap-8"):
        with ui.row().classes("w-full items-center justify-between gap-6 flex-wrap"):
            with ui.column().classes("flex-1 min-w-[300px] gap-3"):
                ui.label("Commercial Solar").classes("text-4xl font-bold text-gray-900")
                ui.label(
                    "Cut operational costs and gain tax benefits with solar for your office, "
                    "shop, mall, or commercial building."
                ).classes("text-lg text-gray-600")
                ui.button("Get Quote", on_click=lambda: ui.navigate.to("/get-quote")).classes(
                    "bg-yellow-500 text-white font-semibold px-6 py-3 mt-3"
                )
            with ui.column().classes("flex-1 min-w-[200px] items-center"):
                ui.icon("business", size="10rem").classes("text-yellow-500")

        ui.separator()

        ui.label("Why Commercial Solar?").classes("text-2xl font-bold")
        points = [
            ("Savings: Reduce electricity costs by 60-80%"),
            ("Tax Benefits: Accelerated depreciation up to 40%"),
            ("Fast Payback: 3-5 year ROI"),
            ("Brand Image: Showcase your green commitment"),
            ("Zero Downtime: Reliable power for business operations"),
            ("Scalable: Expand as your business grows"),
        ]
        with ui.column().classes("gap-2"):
            for p in points:
                with ui.row().classes("items-center gap-2"):
                    ui.icon("check_circle", size="1.3rem").classes("text-green-500")
                    ui.label(p).classes("text-gray-700")

        ui.separator()

        ui.label("Ideal For").classes("text-2xl font-bold")
        with ui.row().classes("w-full gap-3 flex-wrap"):
            for item in ["Offices", "Shops", "Showrooms", "Hospitals", "Schools", "Hotels", "Malls", "Warehouses"]:
                ui.chip(item, icon="check").classes("bg-yellow-50 text-yellow-700")

        ui.separator()

        with ui.card().classes("w-full bg-yellow-50 p-6 items-center"):
            ui.label("Ready to Save on Business Electricity?").classes("text-2xl font-bold")
            ui.button("Request Consultation", on_click=lambda: ui.navigate.to("/get-quote")).classes(
                "bg-yellow-500 text-white font-semibold px-6 py-3 mt-3"
            )