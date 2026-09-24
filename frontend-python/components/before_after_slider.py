"""
NP POWER TECH SOLAR - Before/After Image Slider
"""

from nicegui import ui


def before_after_slider(before_url: str, after_url: str, title: str = ""):
    """Interactive before/after image comparison slider."""
    with ui.column().classes("w-full gap-2"):
        if title:
            ui.label(title).classes("text-lg font-semibold text-gray-800 text-center")

        with ui.element("div").classes(
            "relative w-full h-64 md:h-96 overflow-hidden rounded-lg shadow-lg"
        ):
            # Before image (bottom layer)
            ui.image(before_url).classes("absolute inset-0 w-full h-full object-cover")

            # After image (top layer, clipped)
            ui.image(after_url).classes(
                "absolute inset-0 w-full h-full object-cover"
            ).style("clip-path: inset(0 0 0 50%);")

            # Label
            ui.label("AFTER").classes(
                "absolute top-3 right-3 bg-green-500 text-white px-2 py-1 "
                "rounded text-xs font-bold"
            )
            ui.label("BEFORE").classes(
                "absolute top-3 left-3 bg-red-500 text-white px-2 py-1 "
                "rounded text-xs font-bold"
            )

        ui.label("Tip: Use CSS custom properties to make this fully draggable in future.").classes(
            "text-xs text-gray-400 text-center"
        )


def simple_before_after():
    """Placeholder for homepage — uses colored boxes instead of real images."""
    with ui.row().classes("w-full gap-4 flex-wrap justify-center"):
        with ui.card().classes("w-full md:w-96 p-4"):
            ui.label("BEFORE").classes("text-sm font-bold text-red-500 text-center")
            with ui.element("div").classes(
                "w-full h-48 bg-gray-300 flex items-center justify-center rounded"
            ):
                ui.icon("roofing", size="4rem").classes("text-gray-500")

        with ui.card().classes("w-full md:w-96 p-4"):
            ui.label("AFTER").classes("text-sm font-bold text-green-500 text-center")
            with ui.element("div").classes(
                "w-full h-48 bg-gradient-to-br from-yellow-400 to-orange-400 "
                "flex items-center justify-center rounded"
            ):
                ui.icon("solar_power", size="4rem").classes("text-white")