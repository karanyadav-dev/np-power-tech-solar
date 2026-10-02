"""
NP POWER TECH SOLAR - Contact Page
"""

from nicegui import ui
from layouts.public_layout import public_layout, public_layout_footer
from config.settings import settings
from services.settings_service import settings_service
from services.lead_service import lead_service


@ui.page("/contact")
def contact_page():
    container = public_layout(current_page="/contact")

    # Get settings
    company_phone = settings_service.get("company_phone", settings.PUBLIC_COMPANY_PHONE)
    company_phone_2 = settings_service.get("company_phone_2", "7357968185")
    company_email = settings_service.get("company_email", "nppowertechsolar@gmail.com")
    company_whatsapp = settings_service.get("company_whatsapp", settings.PUBLIC_COMPANY_WHATSAPP) or company_phone
    addr_1 = settings_service.get("company_address_1", "Police Thane Ke Pichhe, Govindgarh - 303712")
    addr_2 = settings_service.get("company_address_2", "Main Bus Stand, Dhodsar")

    with container:
        ui.label("संपर्क करें").classes("text-4xl font-bold text-gray-900")
        ui.label("कोई सवाल है? हमें बताएं — हम आपकी मदद करेंगे।").classes("text-gray-600 text-lg")

        with ui.row().classes("w-full gap-8 flex-wrap mt-4"):
            # Contact info
            with ui.column().classes("flex-1 min-w-[300px] gap-4"):
                with ui.card().classes("w-full p-6"):
                    ui.label("📞 फ़ोन").classes("text-xl font-bold text-gray-900")
                    with ui.column().classes("gap-1 mt-2"):
                        ui.label(f"Office: {company_phone}").classes("text-gray-700")
                        ui.label(f"Manager: {company_phone_2}").classes("text-gray-700")

                with ui.card().classes("w-full p-6"):
                    ui.label("✉️ ईमेल").classes("text-xl font-bold text-gray-900")
                    ui.label(company_email).classes("text-gray-700 mt-2")

                with ui.card().classes("w-full p-6"):
                    ui.label("📍 हमारे पते").classes("text-xl font-bold text-gray-900")
                    with ui.column().classes("gap-3 mt-2"):
                        with ui.row().classes("items-start gap-2"):
                            ui.icon("location_on", size="1.2rem").classes("text-yellow-500 mt-1")
                            with ui.column().classes("gap-0"):
                                ui.label("Office 1").classes("text-xs text-gray-500 font-semibold")
                                ui.label(addr_1).classes("text-gray-700")
                        with ui.row().classes("items-start gap-2"):
                            ui.icon("location_on", size="1.2rem").classes("text-yellow-500 mt-1")
                            with ui.column().classes("gap-0"):
                                ui.label("Office 2").classes("text-xs text-gray-500 font-semibold")
                                ui.label(addr_2).classes("text-gray-700")

                with ui.card().classes("w-full p-6 bg-green-50"):
                    ui.label("⏰ समय").classes("text-xl font-bold text-gray-900")
                    ui.label("सोमवार - शनिवार: सुबह 9:00 - शाम 6:00").classes("text-gray-700 mt-2")

            # Contact form
            with ui.card().classes("flex-1 min-w-[300px] p-6 gap-4"):
                ui.label("संदेश भेजें").classes("text-xl font-bold")
                name = ui.input("आपका नाम *").classes("w-full").props("outlined")
                phone = ui.input("फ़ोन *").classes("w-full").props("outlined")
                email = ui.input("ईमेल").classes("w-full").props("outlined")
                msg = ui.textarea("संदेश").classes("w-full").props("outlined")

                result_label = ui.label("").classes("text-sm")

                def submit():
                    if not name.value or not phone.value:
                        result_label.set_text("कृपया नाम और फ़ोन भरें।")
                        result_label.classes("text-red-600 font-semibold")
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
                        result_label.set_text(f"✅ संदेश भेजा गया! संदर्भ: {ref}")
                        result_label.classes("text-green-600 font-semibold")
                        name.value = ""
                        phone.value = ""
                        email.value = ""
                        msg.value = ""
                    else:
                        err = resp.get("error", {}).get("message", "कृपया दोबारा कोशिश करें।")
                        result_label.set_text(f"❌ {err}")
                        result_label.classes("text-red-600 font-semibold")

                ui.button(
                    "संदेश भेजें",
                    on_click=submit,
                ).classes("bg-yellow-500 text-white w-full py-3").style("color: white !important;")

    public_layout_footer()