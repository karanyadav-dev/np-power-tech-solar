"""
NP POWER TECH SOLAR - Write Review Page
"""

from nicegui import ui
from layouts.public_layout import public_layout
from services.review_service import review_service
from components.upload_widget import upload_widget


@ui.page("/write-review")
def write_review_page():
    public_layout(current_page="/write-review")

    with ui.column().classes("w-full max-w-3xl mx-auto px-4 py-8 gap-6"):
        ui.label("Share Your Experience").classes("text-4xl font-bold text-gray-900")
        ui.label(
            "Your feedback helps others make the right choice. Thank you!"
        ).classes("text-gray-600")

        with ui.card().classes("w-full p-6 gap-4"):
            name = ui.input("Your Name *").classes("w-full")
            location = ui.input("Your City / Location").classes("w-full")
            phone = ui.input("Phone (optional, kept private)").classes("w-full")

            rating = ui.slider(min=1, max=5, value=5, step=1).classes("w-full")
            rating_label = ui.label("⭐ 5 / 5").classes("text-lg font-bold text-yellow-600")
            rating.on_value_change(lambda e: rating_label.set_text(f"⭐ {int(e.value)} / 5"))

            title = ui.input("Review Title (optional)").classes("w-full")
            text = ui.textarea("Your Review *").classes("w-full")

            ui.separator()
            ui.label("📸 Upload Roof / Installation Photo (optional)").classes("text-sm font-semibold")
            photo_urls = []

            def on_photo_upload(result):
                url = result.get("data", {}).get("relativePath", "")
                if url:
                    photo_urls.append(url)
                ui.notify("Photo uploaded ✅", type="positive")

            upload_widget(
                upload_type="site_photos",
                label="Upload Installation Photo",
                accept="image/*",
                max_size_mb=10,
                on_success=on_photo_upload,
            )

            result_label = ui.label("").classes("text-sm")

            def submit():
                if not name.value or not text.value:
                    result_label.set_text("Please fill name and review text.")
                    result_label.classes("text-red-600")
                    return

                payload = {
                    "customerName": name.value,
                    "customerLocation": location.value or None,
                    "customerPhone": phone.value or None,
                    "rating": int(rating.value),
                    "title": title.value or None,
                    "reviewText": text.value,
                }

                resp = review_service.create(payload)

                if resp.get("success"):
                    result_label.set_text(
                        "✅ Thank you! Your review has been submitted and will appear after verification."
                    )
                    result_label.classes("text-green-600 font-semibold")
                    # Clear
                    name.value = ""
                    location.value = ""
                    phone.value = ""
                    title.value = ""
                    text.value = ""
                else:
                    err = resp.get("error", {}).get("message", "Try again.")
                    result_label.set_text(f"❌ {err}")
                    result_label.classes("text-red-600")

            ui.button("Submit Review", on_click=submit).classes(
                "bg-yellow-500 text-white font-semibold px-6 py-3 mt-4"
            )