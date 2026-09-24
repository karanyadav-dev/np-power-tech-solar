"""
NP POWER TECH SOLAR - Hybrid System Page
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/hybrid")
def hybrid_page():
    public_layout(current_page="/hybrid")

    with ui.column().classes("w-full max-w-6xl mx-auto px-4 py-8 gap-8"):
        with ui.row().classes("w-full items-center justify-between gap-6 flex-wrap"):
            with ui.column().classes("flex-1 min-w-[300px] gap-3"):
                ui.label("Hybrid Solar System").classes("text-4xl font-bold text-gray-900")
                ui.label(
                    "Best of both worlds — grid connection + battery backup. "
                    "Never lose power during outages while saving on bills."
                ).classes("text-lg text-gray-600")
                ui.button("Get Quote", on_click=lambda: ui.navigate.to("/get-quote")).classes(
                    "bg-yellow-500 text-white font-semibold px-6 py-3 mt-3"
                )
            with ui.column().classes("flex-1 min-w-[200px] items-center"):
                ui.icon("sync_alt", size="10rem").classes("text-yellow-500")

        ui.separator()

        ui.label("How Hybrid Works").classes("text-2xl font-bold")
        with ui.column().classes("gap-3"):
            for i, step in enumerate([
                "Solar panels generate power during day",
                "Excess power charges battery bank first",
                "Remaining excess exported to grid",
                "During night/outage, battery supplies power",
                "Grid acts as backup when battery is low",
                "You get both savings AND backup",
            ], 1):
                with ui.row().classes("items-center gap-3"):
                    ui.label(str(i)).classes(
                        "w-8 h-8 bg-yellow-500 text-white rounded-full flex items-center justify-center text-sm font-bold"
                    )
                    ui.label(step).classes("text-gray-700")

        ui.separator()

        ui.label("Advantages").classes("text-2xl font-bold")
        with ui.row().classes("w-full gap-4 flex-wrap"):
            for icon, text in [
                ("backup", "Power backup"),
                ("savings", "Grid savings"),
                ("battery_full", "Battery storage"),
                ("eco", "Eco-friendly"),
                ("trending_up", "Higher ROI"),
                ("settings", "Flexible"),
            ]:
                with ui.card().classes("flex-1 min-w-[180px] p-4 items-center text-center"):
                    ui.icon(icon, size="2.5rem").classes("text-yellow-500")
                    ui.label(text).classes("text-sm mt-2")