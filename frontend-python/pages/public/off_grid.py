"""
NP POWER TECH SOLAR - Off-Grid System Page
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/off-grid")
def off_grid_page():
    public_layout(current_page="/off-grid")

    with ui.column().classes("w-full max-w-6xl mx-auto px-4 py-8 gap-8"):
        with ui.row().classes("w-full items-center justify-between gap-6 flex-wrap"):
            with ui.column().classes("flex-1 min-w-[300px] gap-3"):
                ui.label("Off-Grid Solar System").classes("text-4xl font-bold text-gray-900")
                ui.label(
                    "Complete independence from the grid. Perfect for remote locations, "
                    "farmhouses, and areas with unreliable power supply."
                ).classes("text-lg text-gray-600")
                ui.button("Get Quote", on_click=lambda: ui.navigate.to("/get-quote")).classes(
                    "bg-yellow-500 text-white font-semibold px-6 py-3 mt-3"
                )
            with ui.column().classes("flex-1 min-w-[200px] items-center"):
                ui.icon("power_off", size="10rem").classes("text-yellow-500")

        ui.separator()

        ui.label("Components").classes("text-2xl font-bold")
        with ui.row().classes("w-full gap-4 flex-wrap"):
            for icon, title, desc in [
                ("solar_power", "Solar Panels", "Generate DC power"),
                ("battery_charging_full", "Battery Bank", "Store excess energy"),
                ("electrical_services", "Charge Controller", "Regulate charging"),
                ("power", "Inverter", "Convert to AC"),
            ]:
                with ui.card().classes("flex-1 min-w-[220px] p-5 items-center text-center"):
                    ui.icon(icon, size="2.5rem").classes("text-yellow-500")
                    ui.label(title).classes("text-lg font-semibold mt-2")
                    ui.label(desc).classes("text-gray-600 text-sm mt-1")

        ui.separator()

        ui.label("Best For").classes("text-2xl font-bold")
        with ui.row().classes("w-full gap-3 flex-wrap"):
            for item in ["Remote villages", "Farmhouses", "Hill stations", "Telecom towers", "Rural schools", "Off-grid homes"]:
                ui.chip(item, icon="check").classes("bg-yellow-50 text-yellow-700")

        ui.separator()

        with ui.card().classes("w-full bg-blue-50 p-6 items-center"):
            ui.label("Off-Grid requires proper sizing").classes("text-lg font-semibold")
            ui.label("We design systems based on your daily consumption pattern.").classes("text-gray-600 text-sm mt-1")
            ui.button("Talk to Expert", on_click=lambda: ui.navigate.to("/contact")).classes(
                "bg-yellow-500 text-white mt-3"
            )