"""
NP POWER TECH SOLAR - Admin Dashboard
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.admin_service import admin_service
from api.client import api_client


@ui.page("/admin/dashboard")
def admin_dashboard():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    container = admin_layout(current_page="/admin/dashboard", page_title="Dashboard")

    with container:
        # Welcome
        ui.label("Welcome to Admin Dashboard").classes("text-3xl font-bold text-gray-900")
        ui.label("Overview of your solar business").classes("text-gray-500")

        # Stats cards container (will load from API)
        stats_container = ui.row().classes("w-full gap-4 flex-wrap mt-4")

        # Recent leads container
        ui.label("Recent Leads").classes("text-2xl font-bold mt-6")
        leads_container = ui.column().classes("w-full")

        def load_dashboard():
            # ---- STATS ----
            stats_container.clear()

            # Fetch counts from APIs
            leads_resp = admin_service.list_leads(limit=1)
            customers_resp = admin_service.list_customers(limit=1)
            products_resp = admin_service.list_products(limit=1)

            leads_count = leads_resp.get("data", {}).get("pagination", {}).get("total", 0) if leads_resp.get("success") else 0
            customers_count = customers_resp.get("data", {}).get("pagination", {}).get("total", 0) if customers_resp.get("success") else 0
            products_count = len(products_resp.get("data", [])) if products_resp.get("success") else 0

            with stats_container:
                # Leads card
                with ui.card().classes("flex-1 min-w-[200px] p-6 cursor-pointer hover:shadow-lg").on(
                    "click", lambda: ui.navigate.to("/admin/leads")
                ):
                    ui.label("Total Leads").classes("text-gray-500 text-sm")
                    ui.label(str(leads_count)).classes("text-4xl font-bold text-yellow-500 mt-2")

                # Customers card
                with ui.card().classes("flex-1 min-w-[200px] p-6 cursor-pointer hover:shadow-lg").on(
                    "click", lambda: ui.navigate.to("/admin/customers")
                ):
                    ui.label("Customers").classes("text-gray-500 text-sm")
                    ui.label(str(customers_count)).classes("text-4xl font-bold text-blue-500 mt-2")

                # Products card
                with ui.card().classes("flex-1 min-w-[200px] p-6 cursor-pointer hover:shadow-lg").on(
                    "click", lambda: ui.navigate.to("/admin/products")
                ):
                    ui.label("Products").classes("text-gray-500 text-sm")
                    ui.label(str(products_count)).classes("text-4xl font-bold text-green-500 mt-2")

                # Quotations card
                quotes_resp = admin_service.list_leads(limit=1)  # placeholder — we'll add quotations count later
                with ui.card().classes("flex-1 min-w-[200px] p-6 cursor-pointer hover:shadow-lg").on(
                    "click", lambda: ui.navigate.to("/admin/quotations")
                ):
                    ui.label("Quotations").classes("text-gray-500 text-sm")
                    ui.label("→").classes("text-4xl font-bold text-purple-500 mt-2")

            # ---- RECENT LEADS ----
            leads_container.clear()
            resp = admin_service.list_leads(limit=10)
            leads = resp.get("data", []) if resp.get("success") else []

            with leads_container:
                if not leads:
                    ui.label("No leads yet.").classes("text-gray-500 text-center p-8")
                    return

                rows_html = ""
                for l in leads:
                    rows_html += f"""
                    <tr class="border-b hover:bg-gray-50">
                        <td class="p-3">{l.get('lead_number', '—')}</td>
                        <td class="p-3">{l.get('full_name', '—')}</td>
                        <td class="p-3">{l.get('phone', '—')}</td>
                        <td class="p-3">{l.get('city', '—') or '—'}</td>
                        <td class="p-3">
                            <span class="px-2 py-1 text-xs rounded bg-yellow-100 text-yellow-700">
                                {l.get('status', '—')}
                            </span>
                        </td>
                        <td class="p-3 text-xs text-gray-500">{l.get('created_at', '')[:19]}</td>
                    </tr>
                    """

                ui.html(f"""
                <div class="overflow-x-auto rounded-lg shadow">
                    <table class="w-full bg-white">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="p-3 text-left text-sm font-semibold">Lead #</th>
                                <th class="p-3 text-left text-sm font-semibold">Name</th>
                                <th class="p-3 text-left text-sm font-semibold">Phone</th>
                                <th class="p-3 text-left text-sm font-semibold">City</th>
                                <th class="p-3 text-left text-sm font-semibold">Status</th>
                                <th class="p-3 text-left text-sm font-semibold">Created</th>
                            </tr>
                        </thead>
                        <tbody>{rows_html}</tbody>
                    </table>
                </div>
                """).classes("w-full")

        # Load dashboard on start
        ui.timer(0.5, load_dashboard, once=True)