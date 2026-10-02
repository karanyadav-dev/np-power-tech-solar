"""
NP POWER TECH SOLAR - Admin Reviews
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.admin_service import admin_service
from api.client import api_client
from config.settings import settings


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
        reviews_container = ui.column().classes("w-full gap-4")

        def load():
            reviews_container.clear()
            resp = admin_service.list_reviews(limit=100)
            reviews_data = resp.get("data", {})
            reviews = reviews_data.get("reviews", []) if isinstance(reviews_data, dict) else []
            loading.set_text(f"OK {len(reviews)} reviews found")
            loading.classes("text-green-600 text-sm")

            with reviews_container:
                if not reviews:
                    ui.label("No reviews yet").classes("text-gray-500 text-center p-8")
                    return

                for r in reviews:
                    with ui.card().classes("w-full p-5"):
                        with ui.row().classes("w-full justify-between items-center"):
                            with ui.row().classes("items-center gap-3"):
                                ui.icon("person", size="1.5rem").classes("text-yellow-500")
                                with ui.column().classes("gap-0"):
                                    ui.label(r.get("customer_name", "")).classes("font-bold")
                                    ui.label(r.get("customer_location", "") or "").classes("text-xs text-gray-500")

                            status = "Published" if r.get("is_published") else "Pending"
                            status_color = "bg-green-100 text-green-800" if r.get("is_published") else "bg-yellow-100 text-yellow-800"
                            ui.chip(status).classes(f"{status_color} text-xs")

                        with ui.row().classes("mt-2"):
                            for _ in range(int(r.get("rating", 0))):
                                ui.icon("star", size="1.1rem").classes("text-yellow-500")
                            for _ in range(5 - int(r.get("rating", 0))):
                                ui.icon("star_border", size="1.1rem").classes("text-gray-300")

                        if r.get("title"):
                            ui.label(r["title"]).classes("font-semibold mt-2")
                        ui.label(r.get("review_text", "")).classes("text-gray-700 mt-2")

                        # Photos section
                        photos = r.get("photo_urls") or []
                        if isinstance(photos, str):
                            import json
                            try:
                                photos = json.loads(photos)
                            except Exception:
                                photos = []
                        if not isinstance(photos, list):
                            photos = []

                        if photos:
                            ui.separator()
                            ui.label("Customer Photos:").classes("text-sm font-semibold text-gray-600 mt-2")
                            with ui.row().classes("gap-3 flex-wrap mt-1"):
                                for photo in photos:
                                    photo_url = photo if photo.startswith("/uploads") else f"/uploads/{photo}"
                                    full_url = f"{settings.BACKEND_API_BASE_URL}{photo_url}"
                                    ui.image(full_url).classes(
                                        "w-32 h-32 object-cover rounded cursor-pointer border"
                                    ).on(
                                        "click",
                                        lambda u=full_url: ui.run_javascript(f'window.open("{u}", "_blank")'),
                                    )

                        def make_publish_toggle(rid, current_state):
                            def toggle():
                                resp = admin_service.update_review(rid, {"isPublished": not current_state})
                                if resp.get("success"):
                                    ui.notify("Updated", type="positive")
                                    load()
                                else:
                                    ui.notify("Failed", type="negative")
                            return toggle

                        def make_delete(rid):
                            def do_delete():
                                resp = admin_service.delete_review(rid)
                                if resp.get("success"):
                                    ui.notify("Deleted", type="positive")
                                    load()
                                else:
                                    ui.notify("Delete failed", type="negative")
                            return do_delete

                        with ui.row().classes("gap-2 mt-3 flex-wrap"):
                            if r.get("is_published"):
                                ui.button(
                                    "Unpublish",
                                    on_click=make_publish_toggle(r["id"], True),
                                ).classes("bg-gray-500 text-white").style("color: white !important;")
                            else:
                                ui.button(
                                    "Publish",
                                    on_click=make_publish_toggle(r["id"], False),
                                ).classes("bg-green-500 text-white").style("color: white !important;")

                            ui.button(
                                "Delete",
                                on_click=make_delete(r["id"]),
                            ).classes("bg-red-500 text-white").style("color: white !important;")

        ui.timer(0.3, load, once=True)