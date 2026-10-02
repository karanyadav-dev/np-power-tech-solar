"""
NP POWER TECH SOLAR - Admin Uploads
View uploaded documents with customer info + photo preview + manual link.
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.admin_service import admin_service
from api.client import api_client
from config.settings import settings


@ui.page("/admin/uploads")
def admin_uploads():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    container = admin_layout(current_page="/admin/uploads", page_title="Uploads")

    with container:
        ui.label("Uploaded Documents").classes("text-2xl font-bold")
        ui.label("Customer bills, photos, and documents with preview").classes(
            "text-sm text-gray-500"
        )

        # Filters
        with ui.row().classes("w-full gap-3 items-center"):
            type_filter = ui.select(
                {
                    "": "All Types",
                    "electricity_bills": "Electricity Bills",
                    "roof_photos": "Roof Photos",
                    "site_photos": "Site Photos",
                    "customer_documents": "Customer Documents",
                    "project_images": "Project Images",
                },
                value="",
                label="Filter by Type",
            ).classes("w-64").props("outlined dense")
            refresh_btn = ui.button("Refresh", icon="refresh").classes("bg-gray-700 text-white")

        loading = ui.label("Loading...").classes("text-gray-500")
        docs_container = ui.column().classes("w-full gap-4")

        def _full_url(relative_path: str) -> str:
            """Build full backend URL from relative path."""
            if not relative_path:
                return ""
            if relative_path.startswith("http"):
                return relative_path
            base = settings.BACKEND_API_BASE_URL.rstrip("/")
            path = relative_path if relative_path.startswith("/") else "/" + relative_path
            return base + path

        def _is_image(mime: str, filename: str) -> bool:
            if mime and "image" in mime.lower():
                return True
            return filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif"))

        def _open_link_dialog(doc_id: str, doc_title: str, on_success=None):
            """Open dialog to select customer + link."""
            resp = api_client.get("/api/v1/customers", params={"limit": 200})
            customers = resp.get("data", []) if resp.get("success") else []

            if not customers:
                ui.notify("No customers found", type="warning")
                return

            options = {}
            for c in customers:
                label = f"{c.get('full_name', '')} — {c.get('phone', '')}"
                if c.get("city"):
                    label += f" ({c.get('city')})"
                options[c["id"]] = label

            with ui.dialog() as dialog, ui.card().classes("w-96 p-5"):
                ui.label("🔗 Link Document to Customer").classes("text-lg font-bold mb-1")
                ui.label(f"Document: {doc_title[:40]}").classes("text-xs text-gray-500 mb-3")

                select = ui.select(options, label="Select Customer").classes("w-full").props("outlined")

                result_lbl = ui.label("").classes("text-xs mt-1")

                def do_link():
                    if not select.value:
                        result_lbl.set_text("Please select a customer")
                        result_lbl.classes("text-red-600 text-xs")
                        return

                    link_resp = api_client.post(
                        f"/api/v1/uploads/{doc_id}/link-customer",
                        json={"customerId": select.value},
                    )
                    if link_resp.get("success"):
                        ui.notify("✅ Linked to customer", type="positive")
                        dialog.close()
                        if on_success:
                            on_success()
                    else:
                        err = link_resp.get("error", {}).get("message", "Failed")
                        result_lbl.set_text(f"❌ {err}")
                        result_lbl.classes("text-red-600 text-xs")

                with ui.row().classes("w-full justify-end gap-2 mt-3"):
                    ui.button("Cancel", on_click=dialog.close).props("outline")
                    ui.button("🔗 Link", on_click=do_link).classes("bg-blue-500 text-white")

            dialog.open()

        def load():
            docs_container.clear()
            loading.set_text("Loading...")
            loading.classes("text-gray-500 text-sm")

            filters = {}
            if type_filter.value:
                filters["documentType"] = type_filter.value

            resp = admin_service.list_documents(**filters)
            docs = resp.get("data", []) if resp.get("success") else []
            loading.set_text(f"✅ {len(docs)} documents found")
            loading.classes("text-green-600 text-sm")

            with docs_container:
                if not docs:
                    ui.label("No uploads yet").classes("text-gray-500 text-center p-8")
                    return

                # Summary cards
                with ui.row().classes("w-full gap-4 flex-wrap mb-2"):
                    bills = sum(1 for d in docs if d.get("document_type") == "electricity_bills")
                    roof_photos = sum(1 for d in docs if d.get("document_type") == "roof_photos")
                    site_photos = sum(1 for d in docs if d.get("document_type") == "site_photos")
                    unlinked = sum(1 for d in docs if not d.get("customer_id"))

                    for label, val, color in [
                        ("Electricity Bills", bills, "text-yellow-600"),
                        ("Roof Photos", roof_photos, "text-blue-600"),
                        ("Site Photos", site_photos, "text-green-600"),
                        ("Unlinked", unlinked, "text-red-600"),
                    ]:
                        with ui.card().classes("flex-1 min-w-[150px] p-4"):
                            ui.label(label).classes("text-xs text-gray-500")
                            ui.label(str(val)).classes(f"text-2xl font-bold {color}")

                # Documents grid
                for d in docs:
                    doc_type = d.get("document_type", "—")
                    title = d.get("title", "—")
                    size = d.get("file_size", 0)
                    size_str = f"{size / 1024:.1f} KB" if size else "—"
                    file_url = d.get("file_url", "")
                    full_url = _full_url(file_url)
                    created = (d.get("created_at", "") or "")[:19].replace("T", " ")
                    mime = d.get("mime_type", "")
                    doc_id = d.get("id", "")

                    customer_name = d.get("customer_name") or "—"
                    customer_phone = d.get("customer_phone") or ""
                    customer_city = d.get("customer_city") or ""
                    customer_id = d.get("customer_id")

                    with ui.card().classes("w-full p-4"):
                        with ui.row().classes("w-full gap-4 items-start"):
                            # Preview (left)
                            with ui.column().classes("w-32 shrink-0"):
                                if _is_image(mime, title) and full_url:
                                    with ui.element("a").props(
                                        f'href="{full_url}" target="_blank"'
                                    ):
                                        ui.image(full_url).classes(
                                            "w-32 h-32 object-cover rounded border cursor-pointer"
                                        )
                                else:
                                    with ui.element("div").classes(
                                        "w-32 h-32 bg-gray-100 flex items-center justify-center rounded border"
                                    ):
                                        ui.icon("description", size="3rem").classes("text-gray-400")

                            # Details (right)
                            with ui.column().classes("flex-1 gap-1"):
                                with ui.row().classes("items-center gap-2 flex-wrap"):
                                    ui.label(title).classes("text-base font-bold text-gray-900")
                                    type_color = {
                                        "electricity_bills": "bg-yellow-100 text-yellow-800",
                                        "roof_photos": "bg-blue-100 text-blue-800",
                                        "site_photos": "bg-green-100 text-green-800",
                                        "customer_documents": "bg-purple-100 text-purple-800",
                                        "project_images": "bg-gray-100 text-gray-800",
                                    }.get(doc_type, "bg-gray-100 text-gray-800")
                                    ui.chip(doc_type).classes(f"{type_color} text-xs")

                                # Customer info OR link button
                                if customer_id:
                                    # Show linked customer
                                    with ui.row().classes("items-center gap-3 flex-wrap mt-1"):
                                        with ui.row().classes("items-center gap-1"):
                                            ui.icon("link", size="1rem").classes("text-green-600")
                                            ui.label("Linked:").classes("text-xs text-green-700 font-semibold")
                                            ui.label(customer_name).classes("text-sm font-semibold text-green-800")
                                        if customer_phone:
                                            with ui.row().classes("items-center gap-1"):
                                                ui.icon("phone", size="1rem").classes("text-gray-500")
                                                ui.label(customer_phone).classes("text-sm text-gray-600")
                                        if customer_city:
                                            with ui.row().classes("items-center gap-1"):
                                                ui.icon("location_on", size="1rem").classes("text-gray-500")
                                                ui.label(customer_city).classes("text-sm text-gray-600")
                                else:
                                    # Not linked — show link button
                                    with ui.row().classes("items-center gap-2 mt-1"):
                                        ui.label("⚠️ No customer linked").classes("text-xs text-orange-600 italic")
                                        ui.button(
                                            "🔗 Link to Customer",
                                            on_click=lambda d_id=doc_id, t=title: _open_link_dialog(d_id, t, on_success=load),
                                        ).props("flat dense dense").classes("text-blue-600 font-semibold text-xs")

                                # Meta
                                with ui.row().classes("items-center gap-4 mt-1 text-xs text-gray-500"):
                                    ui.label(f"Size: {size_str}")
                                    ui.label(f"Uploaded: {created}")
                                    if mime:
                                        ui.label(f"Type: {mime}")

                                # Actions
                                with ui.row().classes("gap-2 mt-2 flex-wrap"):
                                    if full_url:
                                        ui.button(
                                            "👁️ Open",
                                            on_click=lambda u=full_url: ui.run_javascript(
                                                f'window.open("{u}", "_blank")'
                                            ),
                                        ).props("flat dense").classes("text-blue-600")

                                        ui.button(
                                            "📋 Copy URL",
                                            on_click=lambda u=full_url: ui.run_javascript(
                                                f'navigator.clipboard.writeText("{u}"); '
                                                f'alert("URL copied")'
                                            ),
                                        ).props("flat dense").classes("text-gray-600")

                                    # Unlink button (if linked)
                                    if customer_id:
                                        def make_unlink(d_id):
                                            def do_unlink():
                                                unlink_resp = api_client.post(
                                                    f"/api/v1/uploads/{d_id}/link-customer",
                                                    json={"customerId": None},
                                                )
                                                if unlink_resp.get("success"):
                                                    ui.notify("Unlinked", type="info")
                                                    load()
                                                else:
                                                    ui.notify("Failed to unlink", type="negative")
                                            return do_unlink

                                        ui.button(
                                            "🔓 Unlink",
                                            on_click=make_unlink(doc_id),
                                        ).props("flat dense").classes("text-red-500 text-xs")

        refresh_btn.on("click", load)
        type_filter.on("change", load)
        ui.timer(0.3, load, once=True)