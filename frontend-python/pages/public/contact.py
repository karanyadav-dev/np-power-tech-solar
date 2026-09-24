"""
NP POWER TECH SOLAR - Contact Page
"""

from nicegui import ui
from layouts.public_layout import public_layout
from config.settings import settings
from services.lead_service import lead_service


@ui.page("/contact")
def contact_page():
    public_layout(current_page="/contact")

    with ui.column().classes("w-full max-w-6xl mx-auto px-4 py-8 gap-8"):
        ui.label("Contact Us").classes("text-4xl font-bold text-gray-900")
        ui.label("Have a question? We'd love to hear from you.").classes("text-gray-600")

        with ui.row().classes("w-full gap-8 flex-wrap"):
            # Contact info
            with ui.column().classes("flex-1 min-w-[300px] gap-4"):
                ui.label("Get in Touch").classes("text-2xl font-bold")
                if settings.PUBLIC_COMPANY_PHONE:
                    with ui.row().classes("items-center gap-3"):
                        ui.icon("phone", size="1.5rem").classes("text-yellow-500")
                        ui.label(settings.PUBLIC_COMPANY_PHONE).classes("text-gray-700")
                if settings.PUBLIC_COMPANY_EMAIL:
                    with ui.row().classes("items-center gap-3"):
                        ui.icon("email", size="1.5rem").classes("text-yellow-500")
                        ui.label(settings.PUBLIC_COMPANY_EMAIL).classes("text-gray-700")
                if settings.PUBLIC_COMPANY_ADDRESS:
                    with ui.row().classes("items-center gap-3"):
                        ui.icon("location_on", size="1.5rem").classes("text-yellow-500")
                        ui.label(settings.PUBLIC_COMPANY_ADDRESS).classes("text-gray-700")

                with ui.row().classes("items-center gap-3"):
                    ui.icon("schedule", size="1.5rem").classes("text-yellow-500")
                    ui.label("Mon - Sat: 9:00 AM - 6:00 PM").classes("text-gray-700")

            # Contact form
            with ui.card().classes("flex-1 min-w-[300px] p-6 gap-4"):
                ui.label("Send us a message").classes("text-xl font-bold")
                name = ui.input("Name *").classes("w-full")
                phone = ui.input("Phone *").classes("w-full")
                email = ui.input("Email").classes("w-full")
                msg = ui.textarea("Message").classes("w-full")

                result_label = ui.label("").classes("text-sm")

                def submit():
                    if not name.value or not phone.value:
                        result_label.set_text("Please fill name and phone.")
                        result_label.classes("text-red-600 text-sm")
                        return

                    resp = lead_service.create({
                        "fullName": name.value,
                        "phone": phone.value,
                        "email": email.value or None,
                        "message": msg.value or "Contact form submission",
                        "sourceCode": "website",
                    })

                    if resp.get("success"):
                        ref = resp.get("data", {}).get("lead_number", "")
                        result_label.set_text(f"✅ Message sent! Reference: {ref}")
                        result_label.classes("text-green-600 text-sm")
                        name.value = ""
                        phone.value = ""
                        email.value = ""
                        msg.value = ""
                    else:
                        err = resp.get("error", {}).get("message", "Try again.")
                        result_label.set_text(f"❌ {err}")
                        result_label.classes("text-red-600 text-sm")

                ui.button("Send Message", on_click=submit).classes(
                    "bg-yellow-500 text-white w-full mt-2"
                )