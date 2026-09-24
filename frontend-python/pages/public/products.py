"""
NP POWER TECH SOLAR - Products Page
"""

from nicegui import ui
from layouts.public_layout import public_layout
from services.product_service import product_service


@ui.page("/products")
def products_page():
    public_layout(current_page="/products")

    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-6"):
        ui.label("Our Products").classes("text-4xl font-bold text-gray-900")
        ui.label("High-quality solar products from trusted brands.").classes("text-gray-600")

        # Filters
        with ui.row().classes("w-full gap-4 items-center mt-4"):
            category_select = ui.select(
                {"": "All Categories"},
                value="",
                label="Category",
            ).classes("w-64")

            search_input = ui.input("Search...").classes("w-64")

            async def refresh():
                await load_products(category_select.value, search_input.value)

            ui.button("Search", on_click=refresh).classes("bg-yellow-500 text-white")

        # Product grid
        product_container = ui.row().classes("w-full gap-6 flex-wrap mt-6")

    async def load_products(category_id=None, search=None):
        product_container.clear()
        params = {"limit": 24}
        if category_id:
            params["categoryId"] = category_id
        if search:
            params["search"] = search

        result = product_service.list(**params)
        products = result.get("data", []) if result.get("success") else []

        with product_container:
            if not products:
                ui.label("No products found.").classes("text-gray-500")
                return

            for p in products:
                with ui.card().classes("w-72 p-4 hover:shadow-lg transition-shadow"):
                    ui.label(p.get("brand") or "Product").classes("text-xs text-yellow-600 font-semibold")
                    ui.label(p.get("name", "")).classes("text-lg font-bold text-gray-900 mt-1")
                    ui.label(p.get("capacity") or "").classes("text-sm text-gray-500")
                    if p.get("price"):
                        ui.label(f"₹ {p['price']}").classes("text-xl font-bold text-green-600 mt-2")
                    if p.get("warranty_years"):
                        ui.label(f"{p['warranty_years']} years warranty").classes("text-xs text-gray-400 mt-1")

    # Load categories
    def load_categories():
        result = product_service.list_categories()
        cats = result.get("data", []) if result.get("success") else []
        options = {"": "All Categories"}
        for c in cats:
            options[c["id"]] = c["name"]
        category_select.options = options
        category_select.update()

    ui.timer(0.1, load_categories, once=True)
    ui.timer(0.2, lambda: load_products(), once=True)