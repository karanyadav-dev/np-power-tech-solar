"""
NP POWER TECH SOLAR - Add/Edit Project Form
With photo upload.
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.project_service import project_service
from components.upload_widget import upload_widget
from config.settings import settings
from api.client import api_client


def _project_form(project_id=None):
    """Reusable form."""
    is_edit = project_id is not None
    page_title = "Edit Project" if is_edit else "Add New Project"

    container = admin_layout(current_page="/admin/projects", page_title=page_title)

    with container:
        ui.link("← Back to Projects", "/admin/projects").classes("text-yellow-600 text-sm no-underline")
        ui.label(page_title).classes("text-2xl font-bold mt-2")

        existing = {}
        uploaded_images = []

        if is_edit:
            resp = project_service.get(project_id)
            if resp.get("success"):
                existing = resp.get("data", {})
                uploaded_images = [img["image_url"] for img in existing.get("images", [])]

        with ui.card().classes("w-full max-w-3xl p-6 gap-4 mt-4"):
            project_name = ui.input("Project Name *", value=existing.get("project_name", "")).classes("w-full").props("outlined")
            slug = ui.input("Slug (URL-friendly) *", value=existing.get("slug", "")).classes("w-full").props("outlined")

            with ui.row().classes("w-full gap-4"):
                location = ui.input("Location", value=existing.get("location", "") or "").classes("flex-1").props("outlined")
                city = ui.input("City", value=existing.get("city", "") or "").classes("flex-1").props("outlined")
                state = ui.input("State", value=existing.get("state", "") or "").classes("flex-1").props("outlined")

            with ui.row().classes("w-full gap-4"):
                system_size = ui.number("System Size (kW)", value=float(existing.get("system_size_kw", 0) or 0), min=0).classes("flex-1").props("outlined")
                system_type = ui.select(
                    ["on-grid", "off-grid", "hybrid"],
                    value=existing.get("system_type", "on-grid") or "on-grid",
                    label="System Type",
                ).classes("flex-1").props("outlined")

            description = ui.textarea("Description", value=existing.get("description", "") or "").classes("w-full").props("outlined")

            with ui.row().classes("gap-4"):
                is_published = ui.checkbox("Published (visible on website)", value=existing.get("is_published", False))
                customer_approval = ui.checkbox("Customer Approved", value=existing.get("customer_approval", False))

            # Image Upload Section
            ui.separator()
            ui.label("📸 Project Photos").classes("text-lg font-bold")
            ui.label("Upload 1-10 photos of this project").classes("text-sm text-gray-500")

            images_status = ui.label(f"{len(uploaded_images)} photo(s) uploaded").classes("text-sm text-gray-600")

            def on_image_upload(result):
                url = result.get("data", {}).get("relativePath", "")
                if url and url not in uploaded_images:
                    uploaded_images.append(url)
                ui.notify("Photo uploaded ✅", type="positive")
                images_status.set_text(f"✅ {len(uploaded_images)} photo(s) uploaded")
                images_status.classes("text-sm text-green-600 font-semibold")
                refresh_thumbnails()

            upload_widget(
                upload_type="project_images",
                label="📷 Upload Project Photo",
                accept="image/*",
                max_size_mb=10,
                on_success=on_image_upload,
            )

            # Thumbnail preview
            thumbnails_container = ui.row().classes("w-full gap-2 flex-wrap mt-2")

            def refresh_thumbnails():
                thumbnails_container.clear()
                with thumbnails_container:
                    for img in uploaded_images:
                        full_url = f"{settings.BACKEND_API_BASE_URL}{img}" if img.startswith("/uploads") else img
                        with ui.element("div").classes("relative border rounded"):
                            ui.image(full_url).classes("w-24 h-24 object-cover rounded")
                            # Remove button
                            def make_remove(u):
                                def do_remove():
                                    if u in uploaded_images:
                                        uploaded_images.remove(u)
                                    images_status.set_text(f"{len(uploaded_images)} photo(s) uploaded")
                                    refresh_thumbnails()
                                    ui.notify("Photo removed", type="info")
                                return do_remove

                            ui.button(icon="close", on_click=make_remove(img)).props(
                                "round dense flat size=sm color=negative"
                            ).classes("absolute top-0 right-0")

            refresh_thumbnails()

            # Save
            result_label = ui.label("").classes("text-sm")

            def save():
                if not project_name.value or not slug.value:
                    result_label.set_text("Name and slug are required")
                    result_label.classes("text-red-600")
                    return

                payload = {
                    "projectName": project_name.value,
                    "slug": slug.value.lower().replace(" ", "-"),
                    "location": location.value or None,
                    "city": city.value or None,
                    "state": state.value or None,
                    "systemSizeKw": float(system_size.value) if system_size.value else None,
                    "systemType": system_type.value,
                    "description": description.value or None,
                    "isPublished": bool(is_published.value),
                    "customerApproval": bool(customer_approval.value),
                    "images": uploaded_images,
                }

                if is_edit:
                    resp = project_service.update(project_id, payload)
                else:
                    resp = project_service.create(payload)

                if resp.get("success"):
                    ui.notify("Project saved ✅", type="positive")
                    ui.navigate.to("/admin/projects")
                else:
                    err = resp.get("error", {}).get("message", "Failed")
                    result_label.set_text(f"❌ {err}")
                    result_label.classes("text-red-600")

            with ui.row().classes("gap-3 mt-4"):
                ui.button("Cancel", on_click=lambda: ui.navigate.to("/admin/projects")).props("outline")
                ui.button("💾 Save Project", on_click=save).classes("bg-yellow-500 text-white font-semibold").style("color: white !important;")


@ui.page("/admin/projects/new")
def admin_project_new():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)
    _project_form(None)


@ui.page("/admin/projects/{project_id}/edit")
def admin_project_edit(project_id: str):
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)
    _project_form(project_id)