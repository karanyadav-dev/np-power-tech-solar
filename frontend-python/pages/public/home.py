"""
NP POWER TECH SOLAR - Complete Homepage (Village-Friendly)
"""

from nicegui import ui
from layouts.public_layout import public_layout, public_layout_footer
from config.settings import settings
from services.product_service import product_service
from services.settings_service import settings_service
from components.whatsapp_button import whatsapp_button
from components.call_button import call_button
from components.before_after_slider import simple_before_after
from components.service_areas import service_areas_section, contact_map_section


def _hero_section():
    """Village-friendly hero with BIG call-to-action buttons."""
    with ui.row().classes("w-full items-center justify-between gap-8 flex-wrap"):
        with ui.column().classes("gap-4 flex-1 min-w-[300px]"):
            ui.label("घर की छत पर सोलर लगवाएं").classes(
                "text-4xl md:text-5xl font-bold text-gray-900 leading-tight"
            )
            ui.label("बिजली का बिल कम करें, सरकारी सब्सिडी पाएं").classes(
                "text-xl md:text-2xl text-gray-700"
            )
            ui.label(
                "फ्री साइट सर्वे • सरकारी सब्सिडी सहायता • विशेषज्ञ इंस्टॉलेशन"
            ).classes("text-base text-gray-600")

            # BIG CTA buttons (only 2 - Call + WhatsApp)
            with ui.row().classes("gap-3 mt-6 flex-wrap"):
                ui.button(
                    "📞 अभी कॉल करें",
                    on_click=lambda: ui.run_javascript(
                        f'window.location.href="tel:{settings_service.get("company_phone", settings.PUBLIC_COMPANY_PHONE)}"'
                    ),
                ).classes("bg-yellow-500 text-white font-bold px-8 py-4 text-lg rounded-lg shadow-lg").style("color: white !important;")

                ui.button(
                    "💬 WhatsApp करें",
                    on_click=lambda: ui.run_javascript(
                        f'window.open("https://wa.me/{settings_service.get("company_phone", settings.PUBLIC_COMPANY_WHATSAPP).replace("+", "").replace("-", "").replace(" ", "")}", "_blank")'
                    ),
                ).classes("bg-green-500 text-white font-bold px-8 py-4 text-lg rounded-lg shadow-lg").style("color: white !important;")

        with ui.column().classes("flex-1 min-w-[200px] items-center"):
            ui.icon("solar_power", size="14rem").classes("text-yellow-400")


def _trust_badges():
    """4 trust badges - big icons, simple text."""
    badges = [
        ("verified", "सरकारी सब्सिडी", "₹78,000 तक"),
        ("schedule", "25 साल वारंटी", "लंबे समय तक"),
        ("home_work", "फ्री साइट सर्वे", "घर पर आकर"),
        ("savings", "कम बिजली बिल", "90% तक"),
    ]
    with ui.row().classes("w-full justify-around items-center gap-4 flex-wrap"):
        for icon, title, sub in badges:
            with ui.card().classes("flex-1 min-w-[180px] p-4 items-center text-center"):
                ui.icon(icon, size="3rem").classes("text-yellow-500")
                ui.label(title).classes("text-lg font-bold text-gray-800 mt-2")
                ui.label(sub).classes("text-sm text-gray-500")


def _how_it_works():
    """3-step process - VERY simple."""
    ui.label("ये कैसे काम करता है?").classes("text-3xl font-bold text-gray-900 mt-8")
    ui.label("सिर्फ 3 आसान स्टेप").classes("text-gray-600")

    steps = [
        ("1", "फ्री साइट सर्वे", "हमारी टीम आपके घर पर आकर छत देखकर सलाह देगी"),
        ("2", "मुफ्त कोटेशन", "आपकी ज़रूरत के हिसाब से रेट और सब्सिडी बताएंगे"),
        ("3", "इंस्टॉलेशन", "3-7 दिन में सोलर लगाकर आपको बिजली बचाना सिखाएंगे"),
    ]

    with ui.row().classes("w-full gap-4 flex-wrap mt-4"):
        for num, title, desc in steps:
            with ui.card().classes("flex-1 min-w-[220px] p-5 items-center text-center"):
                ui.label(num).classes(
                    "text-4xl font-bold text-yellow-500 bg-yellow-50 rounded-full "
                    "w-16 h-16 flex items-center justify-center"
                )
                ui.label(title).classes("text-xl font-bold mt-3")
                ui.label(desc).classes("text-gray-600 text-sm mt-2")


def _services_section():
    ui.label("हमारी सेवाएं").classes("text-3xl font-bold text-gray-900 mt-8")
    ui.label("हर ज़रूरत के लिए सोलर समाधान").classes("text-gray-600")

    services = [
        ("घर के लिए सोलर", "1kW से 10kW तक", "home", "/residential"),
        ("दुकान के लिए", "व्यापारिक सोलर", "storefront", "/commercial"),
        ("फैक्ट्री के लिए", "औद्योगिक सोलर", "factory", "/industrial"),
        ("सोलर वॉटर हीटर", "गर्म पानी", "water_drop", "/services"),
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
    ui.label("हमारे प्रोडक्ट्स").classes("text-3xl font-bold text-gray-900 mt-6")
    ui.label("भरोसेमंद ब्रांड्स के सोलर प्रोडक्ट्स").classes("text-gray-600")

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
                for name, cap, price in [
                    ("Adani 540W Panel", "540W", "₹13,500"),
                    ("Growatt 5kW Inverter", "5kW", "₹45,000"),
                    ("Luminous 150Ah Battery", "150Ah", "₹12,000"),
                ]:
                    with ui.card().classes("w-72 p-4"):
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
                        try:
                            price_val = float(p["price"])
                            ui.label(f"₹{price_val:,.0f}").classes(
                                "text-xl font-bold text-green-600 mt-2"
                            )
                        except Exception:
                            ui.label(f"₹{p['price']}").classes(
                                "text-xl font-bold text-green-600 mt-2"
                            )

    ui.timer(0.1, load_products, once=True)


def _subsidy_section():
    """Big subsidy banner - village-friendly."""
    with ui.card().classes(
        "w-full bg-gradient-to-r from-green-500 to-green-600 p-8 mt-8 items-center"
    ):
        ui.label("💰 सरकारी सब्सिडी पाएं").classes("text-3xl font-bold text-white")
        ui.label("₹78,000 तक की सब्सिडी").classes("text-5xl font-bold text-white mt-2")
        ui.label("PM सूर्य घर योजना के तहत").classes("text-white mt-2")
        ui.button(
            "सब्सिडी के बारे में और जानें →",
            on_click=lambda: ui.navigate.to("/subsidy"),
        ).classes("bg-white font-bold px-8 py-3 mt-4 text-lg").style(
            "color: #16a34a !important; background: white !important;"
        )


def _why_choose_us():
    ui.label("हमें क्यों चुनें?").classes("text-3xl font-bold text-gray-900 mt-6")

    points = [
        ("workspace_premium", "सरकारी मान्यता", "MNRE प्रमाणित"),
        ("schedule", "तेज़ इंस्टॉलेशन", "3-7 दिन में"),
        ("verified_user", "25 साल वारंटी", "पैनल की लंबी उम्र"),
        ("savings", "सब्सिडी में मदद", "पूरी प्रक्रिया में सहायता"),
        ("support_agent", "लाइफटाइम सपोर्ट", "AMC प्लान उपलब्ध"),
        ("payments", "आसान किश्तें", "लोन में सहायता"),
    ]

    with ui.row().classes("w-full gap-4 flex-wrap mt-4"):
        for icon, title, desc in points:
            with ui.card().classes("flex-1 min-w-[200px] p-5 items-center text-center"):
                ui.icon(icon, size="2.5rem").classes("text-yellow-500")
                ui.label(title).classes("text-lg font-semibold mt-2")
                ui.label(desc).classes("text-gray-600 text-sm mt-1")


def _reviews_section():
    """Reviews with customer-uploaded photos on top, name below."""
    from services.review_service import review_service

    ui.label("ग्राहक क्या कहते हैं?").classes("text-3xl font-bold text-gray-900")
    ui.label("हमारे संतुष्ट ग्राहकों के अनुभव").classes("text-gray-600")

    reviews_container = ui.row().classes("w-full gap-6 flex-wrap mt-4")

    def _full_url(relative_path: str) -> str:
        """Build full backend URL from relative path."""
        if not relative_path:
            return ""
        if relative_path.startswith("http"):
            return relative_path
        base = settings.BACKEND_API_BASE_URL.rstrip("/")
        path = relative_path if relative_path.startswith("/") else "/" + relative_path
        return base + path

    def load_reviews():
        reviews_container.clear()
        resp = review_service.list_public(limit=6)
        reviews = resp.get("data", []) if resp.get("success") else []

        if not reviews:
            with reviews_container:
                ui.label("अभी कोई रिव्यू नहीं है। पहले रिव्यू देने वाले बनें!").classes(
                    "text-gray-500 italic w-full text-center py-8"
                )
            return

        with reviews_container:
            for r in reviews:
                name = r.get("customer_name", "Customer")
                loc = r.get("customer_location", "India")
                rating = int(r.get("rating", 5) or 5)
                text = r.get("review_text", "")
                title = r.get("title", "")
                photos = r.get("photo_urls") or []

                # Parse JSON string if needed
                if isinstance(photos, str):
                    import json
                    try:
                        photos = json.loads(photos)
                    except Exception:
                        photos = []
                if not isinstance(photos, list):
                    photos = []

                with ui.card().classes(
                    "w-full md:w-[350px] p-0 overflow-hidden hover:shadow-lg transition-shadow"
                ):
                    # ---------- PHOTO ON TOP ----------
                    if photos:
                        photo_url = _full_url(photos[0])
                        with ui.element("div").classes(
                            "w-full h-48 bg-gray-100 overflow-hidden cursor-pointer"
                        ).on(
                            "click",
                            lambda u=photo_url: ui.run_javascript(
                                f'window.open("{u}", "_blank")'
                            ),
                        ):
                            ui.image(photo_url).classes(
                                "w-full h-full object-cover"
                            )
                    else:
                        # Fallback — no photo
                        with ui.element("div").classes(
                            "w-full h-48 bg-gradient-to-br from-yellow-100 to-yellow-200 "
                            "flex items-center justify-center"
                        ):
                            ui.icon("solar_power", size="5rem").classes("text-yellow-500")

                    # ---------- NAME + LOCATION BELOW ----------
                    with ui.column().classes("p-4 gap-1"):
                        with ui.row().classes("items-center gap-2 w-full"):
                            ui.icon("person", size="1.2rem").classes("text-yellow-600")
                            ui.label(name).classes("font-semibold text-gray-900 text-base")

                        ui.label(loc).classes("text-xs text-gray-500 ml-7")

                        # ---------- RATING ----------
                        with ui.row().classes("mt-2"):
                            for _ in range(rating):
                                ui.icon("star", size="1rem").classes("text-yellow-500")
                            for _ in range(5 - rating):
                                ui.icon("star_border", size="1rem").classes("text-gray-300")

                        # ---------- TITLE ----------
                        if title:
                            ui.label(f'"{title}"').classes(
                                "text-sm font-semibold text-gray-800 mt-2"
                            )

                        # ---------- REVIEW TEXT ----------
                        if text:
                            ui.label(f'"{text}"').classes(
                                "text-sm text-gray-600 italic mt-1 leading-relaxed"
                            )

    ui.timer(0.1, load_reviews, once=True)

    # CTA button
    with ui.row().classes("w-full justify-center mt-6"):
        ui.button(
            "अपनी रिव्यू लिखें →",
            on_click=lambda: ui.navigate.to("/write-review"),
        ).props("outline").classes("border-yellow-500 text-yellow-600")


def _faq_preview():
    ui.label("अक्सर पूछे जाने वाले सवाल").classes("text-3xl font-bold text-gray-900 mt-6")

    faqs = [
        ("सोलर सिस्टम की कीमत कितनी होती है?",
         "3kW का सिस्टम ₹1,50,000 - ₹1,80,000 का आता है (सब्सिडी से पहले)।"),
        ("सरकारी सब्सिडी कितनी मिलती है?",
         "PM सूर्य घर योजना के तहत ₹78,000 तक सब्सिडी मिल सकती है।"),
        ("छत पर कितनी जगह चाहिए?",
         "हर 1kW के लिए लगभग 100 वर्ग फुट जगह चाहिए।"),
    ]

    with ui.column().classes("w-full gap-2 mt-4"):
        for q, a in faqs:
            with ui.expansion(q).classes("w-full border rounded"):
                ui.label(a).classes("text-gray-600 p-3")

    ui.link("सभी सवाल देखें →", "/faq").classes("text-yellow-600 font-semibold mt-3")


def _final_cta():
    with ui.card().classes(
        "w-full bg-gradient-to-r from-yellow-400 to-orange-400 p-8 mt-8 items-center"
    ):
        ui.label("आज ही सोलर लगवाएं!").classes("text-3xl font-bold text-white")
        ui.label("फ्री साइट सर्वे और पर्सनल कोटेशन के लिए अभी संपर्क करें।").classes(
            "text-white mt-2 text-lg"
        )
        with ui.row().classes("gap-4 mt-6 flex-wrap justify-center"):
            ui.button(
                "📞 अभी कॉल करें",
                on_click=lambda: ui.run_javascript(
                    f'window.location.href="tel:{settings_service.get("company_phone", settings.PUBLIC_COMPANY_PHONE)}"'
                ),
            ).classes("bg-white font-bold px-8 py-4 text-lg").style(
                "color: #d97706 !important; background: white !important;"
            )

            ui.button(
                "💬 WhatsApp करें",
                on_click=lambda: ui.run_javascript(
                    f'window.open("https://wa.me/{settings_service.get("company_phone", settings.PUBLIC_COMPANY_WHATSAPP).replace("+", "").replace("-", "").replace(" ", "")}", "_blank")'
                ),
            ).classes("bg-gray-900 text-white font-bold px-8 py-4 text-lg").style("color: white !important;")


@ui.page("/")
def home_page():
    """Complete village-friendly homepage."""
    container = public_layout(current_page="/")

    # Floating buttons
    whatsapp_button()
    call_button()

    with container:
        _hero_section()
        ui.separator()
        _trust_badges()
        ui.separator()
        _how_it_works()
        ui.separator()
        _services_section()
        _products_section()
        ui.separator()
        _subsidy_section()
        ui.separator()
        _why_choose_us()
        ui.separator()
        _reviews_section()
        ui.separator()
        _faq_preview()
        _final_cta()

    # Footer
    public_layout_footer()