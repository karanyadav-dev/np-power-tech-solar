"""
NP POWER TECH SOLAR - Write Review Page
Customer review form with photo upload.
"""

from nicegui import ui
from layouts.public_layout import public_layout, public_layout_footer
from services.review_service import review_service
from components.upload_widget import upload_widget


@ui.page("/write-review")
def write_review_page():
    container = public_layout(current_page="/write-review")

    uploaded_photos = []

    with container:
        ui.label("अपना अनुभव साझा करें").classes("text-4xl font-bold text-gray-900")
        ui.label(
            "आपकी राय दूसरों को सही निर्णय लेने में मदद करती है। धन्यवाद!"
        ).classes("text-gray-600 text-lg")

        with ui.card().classes("w-full p-6 gap-4 mt-4"):
            # Customer details
            name = ui.input("आपका नाम *").classes("w-full").props("outlined")
            location = ui.input("आपका शहर / गाँव").classes("w-full").props("outlined")
            phone = ui.input("फ़ोन (वैकल्पिक)").classes("w-full").props("outlined")

            # Rating
            ui.label("रेटिंग दें *").classes("text-sm font-semibold text-gray-700 mt-2")
            rating = ui.slider(min=1, max=5, value=5, step=1).classes("w-full")
            rating_label = ui.label("⭐ 5 / 5").classes("text-lg font-bold text-yellow-600")
            rating.on_value_change(lambda e: rating_label.set_text(f"⭐ {int(e.value)} / 5"))

            # Review title + text
            title = ui.input("रिव्यू शीर्षक (वैकल्पिक)").classes("w-full").props("outlined")
            text = ui.textarea("आपका अनुभव *").classes("w-full").props("outlined")

            # Photos section
            ui.separator()
            ui.label("📸 सोलर पैनल की फोटो अपलोड करें (वैकल्पिक)").classes(
                "text-base font-semibold text-gray-700"
            )
            ui.label(
                "आपके घर की छत पर लगी सोलर पैनल की फोटो - दूसरों को दिखाने के लिए"
            ).classes("text-xs text-gray-500")

            def on_photo_upload(result):
                url = result.get("data", {}).get("relativePath", "")
                if url and url not in uploaded_photos:
                    uploaded_photos.append(url)
                ui.notify("फोटो अपलोड हो गई ✅", type="positive")
                photo_status.set_text(f"✅ {len(uploaded_photos)} फोटो अपलोड हो गई")
                photo_status.classes("text-xs text-green-600 font-semibold")

            upload_widget(
                upload_type="site_photos",
                label="📷 फोटो अपलोड करें",
                accept="image/*",
                max_size_mb=10,
                on_success=on_photo_upload,
            )

            photo_status = ui.label("").classes("text-xs text-gray-500")

            result_label = ui.label("").classes("text-sm mt-2")

            def submit():
                if not name.value or not text.value:
                    result_label.set_text("कृपया नाम और रिव्यू दोनों भरें।")
                    result_label.classes("text-red-600 font-semibold")
                    return

                payload = {
                    "customerName": name.value,
                    "customerLocation": location.value or None,
                    "customerPhone": phone.value or None,
                    "rating": int(rating.value),
                    "title": title.value or None,
                    "reviewText": text.value,
                    "photoUrls": list(uploaded_photos),
                }

                resp = review_service.create(payload)

                if resp.get("success"):
                    result_label.set_text(
                        "✅ धन्यवाद! आपका रिव्यू जमा हो गया। सत्यापन के बाद वेबसाइट पर दिखेगा।"
                    )
                    result_label.classes("text-green-600 font-semibold")
                    # Clear
                    name.value = ""
                    location.value = ""
                    phone.value = ""
                    title.value = ""
                    text.value = ""
                    uploaded_photos.clear()
                    photo_status.set_text("")
                else:
                    err = resp.get("error", {}).get("message", "कृपया दोबारा कोशिश करें।")
                    result_label.set_text(f"❌ {err}")
                    result_label.classes("text-red-600 font-semibold")

            ui.button(
                "रिव्यू जमा करें",
                on_click=submit,
            ).classes("bg-yellow-500 text-white font-semibold px-8 py-3 text-lg mt-2").style(
                "color: white !important;"
            )

    public_layout_footer()