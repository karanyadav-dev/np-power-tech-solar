"""Solar Calculator page."""
from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/calculator")
def calculator_page():
    public_layout(current_page="/calculator")
    with ui.column().classes("w-full max-w-3xl mx-auto px-4 py-8 gap-6"):
        ui.label("Solar Calculator").classes("text-4xl font-bold text-gray-900")
        ui.label(
            "Estimate your solar system size and savings."
        ).classes("text-gray-600")

        with ui.card().classes("w-full p-6 gap-3"):
            ui.input("Monthly Electricity Bill (₹)").classes("w-full")
            ui.input("Monthly Units (kWh)").classes("w-full")
            ui.input("Roof Area (sq ft)").classes("w-full")
            ui.button(
                "Calculate (Coming Soon)",
                on_click=lambda: ui.notify("Full calculator coming soon!"),
            ).classes("bg-yellow-500 text-white font-semibold px-6 py-2 mt-2")