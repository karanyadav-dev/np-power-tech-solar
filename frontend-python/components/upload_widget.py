"""
NP POWER TECH SOLAR - Upload Widget
Reusable file upload component.
"""

import base64
import httpx
from nicegui import ui, events
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
    """
    Reusable file upload widget.

    Args:
        upload_type: Type of upload (electricity_bills, roof_photos, site_photos, etc.)
        label: Display label
        accept: Accepted file types
        max_size_mb: Max file size in MB
        customer_id: Optional customer ID to link
        quotation_id: Optional quotation ID to link
        on_success: Callback function when upload succeeds
    """
    state = {"file_content": None, "file_name": None}

    with ui.card().classes("w-full p-4 border-2 border-dashed border-gray-300 rounded-lg"):
        ui.label(label).classes("text-sm font-semibold text-gray-700")

        status_label = ui.label("").classes("text-xs text-gray-500")

        async def handle_upload(e: events.UploadEventArguments):
            try:
                content = await e.file.read()

                # Size check
                size_mb = len(content) / (1024 * 1024)
                if size_mb > max_size_mb:
                    status_label.set_text(f"❌ File too large ({size_mb:.1f} MB > {max_size_mb} MB)")
                    status_label.classes("text-xs text-red-600")
                    return

                state["file_content"] = content
                state["file_name"] = e.file.name
                status_label.set_text(f"✅ Selected: {e.file.name} ({size_mb:.2f} MB)")
                status_label.classes("text-xs text-green-600")

                # Auto-upload
                await do_upload()

            except Exception as err:
                status_label.set_text(f"❌ Error: {str(err)}")
                status_label.classes("text-xs text-red-600")

        async def do_upload():
            if not state["file_content"]:
                return

            token = None
            try:
                from nicegui import app
                token = app.storage.user.get("access_token")
            except Exception:
                pass

            # Build multipart form data
            files = {
                "file": (state["file_name"], state["file_content"]),
            }
            data = {
                "uploadType": upload_type,
            }
            if customer_id:
                data["customerId"] = customer_id
            if quotation_id:
                data["quotationId"] = quotation_id

            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"

            try:
                async with httpx.AsyncClient(timeout=60) as client:
                    resp = await client.post(
                        f"{settings.BACKEND_API_BASE_URL}/api/v1/uploads",
                        files=files,
                        data=data,
                        headers=headers,
                    )

                if resp.status_code == 200 or resp.status_code == 201:
                    result = resp.json()
                    file_url = result.get("data", {}).get("relativePath", "")
                    status_label.set_text(f"✅ Uploaded: {state['file_name']}")
                    status_label.classes("text-xs text-green-600")

                    if on_success:
                        on_success(result)
                else:
                    err = resp.text[:200]
                    status_label.set_text(f"❌ Upload failed: {err}")
                    status_label.classes("text-xs text-red-600")

            except Exception as err:
                status_label.set_text(f"❌ Network error: {str(err)}")
                status_label.classes("text-xs text-red-600")

        ui.upload(
            on_upload=handle_upload,
            auto_upload=True,
            max_file_size=max_size_mb * 1024 * 1024,
            max_files=1,
        ).props(f'accept="{accept}" flat').classes("w-full")


def bill_upload_widget(quotation_id: str = None, on_success=None):
    """Pre-configured widget for electricity bill upload."""
    return upload_widget(
        upload_type="electricity_bills",
        label="📄 Electricity Bill",
        accept="image/*,application/pdf",
        max_size_mb=10,
        quotation_id=quotation_id,
        on_success=on_success,
    )


def roof_photo_widget(quotation_id: str = None, on_success=None):
    """Pre-configured widget for roof photo upload."""
    return upload_widget(
        upload_type="roof_photos",
        label="🏠 Roof / Site Photo",
        accept="image/*",
        max_size_mb=10,
        quotation_id=quotation_id,
        on_success=on_success,
    )