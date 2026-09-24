"""
NP POWER TECH SOLAR - Admin Layout
Sidebar + top bar with back button for all admin pages.
"""

from nicegui import ui, app
from config.settings import settings


# Only include pages that EXIST
NAV_ITEMS = [
    ("Dashboard", "/admin/dashboard", "dashboard"),
    ("Leads", "/admin/leads", "people"),
    ("Customers", "/admin/customers", "contacts"),
    ("Quotations", "/admin/quotations", "request_quote"),
    ("Products", "/admin/products", "inventory_2"),
    ("Reviews", "/admin/reviews", "star"),
    ("Uploads", "/admin/uploads", "folder"),
]


def admin_layout(current_page: str = "/admin/dashboard", page_title: str = "Admin"):
    """Apply admin layout with sidebar + back button."""

    # Auth check
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return None

    # CRITICAL: Set token in API client so all admin API calls work
    from api.client import api_client
    api_client.set_token(token)

    # Debug log (can remove in production)
    print(f"[ADMIN_LAYOUT] Token set: {token[:30]}...")

    user = app.storage.user.get("user", {})
    full_name = user.get("fullName", "Admin")

    # Left sidebar
    with ui.left_drawer(value=True).classes("bg-gray-900 text-white p-0").props("width=240"):
        with ui.column().classes("w-full gap-0 h-full"):
            # Brand
            with ui.row().classes("items-center gap-2 p-4 border-b border-gray-700"):
                ui.icon("solar_power", size="1.5rem").classes("text-yellow-500")
                ui.label("Admin Panel").classes("text-lg font-bold text-white")

            # Back to site button
            with ui.row().classes(
                "w-full items-center gap-3 px-4 py-3 text-sm no-underline cursor-pointer "
                "hover:bg-gray-800 text-gray-300 border-b border-gray-700"
            ).on("click", lambda: ui.navigate.to("/")):
                ui.icon("arrow_back", size="1.2rem")
                ui.label("← Back to Website")

            # Navigation
            for label, path, icon in NAV_ITEMS:
                is_active = current_page == path
                base_classes = (
                    "w-full flex items-center gap-3 px-4 py-3 text-sm no-underline "
                    "cursor-pointer hover:bg-gray-800"
                )
                if is_active:
                    base_classes += " bg-yellow-500 text-gray-900 font-semibold"
                else:
                    base_classes += " text-gray-300"

                with ui.row().classes(base_classes).on("click", lambda p=path: ui.navigate.to(p)):
                    ui.icon(icon, size="1.2rem")
                    ui.label(label)

            # Bottom — user + logout
            with ui.column().classes("w-full mt-auto p-4 border-t border-gray-700"):
                with ui.row().classes("items-center gap-2 mb-2"):
                    ui.icon("person", size="1.2rem").classes("text-gray-400")
                    ui.label(full_name).classes("text-xs text-gray-400")

                def logout():
                    app.storage.user.clear()
                    ui.navigate.to("/")

                ui.button("Logout", on_click=logout).props("flat dense").classes(
                    "text-white w-full"
                ).style("justify-content: flex-start")

    # Top bar
    with ui.header().classes("bg-white shadow-sm"):
        with ui.row().classes("w-full items-center justify-between px-4 py-2"):
            with ui.row().classes("items-center gap-3"):
                ui.button(icon="menu").props("flat dense").on(
                    "click", lambda: ui.left_drawer().toggle()
                )

                # Back button in header
                with ui.row().classes(
                    "items-center gap-1 cursor-pointer px-2 py-1 rounded hover:bg-gray-100"
                ).on("click", lambda: ui.navigate.to("/admin/dashboard")):
                    ui.icon("arrow_back", size="1.2rem").classes("text-gray-600")
                    ui.label("Back").classes("text-sm text-gray-600")

                ui.label(page_title).classes("text-xl font-bold text-gray-800 ml-2")

            with ui.row().classes("items-center gap-3"):
                ui.link("View Site →", "/").classes(
                    "text-sm text-gray-500 no-underline hover:text-yellow-500"
                )

    # Main content area
    with ui.column().classes("w-full p-6 gap-4") as container:
        pass

    return container