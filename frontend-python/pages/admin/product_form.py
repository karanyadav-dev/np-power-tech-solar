"""
NP POWER TECH SOLAR - Add/Edit Product
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.admin_service import admin_service
from api.client import api_client


def _product_form(product_id=None):
    """Reusable form for add/edit."""
    is_edit = product_id is not None
    page_title = "Edit Product" if is_edit else "Add New Product"

    container = admin_layout(
        current_page="/admin/products",
        page_title=page_title,
    )

    with container:
        ui.link("← Back to Products", "/admin/products").classes("text-yellow-600 text-sm")

        ui.label(page_title).classes("text-2xl font-bold mt-2")

        # Load categories
        categories_resp = admin_service.list_categories()
        categories = categories_resp.get("data", []) if categories_resp.get("success") else []
        category_options = {c["id"]: c["name"] for c in categories}
        category_options[""] = "— No Category —"

        # Load existing data if edit
        existing = {}
        if is_edit:
            resp = admin_service.get_product(product_id)
            if resp.get("success"):
                existing = resp.get("data", {})

        with ui.card().classes("w-full max-w-3xl p-6 gap-4"):
            name = ui.input("Product Name *", value=existing.get("name", "")).classes("w-full").props("outlined dense")
            slug = ui.input("Slug (URL-friendly) *", value=existing.get("slug", "")).classes("w-full").props("outlined dense")
            category_id = ui.select(category_options, value=existing.get("category_id", ""), label="Category").classes("w-full").props("outlined dense")
            brand = ui.input("Brand", value=existing.get("brand", "")).classes("w-full").props("outlined dense")
            model = ui.input("Model", value=existing.get("model", "")).classes("w-full").props("outlined dense")
            capacity = ui.input("Capacity (e.g., 540W, 3kW)", value=existing.get("capacity", "")).classes("w-full").props("outlined dense")
            price = ui.number("Price (₹)", value=float(existing.get("price", 0) or 0), min=0).classes("w-full").props("outlined dense")
            warranty = ui.number("Warranty (years)", value=int(existing.get("warranty_years", 0) or 0), min=0).classes("w-full").props("outlined dense")
            description = ui.textarea("Description", value=existing.get("description", "")).classes("w-full").props("outlined dense")

            with ui.row().classes("gap-4"):
                is_available = ui.checkbox("Available", value=existing.get("is_available", True))
                is_featured = ui.checkbox("Featured on Homepage", value=existing.get("is_featured", False))

            result_label = ui.label("").classes("text-sm")

            def save():
                if not name.value or not slug.value:
                    result_label.set_text("Name and slug are required")
                    result_label.classes("text-red-600")
                    return

                payload = {
                    "name": name.value,
                    "slug": slug.value.lower().replace(" ", "-"),
                    "categoryId": category_id.value or None,
                    "brand": brand.value or None,
                    "model": model.value or None,
                    "capacity": capacity.value or None,
                    "price": float(price.value) if price.value else None,
                    "warrantyYears": int(warranty.value) if warranty.value else None,
                    "description": description.value or None,
                    "isAvailable": bool(is_available.value),
                    "isFeatured": bool(is_featured.value),
                }

                if is_edit:
                    resp = admin_service.update_product(product_id, payload)
                    success_msg = "Product updated"
                else:
                    resp = admin_service.create_product(payload)
                    success_msg = "Product created"

                if resp.get("success"):
                    ui.notify(success_msg, type="positive")
                    ui.navigate.to("/admin/products")
                else:
                    err = resp.get("error", {}).get("message", "Failed")
                    result_label.set_text(f"❌ {err}")
                    result_label.classes("text-red-600")

            with ui.row().classes("gap-3 mt-3"):
                ui.button("Cancel", on_click=lambda: ui.navigate.to("/admin/products")).props("outline")
                ui.button("Save Product", on_click=save).classes("bg-yellow-500 text-white font-semibold")


@ui.page("/admin/products/new")
def admin_product_new():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)
    _product_form(None)


@ui.page("/admin/products/{product_id}/edit")
def admin_product_edit(product_id: str):
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)
    _product_form(product_id)