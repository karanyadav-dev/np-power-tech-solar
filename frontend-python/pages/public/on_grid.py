"""
NP POWER TECH SOLAR - On-Grid System Page
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/on-grid")
def on_grid_page():
    public_layout(current_page="/on-grid")

    with ui.column().classes("w-full max-w-6xl mx-auto px-4 py-8 gap-8"):
        with ui.row().classes("w-full items-center justify-between gap-6 flex-wrap"):
            with ui.column().classes("flex-1 min-w-[300px] gap-3"):
                ui.label("On-Grid Solar System").classes("text-4xl font-bold text-gray-900")
                ui.label(
                    "Grid-tied solar system — most popular for homes and businesses. "
                    "Export excess power to the grid and get credit on your bill."
                ).classes("text-lg text-gray-600")
                ui.button("Get Quote", on_click=lambda: ui.navigate.to("/get-quote")).classes(
                    "bg-yellow-500 text-white font-semibold px-6 py-3 mt-3"
                )
            with ui.column().classes("flex-1 min-w-[200px] items-center"):
                ui.icon("grid_on", size="10rem").classes("text-yellow-500")

        ui.separator()

        ui.label("How It Works").classes("text-2xl font-bold")
        steps = [
            "Solar panels generate DC power during the day",
            "Inverter converts DC to AC power",
            "AC power runs your appliances",
            "Excess power exported to grid via net meter",
            "Grid supplies power at night",
            "You get credit for exported units",
        ]
        with ui.column().classes("gap-2"):
            for i, s in enumerate(steps, 1):
                with ui.row().classes("items-center gap-3"):
                    ui.label(str(i)).classes(
                        "w-8 h-8 bg-yellow-500 text-white rounded-full flex items-center justify-center text-sm font-bold"
                    )
                    ui.label(s).classes("text-gray-700")

        ui.separator()

        ui.label("Advantages").classes("text-2xl font-bold")
        with ui.row().classes("w-full gap-4 flex-wrap"):
            for icon, text in [
                ("savings", "Lowest cost per kW"),
                ("speed", "Simple installation"),
                ("build", "Low maintenance"),
                ("trending_up", "High ROI"),
            ]:
                with ui.card().classes("flex-1 min-w-[200px] p-4 items-center text-center"):
                    ui.icon(icon, size="2.5rem").classes("text-yellow-500")
                    ui.label(text).classes("text-sm mt-2")