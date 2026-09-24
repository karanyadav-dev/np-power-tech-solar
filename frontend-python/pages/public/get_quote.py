"""
NP POWER TECH SOLAR - Get Quote Page (redirects to full wizard)
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/get-quote")
def get_quote_page():
    public_layout(current_page="/get-quote")

    with ui.column().classes("w-full max-w-3xl mx-auto px-4 py-8 gap-6"):
        ui.label("Get a Free Solar Quote").classes("text-4xl font-bold text-gray-900")
        ui.label(
            "Fill our 7-step wizard to get a detailed quotation. "
            "It takes only 2 minutes!"
        ).classes("text-lg text-gray-600")

        with ui.card().classes("w-full p-8 items-center bg-yellow-50"):
            ui.icon("solar_power", size="4rem").classes("text-yellow-500")
            ui.label("Ready to go solar?").classes("text-2xl font-bold mt-4")
            ui.label(
                "Our quotation wizard asks about your system requirements, electricity usage, "
                "roof details, and uploads — everything needed for an accurate quotation."
            ).classes("text-gray-600 text-center mt-2")

            ui.button(
                "Start Quotation Wizard →",
                on_click=lambda: ui.navigate.to("/quotation-request"),
            ).classes("bg-yellow-500 text-white font-semibold px-8 py-4 mt-6 text-lg")

        ui.separator()

        with ui.row().classes("w-full gap-6 flex-wrap justify-center"):
            with ui.card().classes("flex-1 min-w-[250px] p-5 items-center text-center"):
                ui.icon("schedule", size="2rem").classes("text-yellow-500")
                ui.label("Takes 2 minutes").classes("font-semibold mt-2")
                ui.label("Just answer 7 simple questions").classes("text-gray-500 text-sm")

            with ui.card().classes("flex-1 min-w-[250px] p-5 items-center text-center"):
                ui.icon("upload_file", size="2rem").classes("text-yellow-500")
                ui.label("Upload bill & photos").classes("font-semibold mt-2")
                ui.label("Optional but helps accuracy").classes("text-gray-500 text-sm")

            with ui.card().classes("flex-1 min-w-[250px] p-5 items-center text-center"):
                ui.icon("support_agent", size="2rem").classes("text-yellow-500")
                ui.label("Get callback").classes("font-semibold mt-2")
                ui.label("We'll contact within 24 hrs").classes("text-gray-500 text-sm")