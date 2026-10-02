"""
NP POWER TECH SOLAR - Admin Dashboard
Stats + Recent Leads.
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.lead_service import lead_service
from services.admin_service import admin_service
from api.client import api_client


@ui.page("/admin/dashboard")
def admin_dashboard():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    user = app.storage.user.get("user", {})
    full_name = user.get("fullName", "Admin")

    container = admin_layout(current_page="/admin/dashboard", page_title="Dashboard")

    with container:
        ui.label(f"Welcome, {full_name}").classes("text-3xl font-bold")
        ui.label("Overview of your solar business").classes("text-sm text-gray-500")

        # ---------- Stats Cards ----------
        with ui.row().classes("w-full gap-4 flex-wrap mt-4"):
            with ui.card().classes("flex-1 min-w-[200px] p-6"):
                ui.label("Total Leads").classes("text-gray-500 text-sm")
                leads_count = ui.label("—").classes("text-3xl font-bold text-yellow-500")

            with ui.card().classes("flex-1 min-w-[200px] p-6"):
                ui.label("Customers").classes("text-gray-500 text-sm")
                customers_count = ui.label("—").classes("text-3xl font-bold text-blue-500")

            with ui.card().classes("flex-1 min-w-[200px] p-6"):
                ui.label("Products").classes("text-gray-500 text-sm")
                products_count = ui.label("—").classes("text-3xl font-bold text-green-500")

        # ---------- Recent Leads ----------
        ui.label("Recent Leads").classes("text-2xl font-bold mt-8")

        leads_table = ui.table(
            columns=[
                {"name": "lead_number", "label": "Lead #", "field": "lead_number", "align": "left"},
                {"name": "full_name", "label": "Name", "field": "full_name", "align": "left"},
                {"name": "phone", "label": "Phone", "field": "phone", "align": "left"},
                {"name": "city", "label": "City", "field": "city", "align": "left"},
                {"name": "status", "label": "Status", "field": "status", "align": "left"},
                {"name": "created_at", "label": "Created", "field": "created_at", "align": "left"},
            ],
            rows=[],
            row_key="lead_number",
        ).classes("w-full")

    # ---------- Load Data ----------
    def safe_count(resp):
        """Get count from API response — handles both list and dict."""
        if not resp or not resp.get("success"):
            return 0
        data = resp.get("data", [])
        if isinstance(data, list):
            return len(data)
        if isinstance(data, dict):
            return data.get("pagination", {}).get("total", 0)
        return 0

    def safe_list(resp):
        """Get list from API response — handles both list and dict."""
        if not resp or not resp.get("success"):
            return []
        data = resp.get("data", [])
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("data", [])
        return []

    def load_dashboard():
        # Leads
        try:
            leads_resp = lead_service.list(page=1, limit=10)
            leads_count.set_text(str(safe_count(leads_resp)))
            leads_list = safe_list(leads_resp)
            if leads_list:
                leads_table.rows = [
                    {
                        "lead_number": str(l.get("lead_number", "")),
                        "full_name": str(l.get("full_name", "")),
                        "phone": str(l.get("phone", "")),
                        "city": str(l.get("city", "") or "—"),
                        "status": str(l.get("status", "")),
                        "created_at": str(l.get("created_at", ""))[:19],
                    }
                    for l in leads_list[:10]
                ]
                leads_table.update()
        except Exception as e:
            print(f"[dashboard] leads error: {e}")
            leads_count.set_text("0")

        # Customers
        try:
            customers_resp = admin_service.list_customers(page=1, limit=1)
            customers_count.set_text(str(safe_count(customers_resp)))
        except Exception as e:
            print(f"[dashboard] customers error: {e}")
            customers_count.set_text("0")

        # Products
        try:
            products_resp = admin_service.list_products(page=1, limit=1)
            products_count.set_text(str(safe_count(products_resp)))
        except Exception as e:
            print(f"[dashboard] products error: {e}")
            products_count.set_text("0")

    ui.timer(0.3, load_dashboard, once=True)