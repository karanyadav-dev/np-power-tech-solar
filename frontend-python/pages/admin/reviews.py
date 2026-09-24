"""
NP POWER TECH SOLAR - Admin Reviews
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.admin_service import admin_service
from api.client import api_client


@ui.page("/admin/reviews")
def admin_reviews():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    container = admin_layout(current_page="/admin/reviews", page_title="Reviews")

    with container:
        ui.label("Reviews Management").classes("text-2xl font-bold")
        ui.label("Approve, reject, and manage customer reviews").classes("text-sm text-gray-500")

        loading = ui.label("Loading...").classes("text-gray-500")
        reviews_container = ui.column().classes("w-full")

        def load():
            reviews_container.clear()
            resp = admin_service.list_reviews(limit=100)
            reviews = resp.get("data", {}).get("reviews", []) if resp.get("success") else []
            loading.set_text(f"✅ {len(reviews)} reviews found")
            loading.classes("text-green-600 text-sm")

            with reviews_container:
                if not reviews:
                    ui.label("No reviews yet").classes("text-gray-500 text-center p-8")
                    return

                for r in reviews:
                    with ui.card().classes("w-full p-4"):
                        with ui.row().classes("justify-between items-center"):
                            ui.label(f"{r.get('customer_name', '')} — {r.get('rating', 0)}⭐").classes("font-bold")
                            status = "✅ Published" if r.get("is_published") else "⏳ Pending"
                            ui.chip(status).classes("bg-yellow-100 text-xs")

                        ui.label(r.get("review_text", "")).classes("text-gray-600 mt-2")

                        def make_toggle(rid, current_state):
                            def toggle():
                                resp = admin_service.update_review(rid, {"isPublished": not current_state})
                                if resp.get("success"):
                                    ui.notify("Updated", type="positive")
                                    load()
                            return toggle

                        ui.button(
                            "Unpublish" if r.get("is_published") else "Publish",
                            on_click=make_toggle(r["id"], r.get("is_published", False)),
                        ).classes("bg-yellow-500 text-white mt-2")

        ui.timer(0.3, load, once=True)