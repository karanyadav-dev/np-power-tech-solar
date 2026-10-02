"""
NP POWER TECH SOLAR - Admin Layout
Sidebar + top bar with back button + logo.
"""

import base64
from pathlib import Path
from nicegui import ui, app
from config.settings import settings


def _get_logo_base64():
    """Read logo file and convert to base64 data URI."""
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
    if logo_path.exists():
        try:
            with open(logo_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{b64}"
        except Exception:
            return None
    return None


NAV_ITEMS = [
    ("Dashboard", "/admin/dashboard", "dashboard"),
    ("Leads", "/admin/leads", "people"),
    ("Customers", "/admin/customers", "contacts"),
    ("Quotations", "/admin/quotations", "request_quote"),
    ("Products", "/admin/products", "inventory_2"),
    ("Reviews", "/admin/reviews", "star"),
    ("Uploads", "/admin/uploads", "folder"),
    ("Settings", "/admin/settings", "settings"),
]


def admin_layout(current_page: str = "/admin/dashboard", page_title: str = "Admin"):
    """Apply admin layout with sidebar + logo + back button."""

    # Auth check
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return None

    # Set token in API client for all admin pages
    from api.client import api_client
    api_client.set_token(token)

    user = app.storage.user.get("user", {})
    full_name = user.get("fullName", "Admin")

    logo_uri = _get_logo_base64()

    # Left sidebar
    with ui.left_drawer(value=True).classes("bg-gray-900 text-white p-0").props("width=240"):
        with ui.column().classes("w-full gap-0 h-full"):
            # Brand + Logo (centered, larger)
            with ui.column().classes("items-center gap-2 p-4 border-b border-gray-700 w-full"):
                if logo_uri:
                    ui.html(
                        f'<img src="{logo_uri}" style="height: 60px; width: auto; background: white; border-radius: 8px; padding: 6px;" alt="Logo" />'
                    )
                else:
                    ui.icon("solar_power", size="2rem").classes("text-yellow-500")
                ui.label("Admin Panel").classes("text-sm font-bold text-white mt-1")

            # Back to site button
            with ui.row().classes(
                "w-full items-center gap-3 px-4 py-3 text-sm no-underline cursor-pointer "
                "hover:bg-gray-800 text-gray-300 border-b border-gray-700"
            ).on("click", lambda: ui.navigate.to("/")):
                ui.icon("arrow_back", size="1.2rem")
                ui.label("Back to Website")

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