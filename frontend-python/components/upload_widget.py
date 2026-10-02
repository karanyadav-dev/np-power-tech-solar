"""
NP POWER TECH SOLAR - Upload Widget
Reusable file upload component (NiceGUI 2.x compatible).
"""

import httpx
from nicegui import ui, events, app
from config.settings import settings


def upload_widget(
    upload_type: str,
    label: str = "Upload File",
    accept: str = "image/*,application/pdf",
    max_size_mb: int = 10,
    customer_id: str = None,
    quotation_id: str = None,
    on_success=None,
):
    """Reusable file upload widget."""

    with ui.card().classes("w-full p-4 border-2 border-dashed border-gray-300 rounded-lg"):
        ui.label(label).classes("text-sm font-semibold text-gray-700")

        status_label = ui.label("").classes("text-xs text-gray-500")

        async def handle_upload(e: events.UploadEventArguments):
            try:
                # NiceGUI 2.x: e.content is the file content (bytes)
                content = e.content.read() if hasattr(e.content, "read") else e.content
                filename = e.name

                size_mb = len(content) / (1024 * 1024)
                if size_mb > max_size_mb:
                    status_label.set_text(f"❌ File too large ({size_mb:.1f} MB > {max_size_mb} MB)")
                    status_label.classes("text-xs text-red-600")
                    return

                status_label.set_text(f"⏳ Uploading {filename}...")
                status_label.classes("text-xs text-blue-600")

                token = app.storage.user.get("access_token")

                files = {"file": (filename, content)}
                data = {"uploadType": upload_type}
                if customer_id:
                    data["customerId"] = customer_id
                if quotation_id:
                    data["quotationId"] = quotation_id

                headers = {}
                if token:
                    headers["Authorization"] = f"Bearer {token}"

                async with httpx.AsyncClient(timeout=60) as client:
                    resp = await client.post(
                        f"{settings.BACKEND_API_BASE_URL}/api/v1/uploads",
                        files=files,
                        data=data,
                        headers=headers,
                    )

                if resp.status_code in (200, 201):
                    result = resp.json()
                    file_url = result.get("data", {}).get("relativePath", "")
                    status_label.set_text(f"✅ Uploaded: {filename}")
                    status_label.classes("text-xs text-green-600")

                    if on_success:
                        on_success(result)
                else:
                    err = resp.text[:200]
                    status_label.set_text(f"❌ Upload failed: {err}")
                    status_label.classes("text-xs text-red-600")

            except Exception as err:
                status_label.set_text(f"❌ Error: {str(err)}")
                status_label.classes("text-xs text-red-600")

        ui.upload(
            on_upload=handle_upload,
            auto_upload=True,
            max_file_size=max_size_mb * 1024 * 1024,
            max_files=1,
        ).props(f'accept="{accept}" flat').classes("w-full")