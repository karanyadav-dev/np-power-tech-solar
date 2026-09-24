"""
NP POWER TECH SOLAR - Admin Uploads
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
        ui.label("Customer bills, photos, and documents").classes("text-sm text-gray-500")

        # Filters
        with ui.row().classes("w-full gap-3 items-center"):
            type_filter = ui.select(
                {
                    "": "All Types",
                    "electricity_bills": "Electricity Bills",
                    "roof_photos": "Roof Photos",
                    "site_photos": "Site Photos",
                    "customer_documents": "Customer Documents",
                },
                value="",
                label="Filter by Type",
            ).classes("w-64")
            refresh_btn = ui.button("Refresh", icon="refresh").classes("bg-gray-700 text-white")

        loading = ui.label("Loading...").classes("text-gray-500")
        docs_container = ui.column().classes("w-full")

        def load():
            docs_container.clear()
            loading.set_text("Loading...")

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
                with ui.row().classes("w-full gap-4 mb-4 flex-wrap"):
                    bills = sum(1 for d in docs if d.get("document_type") == "electricity_bills")
                    photos = sum(1 for d in docs if d.get("document_type") == "roof_photos")
                    others = len(docs) - bills - photos

                    with ui.card().classes("flex-1 min-w-[150px] p-4"):
                        ui.label("Electricity Bills").classes("text-xs text-gray-500")
                        ui.label(str(bills)).classes("text-2xl font-bold text-yellow-500")

                    with ui.card().classes("flex-1 min-w-[150px] p-4"):
                        ui.label("Roof Photos").classes("text-xs text-gray-500")
                        ui.label(str(photos)).classes("text-2xl font-bold text-blue-500")

                    with ui.card().classes("flex-1 min-w-[150px] p-4"):
                        ui.label("Others").classes("text-xs text-gray-500")
                        ui.label(str(others)).classes("text-2xl font-bold text-green-500")

                # Table
                rows_html = ""
                for d in docs:
                    doc_type = d.get("document_type", "—")
                    title = d.get("title", "—")
                    size = d.get("file_size", 0)
                    size_str = f"{size / 1024:.1f} KB" if size else "—"
                    file_url = d.get("file_url", "#")
                    created = d.get("created_at", "")[:19]
                    mime = d.get("mime_type", "")

                    # Icon based on type
                    icon = "📄"
                    if "image" in mime:
                        icon = "🖼️"
                    elif "pdf" in mime:
                        icon = "📕"

                    rows_html += f"""
                    <tr class="border-b hover:bg-gray-50">
                        <td class="p-3">{icon} {title}</td>
                        <td class="p-3 text-xs">{doc_type}</td>
                        <td class="p-3 text-xs">{size_str}</td>
                        <td class="p-3 text-xs">{created}</td>
                        <td class="p-3">
                            <a href="{file_url}" target="_blank"
                               class="text-blue-600 hover:text-blue-800 no-underline text-xs mr-3">
                               👁️ View
                            </a>
                        </td>
                    </tr>
                    """

                ui.html(f"""
                <div class="overflow-x-auto">
                <table class="w-full bg-white rounded-lg shadow">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="p-3 text-left">File</th>
                            <th class="p-3 text-left">Type</th>
                            <th class="p-3 text-left">Size</th>
                            <th class="p-3 text-left">Uploaded</th>
                            <th class="p-3 text-left">Action</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
                </div>
                """).classes("w-full")

        refresh_btn.on("click", load)
        type_filter.on("change", load)
        ui.timer(0.3, load, once=True)