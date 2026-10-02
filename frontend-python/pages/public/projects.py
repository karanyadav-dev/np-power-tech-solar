"""
NP POWER TECH SOLAR - Public Projects Page
Showcase completed solar projects with photos.
"""

from nicegui import ui
from layouts.public_layout import public_layout, public_layout_footer
from services.project_service import project_service
from config.settings import settings


def _build_image_url(image_path: str) -> str:
    """Build full image URL from backend."""
    if not image_path:
        return ""
    if image_path.startswith("http://") or image_path.startswith("https://"):
        return image_path
    if image_path.startswith("/uploads"):
        return f"{settings.BACKEND_API_BASE_URL}{image_path}"
    return f"{settings.BACKEND_API_BASE_URL}/uploads/{image_path}"


@ui.page("/projects")
def projects_page():
    container = public_layout(current_page="/projects")

    with container:
        # Hero
        ui.label("हमारे प्रोजेक्ट्स").classes("text-4xl font-bold text-gray-900")
        ui.label("हमारी टीम द्वारा पूरे किए गए सोलर इंस्टॉलेशन").classes(
            "text-gray-600 text-lg"
        )

        loading = ui.label("Loading projects...").classes("text-gray-500 mt-4")
        projects_container = ui.row().classes("w-full gap-6 flex-wrap mt-6")

        def load():
            projects_container.clear()

            resp = project_service.list(limit=50, isPublished=True)
            projects = resp.get("data", []) if resp.get("success") else []

            loading.set_text("")
            loading.classes("hidden")

            with projects_container:
                if not projects:
                    with ui.column().classes("w-full items-center py-12"):
                        ui.icon("solar_power", size="5rem").classes("text-gray-300")
                        ui.label("जल्द ही प्रोजेक्ट्स आ रहे हैं...").classes(
                            "text-gray-500 text-lg mt-4"
                        )
                    return

                for p in projects:
                    with ui.card().classes(
                        "w-full md:w-96 p-0 overflow-hidden hover:shadow-xl transition-shadow"
                    ):
                        # --- Image Section ---
                        images = p.get("images", [])

                        # Handle both list of strings and list of dicts
                        image_url = None
                        if images:
                            first = images[0]
                            if isinstance(first, dict):
                                image_url = first.get("image_url") or first.get("url")
                            else:
                                image_url = first

                        if image_url:
                            full_url = _build_image_url(image_url)
                            # Use ui.image with fallback on error
                            with ui.element("div").classes(
                                "w-full h-56 bg-gray-100 flex items-center justify-center overflow-hidden"
                            ):
                                ui.image(full_url).classes(
                                    "w-full h-full object-cover"
                                ).on(
                                    "error",
                                    lambda: ui.notify("Image failed to load", type="warning"),
                                )
                        else:
                            # Placeholder if no image
                            with ui.element("div").classes(
                                "w-full h-56 bg-gradient-to-br from-yellow-400 to-orange-400 "
                                "flex items-center justify-center"
                            ):
                                ui.icon("solar_power", size="5rem").classes("text-white")

                        # --- Content Section ---
                        with ui.column().classes("p-5 gap-2"):
                            # Project name
                            ui.label(p.get("project_name", "")).classes(
                                "text-xl font-bold text-gray-900"
                            )

                            # Location
                            loc_parts = [p.get("city"), p.get("state")]
                            loc = ", ".join([x for x in loc_parts if x])
                            if loc:
                                with ui.row().classes("items-center gap-1"):
                                    ui.icon("location_on", size="1rem").classes(
                                        "text-yellow-500"
                                    )
                                    ui.label(loc).classes("text-sm text-gray-600")

                            # Chips (size + type)
                            with ui.row().classes("gap-2 flex-wrap mt-1"):
                                if p.get("system_size_kw"):
                                    ui.chip(f"{p['system_size_kw']} kW").classes(
                                        "bg-yellow-100 text-yellow-800 text-xs"
                                    )
                                if p.get("system_type"):
                                    ui.chip(p["system_type"]).classes(
                                        "bg-blue-100 text-blue-800 text-xs"
                                    )

                            # Description
                            if p.get("description"):
                                desc = p["description"]
                                if len(desc) > 120:
                                    desc = desc[:120] + "..."
                                ui.label(desc).classes("text-sm text-gray-600")

                            # CTA
                            ui.button(
                                "और जानें →",
                                on_click=lambda: ui.navigate.to("/get-quote"),
                            ).classes(
                                "bg-yellow-500 text-white mt-3 w-full"
                            ).style("color: white !important;")

        ui.timer(0.3, load, once=True)

    public_layout_footer()