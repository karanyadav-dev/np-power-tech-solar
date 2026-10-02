"""
NP POWER TECH SOLAR - Admin Projects
List, add, edit, delete projects with image support.
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.project_service import project_service
from config.settings import settings
from api.client import api_client


def _image_url(img_path: str) -> str:
    """Convert image path to full backend URL."""
    if not img_path:
        return ""
    if img_path.startswith("http://") or img_path.startswith("https://"):
        return img_path
    if img_path.startswith("/uploads"):
        return f"{settings.BACKEND_API_BASE_URL}{img_path}"
    return f"{settings.BACKEND_API_BASE_URL}/uploads/{img_path}"


@ui.page("/admin/projects")
def admin_projects():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    container = admin_layout(current_page="/admin/projects", page_title="Projects")

    with container:
        with ui.row().classes("w-full justify-between items-center"):
            with ui.column().classes("gap-0"):
                ui.label("Projects Portfolio").classes("text-2xl font-bold")
                ui.label("Add and manage your completed solar projects").classes("text-sm text-gray-500")

            ui.button(
                "+ Add Project",
                on_click=lambda: ui.navigate.to("/admin/projects/new"),
            ).classes("bg-yellow-500 text-white font-semibold").style("color: white !important;")

        loading = ui.label("Loading...").classes("text-gray-500")
        projects_container = ui.column().classes("w-full")

        def load():
            projects_container.clear()
            resp = project_service.list(limit=100)
            projects = resp.get("data", []) if resp.get("success") else []
            loading.set_text(f"✅ {len(projects)} projects found")
            loading.classes("text-green-600 text-sm")

            with projects_container:
                if not projects:
                    ui.label("No projects yet. Click '+ Add Project' to start.").classes(
                        "text-gray-500 text-center p-8"
                    )
                    return

                with ui.row().classes("w-full gap-4 flex-wrap mt-2"):
                    for p in projects:
                        with ui.card().classes("w-80 p-4"):
                            # First image thumbnail
                            images = p.get("images", [])
                            if images:
                                first_img = images[0]
                                full_url = _image_url(first_img)
                                ui.image(full_url).classes("w-full h-40 object-cover rounded")
                            else:
                                with ui.element("div").classes(
                                    "w-full h-40 bg-gradient-to-br from-yellow-400 to-orange-400 "
                                    "flex items-center justify-center rounded"
                                ):
                                    ui.icon("photo_library", size="3rem").classes("text-white")

                            ui.label(p.get("project_name", "")).classes("text-lg font-bold mt-2")

                            loc_parts = [p.get("city"), p.get("state")]
                            loc = ", ".join([x for x in loc_parts if x])
                            if loc:
                                ui.label(f"📍 {loc}").classes("text-sm text-gray-500")

                            with ui.row().classes("gap-2 mt-1"):
                                if p.get("system_size_kw"):
                                    ui.chip(f"{p['system_size_kw']} kW").classes("bg-yellow-100 text-xs")
                                if p.get("system_type"):
                                    ui.chip(p["system_type"]).classes("bg-blue-100 text-xs")

                            status = "✅ Published" if p.get("is_published") else "⏳ Draft"
                            ui.label(status).classes("text-xs text-gray-600 mt-2")

                            with ui.row().classes("gap-2 mt-3"):
                                ui.button(
                                    "✏️ Edit",
                                    on_click=lambda pid=p["id"]: ui.navigate.to(f"/admin/projects/{pid}/edit"),
                                ).props("outline dense").classes("text-blue-600")

                                def make_delete(pid):
                                    def do_delete():
                                        resp = project_service.delete(pid)
                                        if resp.get("success"):
                                            ui.notify("Project deleted ✅", type="positive")
                                            load()
                                        else:
                                            ui.notify("Delete failed", type="negative")
                                    return do_delete

                                ui.button(
                                    "🗑️ Delete",
                                    on_click=make_delete(p["id"]),
                                ).props("outline dense").classes("text-red-600")

        ui.timer(0.3, load, once=True)