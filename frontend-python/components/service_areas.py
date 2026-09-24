"""
NP POWER TECH SOLAR - Service Areas Component
"""

from nicegui import ui


CITIES = [
    {"name": "Delhi NCR", "pincodes": "11xxxx", "status": "available"},
    {"name": "Mumbai", "pincodes": "40xxxx", "status": "available"},
    {"name": "Pune", "pincodes": "41xxxx", "status": "available"},
    {"name": "Bengaluru", "pincodes": "56xxxx", "status": "available"},
    {"name": "Hyderabad", "pincodes": "50xxxx", "status": "available"},
    {"name": "Chennai", "pincodes": "60xxxx", "status": "available"},
    {"name": "Ahmedabad", "pincodes": "38xxxx", "status": "coming_soon"},
    {"name": "Jaipur", "pincodes": "30xxxx", "status": "coming_soon"},
    {"name": "Lucknow", "pincodes": "22xxxx", "status": "coming_soon"},
]


def service_areas_section():
    """Display service areas in a grid with status chips."""
    ui.label("Our Service Areas").classes("text-3xl font-bold text-gray-900")
    ui.label("We're expanding rapidly across India. Check if we serve your city:").classes("text-gray-600")

    with ui.row().classes("w-full gap-3 flex-wrap mt-4"):
        for city in CITIES:
            with ui.card().classes("min-w-[180px] p-4 flex-1"):
                with ui.row().classes("items-center gap-2"):
                    ui.icon(
                        "location_on",
                        size="1.2rem"
                    ).classes("text-yellow-500")
                    ui.label(city["name"]).classes("font-semibold text-gray-800")

                if city["status"] == "available":
                    ui.label(f'✓ Available ({city["pincodes"]})').classes(
                        "text-xs text-green-600 font-medium mt-1"
                    )
                else:
                    ui.label(f'⏳ Coming soon ({city["pincodes"]})').classes(
                        "text-xs text-orange-600 font-medium mt-1"
                    )

    with ui.row().classes("items-center gap-2 mt-4"):
        ui.icon("info", size="1.2rem").classes("text-blue-500")
        ui.label("Don't see your city? ").classes("text-gray-600")
        ui.link("Check your pincode →", "/pincode-check").classes("text-yellow-600 font-semibold")


def contact_map_section():
    """Contact info + placeholder for Google Map."""
    ui.label("Visit Us").classes("text-3xl font-bold text-gray-900")

    with ui.row().classes("w-full gap-6 flex-wrap mt-4"):
        # Contact info
        with ui.card().classes("flex-1 min-w-[300px] p-6"):
            ui.label("Get in Touch").classes("text-xl font-bold")
            with ui.column().classes("gap-3 mt-3"):
                with ui.row().classes("items-center gap-3"):
                    ui.icon("phone", size="1.3rem").classes("text-yellow-500")
                    ui.label("+91-XXXX-XXXXXX (Update in settings)").classes("text-gray-700")

                with ui.row().classes("items-center gap-3"):
                    ui.icon("email", size="1.3rem").classes("text-yellow-500")
                    ui.label("contact@nppowertech.com").classes("text-gray-700")

                with ui.row().classes("items-center gap-3"):
                    ui.icon("schedule", size="1.3rem").classes("text-yellow-500")
                    ui.label("Mon-Sat: 9:00 AM - 6:00 PM").classes("text-gray-700")

        # Map placeholder
        with ui.card().classes("flex-1 min-w-[300px] p-0 overflow-hidden"):
            with ui.element("div").classes(
                "w-full h-64 bg-gradient-to-br from-blue-100 to-green-100 "
                "flex items-center justify-center"
            ):
                with ui.column().classes("items-center gap-2"):
                    ui.icon("map", size="4rem").classes("text-gray-400")
                    ui.label("Map placeholder").classes("text-gray-500 text-sm")
                    ui.label("(Google Maps embed to be added)").classes("text-gray-400 text-xs")