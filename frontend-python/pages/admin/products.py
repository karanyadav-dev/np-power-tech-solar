"""
NP POWER TECH SOLAR - Admin Products List
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.admin_service import admin_service
from api.client import api_client


@ui.page("/admin/products")
def admin_products():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    container = admin_layout(current_page="/admin/products", page_title="Products")

    with container:
        # Header with Add button
        with ui.row().classes("w-full justify-between items-center"):
            with ui.column().classes("gap-0"):
                ui.label("Products Management").classes("text-2xl font-bold")
                ui.label("Add, edit, and manage your solar products").classes("text-sm text-gray-500")

            ui.button("+ Add Product", on_click=lambda: ui.navigate.to("/admin/products/new")).classes(
                "bg-yellow-500 text-white font-semibold"
            )

        # Search bar
        with ui.row().classes("w-full gap-3 items-center"):
            search_input = ui.input("Search products...").classes("w-80").props("outlined dense")
            refresh_btn = ui.button("Search", icon="search").classes("bg-gray-700 text-white")

        # Status / loading
        status_label = ui.label("Loading products...").classes("text-gray-500 text-sm")

        # Products table container
        products_container = ui.column().classes("w-full")

        def load_products(search=None):
            products_container.clear()
            status_label.set_text("Loading...")
            status_label.classes("text-gray-500 text-sm")

            try:
                if search:
                    resp = admin_service.list_products(limit=100, search=search)
                else:
                    resp = admin_service.list_products(limit=100)

                if not resp.get("success"):
                    err = resp.get("error", {}).get("message", "Failed to load")
                    status_label.set_text(f"❌ {err}")
                    status_label.classes("text-red-600 text-sm")
                    return

                products = resp.get("data", [])
                status_label.set_text(f"✅ {len(products)} products found")
                status_label.classes("text-green-600 text-sm")

                with products_container:
                    if not products:
                        ui.label("No products found.").classes("text-gray-500 text-center p-8")
                        return

                    # Use HTML table for reliability
                    rows_html = ""
                    for p in products:
                        pid = p.get("id", "")
                        name = p.get("name", "—")
                        brand = p.get("brand", "—") or "—"
                        capacity = p.get("capacity", "—") or "—"
                        price = float(p.get("price", 0) or 0)
                        available = "✅" if p.get("is_available") else "❌"
                        featured = "⭐" if p.get("is_featured") else ""

                        rows_html += f"""
                        <tr class="border-b hover:bg-gray-50">
                            <td class="p-3">{name} {featured}</td>
                            <td class="p-3">{brand}</td>
                            <td class="p-3">{capacity}</td>
                            <td class="p-3">₹ {price:,.0f}</td>
                            <td class="p-3 text-center">{available}</td>
                            <td class="p-3 text-center">
                                <a href="/admin/products/{pid}/edit"
                                   class="text-blue-600 hover:text-blue-800 mr-3 no-underline">
                                   ✏️ Edit
                                </a>
                                <span class="text-red-600 hover:text-red-800 cursor-pointer"
                                      onclick="if(confirm('Delete this product?'))
                                      window.location.href='/admin/products/{pid}/delete'">
                                      🗑️ Delete
                                </span>
                            </td>
                        </tr>
                        """

                    table_html = f"""
                    <div class="overflow-x-auto">
                    <table class="w-full bg-white rounded-lg shadow">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="p-3 text-left">Name</th>
                                <th class="p-3 text-left">Brand</th>
                                <th class="p-3 text-left">Capacity</th>
                                <th class="p-3 text-left">Price</th>
                                <th class="p-3 text-center">Available</th>
                                <th class="p-3 text-center">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                    </div>
                    """

                    ui.html(table_html).classes("w-full")

            except Exception as e:
                status_label.set_text(f"❌ Error: {str(e)}")
                status_label.classes("text-red-600 text-sm")

        refresh_btn.on("click", lambda: load_products(search_input.value))
        search_input.on("keydown.enter", lambda: load_products(search_input.value))

        # Load on page start
        ui.timer(0.3, lambda: load_products(), once=True)


@ui.page("/admin/products/{product_id}/delete")
def admin_product_delete(product_id: str):
    """Handle delete via URL."""
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    resp = admin_service.delete_product(product_id)
    if resp.get("success"):
        ui.notify("Product deleted", type="positive")
    else:
        ui.notify("Delete failed", type="negative")

    ui.navigate.to("/admin/products")