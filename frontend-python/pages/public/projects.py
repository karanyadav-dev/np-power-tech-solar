"""
NP POWER TECH SOLAR - Projects Portfolio
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/projects")
def projects_page():
    public_layout(current_page="/projects")

    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-8"):
        ui.label("Our Projects").classes("text-4xl font-bold text-gray-900")
        ui.label("A glimpse of solar installations we've completed.").classes("text-gray-600")

        # Placeholder projects (to be fetched from API in later phase)
        projects = [
            {"name": "5kW Rooftop - Delhi", "size": "5 kW", "type": "Residential On-grid"},
            {"name": "10kW Commercial - Mumbai", "size": "10 kW", "type": "Commercial On-grid"},
            {"name": "3kW Home - Pune", "size": "3 kW", "type": "Residential Hybrid"},
        ]

        with ui.row().classes("w-full gap-6 flex-wrap"):
            for p in projects:
                with ui.card().classes("w-full md:w-96 p-6"):
                    ui.icon("solar_power", size="4rem").classes("text-yellow-500")
                    ui.label(p["name"]).classes("text-xl font-bold text-gray-900 mt-3")
                    ui.label(f"Size: {p['size']}").classes("text-gray-600")
                    ui.label(f"Type: {p['type']}").classes("text-gray-600")

        ui.separator()
        ui.label(
            "More projects coming soon. Visit this page regularly for updates."
        ).classes("text-gray-500 text-center mt-8")