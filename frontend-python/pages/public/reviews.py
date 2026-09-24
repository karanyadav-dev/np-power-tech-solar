"""
NP POWER TECH SOLAR - Customer Reviews
"""

from nicegui import ui
from layouts.public_layout import public_layout


# Placeholder reviews (to be fetched from API/DB in later phase)
PLACEHOLDER_REVIEWS = [
    {
        "name": "Rajesh Kumar",
        "location": "Delhi",
        "rating": 5,
        "title": "Excellent service and great savings",
        "text": "My electricity bill came down from ₹3,500 to ₹300 in the first month itself. The team was professional and completed installation on time.",
        "date": "2025-08-15",
    },
    {
        "name": "Priya Sharma",
        "location": "Mumbai",
        "rating": 5,
        "title": "Highly recommended!",
        "text": "Very professional team. They handled all the subsidy paperwork and completed installation in 4 days. Quality products and honest pricing.",
        "date": "2025-08-22",
    },
    {
        "name": "Amit Patel",
        "location": "Pune",
        "rating": 4,
        "title": "Good quality and service",
        "text": "The panels are working great. Only minor delay in installation due to rains, but overall satisfied with the quality and team's responsiveness.",
        "date": "2025-09-01",
    },
    {
        "name": "Sunita Verma",
        "location": "Bengaluru",
        "rating": 5,
        "title": "Best decision for my home",
        "text": "The entire process was smooth. Free site survey, transparent pricing, fast installation. Already recommended to my neighbors.",
        "date": "2025-09-10",
    },
    {
        "name": "Mohammed Ali",
        "location": "Hyderabad",
        "rating": 5,
        "title": "Professional and reliable",
        "text": "Team was very knowledgeable. They explained everything clearly. System working perfectly for 6 months now.",
        "date": "2025-09-15",
    },
    {
        "name": "Anjali Singh",
        "location": "Chennai",
        "rating": 4,
        "title": "Satisfied customer",
        "text": "Good quality products and fair pricing. Installation was clean and neat. Would recommend to others.",
        "date": "2025-09-18",
    },
]


@ui.page("/reviews")
def reviews_page():
    public_layout(current_page="/reviews")

    with ui.column().classes("w-full max-w-6xl mx-auto px-4 py-8 gap-6"):
        ui.label("Customer Reviews").classes("text-4xl font-bold text-gray-900")
        ui.label("See what our customers say about us.").classes("text-gray-600")

        # Rating summary
        with ui.card().classes("w-full p-6 items-center"):
            with ui.row().classes("items-center gap-4 flex-wrap justify-center"):
                ui.label("4.8").classes("text-6xl font-bold text-yellow-500")
                with ui.column().classes("gap-1"):
                    with ui.row():
                        for _ in range(5):
                            ui.icon("star", size="1.5rem").classes("text-yellow-500")
                    ui.label(f"Based on {len(PLACEHOLDER_REVIEWS)}+ verified reviews").classes(
                        "text-gray-600"
                    )

        # Reviews grid
        with ui.row().classes("w-full gap-4 flex-wrap"):
            for r in PLACEHOLDER_REVIEWS:
                with ui.card().classes("w-full md:w-96 p-5"):
                    with ui.row().classes("items-center gap-2"):
                        for _ in range(r["rating"]):
                            ui.icon("star", size="1.2rem").classes("text-yellow-500")
                        for _ in range(5 - r["rating"]):
                            ui.icon("star_border", size="1.2rem").classes("text-gray-300")

                    ui.label(f'"{r["title"]}"').classes("text-lg font-bold text-gray-900 mt-2")
                    ui.label(r["text"]).classes("text-gray-600 italic mt-2")
                    ui.separator()
                    ui.label(f"— {r['name']}, {r['location']}").classes(
                        "text-sm text-gray-500 mt-2"
                    )
                    ui.label(r["date"]).classes("text-xs text-gray-400")

        # CTA
        ui.separator()
        with ui.card().classes("w-full bg-yellow-50 p-6 items-center"):
            ui.label("Ready to Join Our Happy Customers?").classes("text-xl font-bold")
            ui.button("Get Free Quote", on_click=lambda: ui.navigate.to("/get-quote")).classes(
                "bg-yellow-500 text-white mt-3"
            )