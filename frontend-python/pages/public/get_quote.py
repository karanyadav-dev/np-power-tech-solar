"""
NP POWER TECH SOLAR - Get Quote Page
Redirects to full wizard.
"""

from nicegui import ui
from layouts.public_layout import public_layout, public_layout_footer


@ui.page("/get-quote")
def get_quote_page():
    container = public_layout(current_page="/get-quote")

    with container:
        ui.label("सोलर कोटेशन लें").classes("text-4xl font-bold text-gray-900")
        ui.label(
            "7 आसान स्टेप भरें और अपना कोटेशन पाएं। सिर्फ 2 मिनट में!"
        ).classes("text-lg text-gray-600")

        with ui.card().classes("w-full max-w-3xl mx-auto p-8 items-center bg-yellow-50 mt-4"):
            ui.icon("solar_power", size="4rem").classes("text-yellow-500")
            ui.label("सोलर लगवाने के लिए तैयार?").classes("text-2xl font-bold mt-4")
            ui.label(
                "हमारा कोटेशन विज़ार्ड आपके सिस्टम, बिजली उपयोग, छत की जानकारी "
                "और ज़रूरी दस्तावेज़ पूछता है - जिससे सटीक कोटेशन मिल सके।"
            ).classes("text-gray-600 text-center mt-2")

            ui.button(
                "कोटेशन विज़ार्ड शुरू करें →",
                on_click=lambda: ui.navigate.to("/quotation-request"),
            ).classes(
                "bg-yellow-500 text-white font-semibold px-8 py-4 mt-6 text-lg"
            ).style("color: white !important;")

        ui.separator().classes("my-6")

        with ui.row().classes("w-full gap-6 flex-wrap justify-center"):
            with ui.card().classes("flex-1 min-w-[250px] p-5 items-center text-center"):
                ui.icon("schedule", size="2rem").classes("text-yellow-500")
                ui.label("2 मिनट का काम").classes("font-semibold mt-2")
                ui.label("7 आसान सवाल").classes("text-gray-500 text-sm")

            with ui.card().classes("flex-1 min-w-[250px] p-5 items-center text-center"):
                ui.icon("upload_file", size="2rem").classes("text-yellow-500")
                ui.label("बिल और फोटो अपलोड").classes("font-semibold mt-2")
                ui.label("सटीकता के लिए").classes("text-gray-500 text-sm")

            with ui.card().classes("flex-1 min-w-[250px] p-5 items-center text-center"):
                ui.icon("support_agent", size="2rem").classes("text-yellow-500")
                ui.label("24 घंटे में कॉलबैक").classes("font-semibold mt-2")
                ui.label("हम संपर्क करेंगे").classes("text-gray-500 text-sm")

    public_layout_footer()