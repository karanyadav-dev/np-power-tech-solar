"""
NP POWER TECH SOLAR - Admin Dashboard (Basic)
"""

from nicegui import ui, app
from services.lead_service import lead_service
from services.auth_service import auth_service
from config.settings import settings


@ui.page("/admin/dashboard")
def admin_dashboard():
    # Check auth
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return

    user = app.storage.user.get("user", {})

    # Set token for API calls
    from api.client import api_client
    api_client.set_token(token)

    # Header
    with ui.header().classes("bg-gray-900 text-white py-3"):
        with ui.row().classes("w-full max-w-7xl mx-auto justify-between items-center px-4"):
            with ui.row().classes("items-center gap-2"):
                ui.icon("solar_power", size="1.5rem").classes("text-yellow-500")
                ui.label("Admin Dashboard").classes("text-lg font-bold")

            with ui.row().classes("items-center gap-4"):
                ui.label(f"👤 {user.get('fullName', 'Admin')}").classes("text-sm")
                def logout():
                    auth_service.logout()
                    app.storage.user.clear()
                    ui.navigate.to("/")
                ui.button("Logout", on_click=logout).props("flat").classes("text-white")

    # Body
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-6"):
        ui.label("Welcome to Admin Dashboard").classes("text-3xl font-bold")

        # Stats cards
        with ui.row().classes("w-full gap-4 flex-wrap"):
            with ui.card().classes("flex-1 min-w-[200px] p-6"):
                ui.label("Total Leads").classes("text-gray-500 text-sm")
                leads_count = ui.label("—").classes("text-3xl font-bold text-yellow-500")
            with ui.card().classes("flex-1 min-w-[200px] p-6"):
                ui.label("Customers").classes("text-gray-500 text-sm")
                ui.label("—").classes("text-3xl font-bold text-blue-500")
            with ui.card().classes("flex-1 min-w-[200px] p-6"):
                ui.label("Products").classes("text-gray-500 text-sm")
                ui.label("—").classes("text-3xl font-bold text-green-500")

        # Leads table
        ui.label("Recent Leads").classes("text-2xl font-bold mt-4")

        leads_container = ui.column().classes("w-full")

        def load_leads():
            leads_container.clear()
            resp = lead_service.list(page=1, limit=20)
            leads = resp.get("data", []) if resp.get("success") else []

            with leads_container:
                if not leads:
                    ui.label("No leads yet.").classes("text-gray-500")
                    leads_count.set_text("0")
                    return

                leads_count.set_text(str(len(leads)))

                columns = [
                    {"name": "lead_number", "label": "Lead #", "field": "lead_number", "align": "left"},
                    {"name": "full_name", "label": "Name", "field": "full_name", "align": "left"},
                    {"name": "phone", "label": "Phone", "field": "phone", "align": "left"},
                    {"name": "city", "label": "City", "field": "city", "align": "left"},
                    {"name": "status", "label": "Status", "field": "status", "align": "left"},
                    {"name": "created_at", "label": "Created", "field": "created_at", "align": "left"},
                ]
                rows = [{"id": l["id"], **l} for l in leads]
                ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")

        ui.timer(0.1, load_leads, once=True)