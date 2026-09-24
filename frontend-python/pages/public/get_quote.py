"""
NP POWER TECH SOLAR - Get Quote Page (Lead Capture)
"""

from nicegui import ui
from layouts.public_layout import public_layout
from services.lead_service import lead_service


@ui.page("/get-quote")
def get_quote_page():
    public_layout(current_page="/get-quote")

    with ui.column().classes("w-full max-w-3xl mx-auto px-4 py-8 gap-6"):
        ui.label("Get a Free Quote").classes("text-4xl font-bold text-gray-900")
        ui.label(
            "Fill the form below and our team will contact you within 24 hours with a personalized quote."
        ).classes("text-gray-600")

        with ui.card().classes("w-full p-6 gap-4"):
            name = ui.input("Full Name *").classes("w-full")
            phone = ui.input("Phone Number *").classes("w-full")
            email = ui.input("Email").classes("w-full")
            city = ui.input("City").classes("w-full")
            pincode = ui.input("Pincode").classes("w-full")

            monthly_bill = ui.number("Monthly Bill (₹)", min=0).classes("w-full")
            system_size = ui.number("System Size (kW)", min=0).classes("w-full")

            system_type = ui.select(
                ["on-grid", "off-grid", "hybrid"],
                value="on-grid",
                label="System Type",
            ).classes("w-full")

            message = ui.textarea("Message / Requirements").classes("w-full")

            result_label = ui.label("").classes("text-sm mt-2")

            def submit():
                if not name.value or not phone.value:
                    result_label.set_text("Please fill name and phone.")
                    result_label.classes("text-red-600 text-sm")
                    return

                payload = {
                    "fullName": name.value,
                    "phone": phone.value,
                    "email": email.value or None,
                    "city": city.value or None,
                    "pincode": pincode.value or None,
                    "monthlyBill": float(monthly_bill.value) if monthly_bill.value else None,
                    "systemSizeKw": float(system_size.value) if system_size.value else None,
                    "systemType": system_type.value,
                    "message": message.value or None,
                    "sourceCode": "website",
                }

                resp = lead_service.create(payload)

                if resp.get("success"):
                    lead_num = resp.get("data", {}).get("lead_number", "")
                    result_label.set_text(f"✅ Thank you! Your request ID: {lead_num}. We will contact you soon.")
                    result_label.classes("text-green-600 text-sm")
                    name.value = ""
                    phone.value = ""
                    email.value = ""
                    city.value = ""
                    pincode.value = ""
                    monthly_bill.value = None
                    system_size.value = None
                    message.value = ""
                else:
                    err = resp.get("error", {}).get("message", "Something went wrong.")
                    result_label.set_text(f"❌ {err}")
                    result_label.classes("text-red-600 text-sm")

            ui.button("Submit Request", on_click=submit).classes(
                "bg-yellow-500 text-white font-semibold px-6 py-3 mt-4"
            )