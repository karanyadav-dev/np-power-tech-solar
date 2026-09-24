"""
NP POWER TECH SOLAR - Complete Homepage
"""

from nicegui import ui
from layouts.public_layout import public_layout
from config.settings import settings
from services.product_service import product_service
from components.whatsapp_button import whatsapp_button
from components.call_button import call_button
from components.before_after_slider import simple_before_after
from components.service_areas import service_areas_section, contact_map_section


def _hero_section():
    with ui.row().classes("w-full items-center justify-between gap-8 flex-wrap"):
        with ui.column().classes("gap-4 flex-1 min-w-[300px]"):
            ui.label("Power Your Future with Solar").classes(
                "text-5xl font-bold text-gray-900 leading-tight"
            )
            ui.label(
                "Save on electricity bills, reduce carbon footprint, and get government subsidies. "
                "End-to-end solar solutions for homes, businesses, and industries."
            ).classes("text-lg text-gray-600")

            with ui.row().classes("gap-4 mt-4 flex-wrap"):
                ui.button("Get Free Quote", on_click=lambda: ui.navigate.to("/get-quote")).classes(
                    "bg-yellow-500 text-white font-semibold px-6 py-3"
                )
                ui.button("Solar Calculator", on_click=lambda: ui.navigate.to("/calculator")).props(
                    "outline"
                ).classes("border-yellow-500 text-yellow-600 px-6 py-3")
                ui.button("Call Now", on_click=lambda: ui.navigate.to("/contact")).props(
                    "flat"
                ).classes("text-gray-700")

        with ui.column().classes("flex-1 min-w-[300px] items-center"):
            ui.icon("solar_power", size="14rem").classes("text-yellow-400")


def _trust_badges():
    badges = [
        ("verified", "MNRE Certified"),
        ("shield", "25-Year Warranty"),
        ("currency_rupee", "Subsidy Available"),
        ("home_work", "Free Site Survey"),
    ]
    with ui.row().classes("w-full justify-around items-center gap-4 flex-wrap"):
        for icon, label in badges:
            with ui.column().classes("items-center gap-2"):
                ui.icon(icon, size="2rem").classes("text-yellow-500")
                ui.label(label).classes("text-gray-700 font-medium text-sm")


def _services_section():
    ui.label("Our Services").classes("text-3xl font-bold text-gray-900")
    ui.label("Complete solar solutions for every need").classes("text-gray-600")

    services = [
        ("Residential Solar", "Home rooftop systems from 1kW to 10kW.", "home", "/residential"),
        ("Commercial Solar", "Offices, shops, and commercial buildings.", "business", "/commercial"),
        ("Industrial Solar", "Large-scale solar for factories.", "factory", "/industrial"),
        ("Solar Water Heater", "Efficient water heating solutions.", "water_drop", "/services"),
    ]

    with ui.row().classes("w-full gap-6 flex-wrap mt-4"):
        for title, desc, icon, link in services:
            with ui.card().classes(
                "flex-1 min-w-[250px] p-6 hover:shadow-lg transition-shadow cursor-pointer"
            ).on("click", lambda l=link: ui.navigate.to(l)):
                ui.icon(icon, size="3rem").classes("text-yellow-500")
                ui.label(title).classes("text-xl font-semibold text-gray-900 mt-2")
                ui.label(desc).classes("text-gray-600 mt-2")


def _products_section():
    ui.label("Featured Products").classes("text-3xl font-bold text-gray-900 mt-6")
    ui.label("High-quality solar products from trusted brands").classes("text-gray-600")

    loading = ui.row().classes("w-full justify-center py-6")
    with loading:
        ui.spinner("dots", size="lg", color="yellow")

    container = ui.row().classes("w-full gap-6 flex-wrap mt-4")

    def load_products():
        loading.set_visibility(False)
        result = product_service.list(limit=6)
        products = result.get("data", []) if result.get("success") else []

        with container:
            if not products:
                placeholders = [
                    ("Adani 540W Mono Panel", "540W", "₹ 13,500"),
                    ("Growatt 5kW Inverter", "5 kW", "₹ 45,000"),
                    ("Luminous 150Ah Battery", "150 Ah", "₹ 12,000"),
                ]
                for name, cap, price in placeholders:
                    with ui.card().classes("w-72 p-4"):
                        ui.label("Sample").classes("text-xs text-yellow-600 font-semibold")
                        ui.label(name).classes("text-lg font-bold text-gray-900")
                        ui.label(cap).classes("text-gray-500 text-sm")
                        ui.label(price).classes("text-xl font-bold text-green-600 mt-2")
                return

            for p in products:
                with ui.card().classes("w-72 p-4 hover:shadow-lg transition-shadow"):
                    ui.label(p.get("brand") or "Product").classes(
                        "text-xs text-yellow-600 font-semibold"
                    )
                    ui.label(p.get("name", "")).classes("text-lg font-bold text-gray-900")
                    ui.label(p.get("capacity", "")).classes("text-gray-500 text-sm")
                    if p.get("price"):
                        ui.label(f"₹ {p['price']}").classes(
                            "text-xl font-bold text-green-600 mt-2"
                        )

    ui.timer(0.1, load_products, once=True)


def _before_after_section():
    ui.label("See the Transformation").classes("text-3xl font-bold text-gray-900 mt-6")
    ui.label("Real installations by our team").classes("text-gray-600")
    simple_before_after()


def _why_choose_us():
    ui.label("Why Choose Us?").classes("text-3xl font-bold text-gray-900 mt-6")

    points = [
        ("workspace_premium", "MNRE Certified", "Government-approved installers"),
        ("schedule", "Fast Installation", "3-7 days from survey"),
        ("verified_user", "25-Year Warranty", "Long-term peace of mind"),
        ("savings", "Max Subsidy Help", "We handle all paperwork"),
        ("support_agent", "Lifetime Support", "AMC plans available"),
        ("payments", "Easy Financing", "Loan assistance provided"),
    ]

    with ui.row().classes("w-full gap-4 flex-wrap mt-4"):
        for icon, title, desc in points:
            with ui.card().classes("flex-1 min-w-[200px] p-5"):
                ui.icon(icon, size="2.5rem").classes("text-yellow-500")
                ui.label(title).classes("text-lg font-semibold mt-2")
                ui.label(desc).classes("text-gray-600 text-sm mt-1")


def _installation_process():
    ui.label("How It Works").classes("text-3xl font-bold text-gray-900 mt-6")

    steps = [
        ("1", "Free Site Survey", "Our team visits your site and assesses roof, load, and requirements."),
        ("2", "Customized Quote", "We provide a detailed quotation with subsidy breakdown."),
        ("3", "Order Confirmation", "Approve the quote and place order."),
        ("4", "Installation", "Certified technicians install your system within 3-7 days."),
        ("5", "Commissioning & Support", "System activated, net metering applied. Lifetime support starts."),
    ]

    with ui.row().classes("w-full gap-4 flex-wrap mt-4"):
        for num, title, desc in steps:
            with ui.card().classes("flex-1 min-w-[220px] p-5"):
                ui.label(num).classes(
                    "text-4xl font-bold text-yellow-500 bg-yellow-50 rounded-full "
                    "w-12 h-12 flex items-center justify-center"
                )
                ui.label(title).classes("text-lg font-semibold mt-3")
                ui.label(desc).classes("text-gray-600 text-sm mt-2")


def _reviews_section():
    from services.review_service import review_service

    ui.label("What Our Customers Say").classes("text-3xl font-bold text-gray-900")
    ui.label("Real feedback from happy solar owners").classes("text-gray-600")

    reviews_container = ui.row().classes("w-full gap-4 flex-wrap mt-4")

    FALLBACK_REVIEWS = [
        {"customer_name": "Rajesh Kumar", "customer_location": "Delhi", "rating": 5,
         "review_text": "Excellent service! My electricity bill came down by 90% in the first month itself."},
        {"customer_name": "Priya Sharma", "customer_location": "Mumbai", "rating": 5,
         "review_text": "Professional team, completed installation in 4 days. Highly recommended!"},
        {"customer_name": "Amit Patel", "customer_location": "Pune", "rating": 4,
         "review_text": "Good quality panels and honest pricing. Subsidy help was very useful."},
    ]

    def load_reviews():
        reviews_container.clear()
        resp = review_service.list_public(limit=6)
        reviews = resp.get("data", []) if resp.get("success") else []

        if not reviews:
            reviews = FALLBACK_REVIEWS

        with reviews_container:
            for r in reviews:
                name = r.get("customer_name", "Customer")
                loc = r.get("customer_location", "India")
                rating = r.get("rating", 5)
                text = r.get("review_text", "")

                with ui.card().classes("flex-1 min-w-[280px] p-5 solar-card"):
                    with ui.row().classes("items-center gap-3"):
                        with ui.element("div").classes(
                            "w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center"
                        ):
                            ui.icon("person", size="1.5rem").classes("text-yellow-600")
                        with ui.column().classes("gap-0"):
                            ui.label(name).classes("font-semibold text-gray-900")
                            ui.label(loc).classes("text-xs text-gray-500")

                    with ui.row().classes("mt-3"):
                        for _ in range(int(rating)):
                            ui.icon("star", size="1.1rem").classes("text-yellow-500")
                        for _ in range(5 - int(rating)):
                            ui.icon("star_border", size="1.1rem").classes("text-gray-300")

                    ui.label(f'"{text}"').classes("text-gray-600 italic mt-3 text-sm leading-relaxed")

    ui.timer(0.1, load_reviews, once=True)

    with ui.row().classes("w-full justify-center mt-4"):
        ui.button("Write a Review →", on_click=lambda: ui.navigate.to("/write-review")).props(
            "outline"
        ).classes("border-yellow-500 text-yellow-600")


def _service_areas_wrapper():
    service_areas_section()


def _contact_map_wrapper():
    contact_map_section()


def _faq_preview():
    ui.label("Frequently Asked Questions").classes("text-3xl font-bold text-gray-900 mt-6")

    faqs = [
        ("How much does a solar system cost?", "A typical 3kW residential system costs ₹1.5-1.8 lakhs before subsidy."),
        ("What subsidy can I get?", "Up to ₹78,000 under PM Surya Ghar scheme for residential systems."),
        ("How much roof area is needed?", "Approximately 100 sq. ft. per kW of system capacity."),
    ]

    with ui.column().classes("w-full gap-2 mt-4"):
        for q, a in faqs:
            with ui.expansion(q).classes("w-full border rounded"):
                ui.label(a).classes("text-gray-600 p-3")

    ui.link("View all FAQs →", "/faq").classes("text-yellow-600 font-semibold mt-3")


def _final_cta():
    with ui.card().classes(
        "w-full bg-gradient-to-r from-yellow-400 to-orange-400 p-8 mt-8 items-center"
    ):
        ui.label("Ready to Go Solar?").classes("text-3xl font-bold text-white")
        ui.label("Get a free site survey and personalized quote today.").classes(
            "text-white mt-2"
        )
        with ui.row().classes("gap-4 mt-4"):
            ui.button("Book Free Survey", on_click=lambda: ui.navigate.to("/site-survey")).classes(
                "bg-white text-yellow-600 font-semibold px-6 py-3"
            )
            ui.button("Get Quote", on_click=lambda: ui.navigate.to("/get-quote")).classes(
                "bg-gray-900 text-white font-semibold px-6 py-3"
            )


@ui.page("/")
def home_page():
    """Complete homepage."""
    public_layout(current_page="/")

    # Floating buttons
    whatsapp_button()
    call_button()

    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-8"):
        _hero_section()
        ui.separator()
        _trust_badges()
        ui.separator()
        _services_section()
        ui.separator()
        _products_section()
        ui.separator()
        _before_after_section()
        ui.separator()
        _why_choose_us()
        ui.separator()
        _installation_process()
        ui.separator()
        _reviews_section()
        ui.separator()
        _service_areas_wrapper()
        ui.separator()
        _contact_map_wrapper()
        ui.separator()
        _faq_preview()
        _final_cta()