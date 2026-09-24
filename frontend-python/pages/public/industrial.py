"""
NP POWER TECH SOLAR - Industrial Solar Page
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/industrial")
def industrial_page():
    public_layout(current_page="/industrial")

    with ui.column().classes("w-full max-w-6xl mx-auto px-4 py-8 gap-8"):
        with ui.row().classes("w-full items-center justify-between gap-6 flex-wrap"):
            with ui.column().classes("flex-1 min-w-[300px] gap-3"):
                ui.label("Industrial Solar").classes("text-4xl font-bold text-gray-900")
                ui.label(
                    "Large-scale solar plants for factories and industrial units. "
                    "High ROI, quick payback, and huge operational savings."
                ).classes("text-lg text-gray-600")
                ui.button("Request Proposal", on_click=lambda: ui.navigate.to("/get-quote")).classes(
                    "bg-yellow-500 text-white font-semibold px-6 py-3 mt-3"
                )
            with ui.column().classes("flex-1 min-w-[200px] items-center"):
                ui.icon("factory", size="10rem").classes("text-yellow-500")

        ui.separator()

        ui.label("Industrial Solar Benefits").classes("text-2xl font-bold")
        with ui.row().classes("w-full gap-4 flex-wrap"):
            benefits = [
                ("trending_up", "30-40% IRR"),
                ("currency_rupee", "Tax Benefits"),
                ("schedule", "3-4 Year Payback"),
                ("eco", "Carbon Credits"),
                ("offline_bolt", "Zero Downtime"),
                ("engineering", "Custom Design"),
            ]
            for icon, text in benefits:
                with ui.card().classes("flex-1 min-w-[180px] p-4 items-center text-center"):
                    ui.icon(icon, size="2.5rem").classes("text-yellow-500")
                    ui.label(text).classes("text-sm mt-2")

        ui.separator()

        ui.label("Our Industrial Capabilities").classes("text-2xl font-bold")
        caps = [
            "Ground-mounted solar plants (100 kW - 10 MW+)",
            "Rooftop solar for large factories",
            "Solar carports and shade structures",
            "Hybrid systems with DG sync",
            "Net metering & open access",
            "O&M contracts for 25 years",
        ]
        with ui.column().classes("gap-2"):
            for c in caps:
                with ui.row().classes("items-center gap-2"):
                    ui.icon("check_circle", size="1.3rem").classes("text-green-500")
                    ui.label(c).classes("text-gray-700")

        ui.separator()

        with ui.card().classes("w-full bg-yellow-50 p-6 items-center"):
            ui.label("Let's Discuss Your Project").classes("text-2xl font-bold")
            ui.button("Contact Sales", on_click=lambda: ui.navigate.to("/contact")).classes(
                "bg-yellow-500 text-white font-semibold px-6 py-3 mt-3"
            )