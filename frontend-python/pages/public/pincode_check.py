"""
NP POWER TECH SOLAR - Pincode Serviceability Check
"""

from nicegui import ui
from layouts.public_layout import public_layout


# Placeholder serviceable pincodes (to be moved to DB via Admin Panel)
SERVICEABLE_PINCODES = {
    "110001": ("Delhi", "Central Delhi", "Delhi", True),
    "110002": ("Delhi", "Central Delhi", "Delhi", True),
    "110016": ("Delhi", "South Delhi", "Delhi", True),
    "400001": ("Mumbai", "Mumbai City", "Maharashtra", True),
    "400051": ("Mumbai", "Bandra", "Maharashtra", True),
    "411001": ("Pune", "Pune City", "Maharashtra", True),
    "411045": ("Pune", "Baner", "Maharashtra", True),
    "560001": ("Bengaluru", "Central", "Karnataka", True),
    "560037": ("Bengaluru", "Whitefield", "Karnataka", True),
    "500001": ("Hyderabad", "Central", "Telangana", True),
    "600001": ("Chennai", "Central", "Tamil Nadu", True),
}


@ui.page("/pincode-check")
def pincode_check_page():
    public_layout(current_page="/pincode-check")

    with ui.column().classes("w-full max-w-3xl mx-auto px-4 py-8 gap-6"):
        ui.label("Check Service Availability").classes("text-4xl font-bold text-gray-900")
        ui.label(
            "Enter your pincode to check if we serve your area for solar installation."
        ).classes("text-gray-600")

        with ui.card().classes("w-full p-6 gap-4"):
            pincode_input = ui.input("Enter Pincode", placeholder="e.g., 110001").classes("w-full")

            result_container = ui.column().classes("w-full mt-4 gap-3")

            def check_pincode():
                result_container.clear()
                pin = (pincode_input.value or "").strip()

                if not pin.isdigit() or len(pin) != 6:
                    with result_container:
                        ui.label("❌ Please enter a valid 6-digit pincode.").classes(
                            "text-red-600 font-semibold"
                        )
                    return

                info = SERVICEABLE_PINCODES.get(pin)

                with result_container:
                    if info:
                        city, area, state, available = info
                        ui.label("✅ Service Available!").classes(
                            "text-2xl font-bold text-green-600"
                        )
                        ui.separator()
                        with ui.row().classes("w-full justify-between py-1"):
                            ui.label("Pincode:").classes("text-gray-600")
                            ui.label(pin).classes("font-bold")
                        with ui.row().classes("w-full justify-between py-1"):
                            ui.label("City:").classes("text-gray-600")
                            ui.label(city).classes("font-bold")
                        with ui.row().classes("w-full justify-between py-1"):
                            ui.label("Area:").classes("text-gray-600")
                            ui.label(area).classes("font-bold")
                        with ui.row().classes("w-full justify-between py-1"):
                            ui.label("State:").classes("text-gray-600")
                            ui.label(state).classes("font-bold")

                        ui.separator()
                        ui.label(
                            "Great! We offer free site survey and installation in your area."
                        ).classes("text-gray-600 mt-2")
                        ui.button(
                            "Book Free Survey",
                            on_click=lambda: ui.navigate.to("/get-quote"),
                        ).classes("bg-yellow-500 text-white mt-3")

                    else:
                        ui.label("⚠️ Contact Required").classes(
                            "text-2xl font-bold text-orange-600"
                        )
                        ui.label(
                            f"We don't have confirmed service in pincode {pin} yet. "
                            "But we may still be able to help — please contact us."
                        ).classes("text-gray-600 mt-2")
                        ui.button(
                            "Contact Us",
                            on_click=lambda: ui.navigate.to("/contact"),
                        ).classes("bg-yellow-500 text-white mt-3")

            ui.button("Check Availability", on_click=check_pincode).classes(
                "bg-yellow-500 text-white font-semibold px-6 py-3 mt-2"
            )

        # Info
        ui.label("Service Areas").classes("text-xl font-bold mt-4")
        ui.label(
            "We currently serve Delhi NCR, Mumbai, Pune, Bengaluru, Hyderabad, Chennai "
            "and expanding. Enter your pincode to confirm."
        ).classes("text-gray-600 text-sm")