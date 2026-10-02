"""
NP POWER TECH SOLAR - Products Page
Click any product to start quotation with that product.
"""

from nicegui import ui
from layouts.public_layout import public_layout, public_layout_footer
from services.product_service import product_service
from config.settings import settings


@ui.page("/products")
def products_page():
    container = public_layout(current_page="/products")

    with container:
        ui.label("हमारे उत्पाद").classes("text-4xl font-bold text-gray-900")
        ui.label("भरोसेमंद ब्रांड्स के उच्च गुणवत्ता वाले सोलर उत्पाद").classes(
            "text-gray-600 text-lg"
        )

        with ui.row().classes("w-full gap-4 items-center mt-4 flex-wrap"):
            category_select = ui.select(
                {"": "सभी श्रेणियाँ"},
                value="",
                label="श्रेणी",
            ).classes("w-64").props("outlined dense")

            search_input = ui.input("खोजें...").classes("w-64").props("outlined dense")

            async def refresh():
                await load_products(category_select.value, search_input.value)

            ui.button("खोजें", icon="search", on_click=refresh).classes(
                "bg-yellow-500 text-white"
            ).style("color: white !important;")

        product_container = ui.row().classes("w-full gap-6 flex-wrap mt-6")

    async def load_products(category_id=None, search=None):
        product_container.clear()
        params = {"limit": 48}
        if category_id:
            params["categoryId"] = category_id
        if search:
            params["search"] = search

        result = product_service.list(**params)
        products = result.get("data", []) if result.get("success") else []

        with product_container:
            if not products:
                ui.label("कोई उत्पाद नहीं मिला।").classes("text-gray-500 text-center p-8 w-full")
                return

            for p in products:
                with ui.card().classes(
                    "w-72 p-4 hover:shadow-lg transition-shadow cursor-pointer"
                ).on("click", lambda pid=p["id"]: ui.navigate.to(f"/quotation-request?product={pid}")):
                    ui.label(p.get("category_name") or p.get("brand") or "उत्पाद").classes(
                        "text-xs text-yellow-600 font-semibold uppercase"
                    )

                    ui.label(p.get("name", "")).classes("text-lg font-bold text-gray-900 mt-1")

                    if p.get("capacity"):
                        ui.label(p["capacity"]).classes("text-sm text-gray-500")

                    if p.get("price"):
                        try:
                            price_val = float(p["price"])
                            ui.label(f" {price_val:,.0f}").classes(
                                "text-2xl font-bold text-green-600 mt-2"
                            )
                        except Exception:
                            ui.label(f" {p['price']}").classes(
                                "text-2xl font-bold text-green-600 mt-2"
                            )

                    if p.get("warranty_years"):
                        ui.label(f"{p['warranty_years']} साल वारंटी").classes(
                            "text-xs text-gray-400 mt-1"
                        )

                    ui.button(
                        "कोटेशन लें →",
                        on_click=lambda pid=p["id"]: ui.navigate.to(f"/quotation-request?product={pid}"),
                    ).classes("bg-yellow-500 text-white w-full mt-3").style("color: white !important;")

    def load_categories():
        result = product_service.list_categories()
        cats = result.get("data", []) if result.get("success") else []
        options = {"": "सभी श्रेणियाँ"}
        for c in cats:
            options[c["id"]] = c["name"]
        category_select.options = options
        category_select.update()

    ui.timer(0.1, load_categories, once=True)
    ui.timer(0.2, lambda: load_products(), once=True)

    public_layout_footer()