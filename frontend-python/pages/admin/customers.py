"""
NP POWER TECH SOLAR - Admin Customers
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.admin_service import admin_service
from api.client import api_client


@ui.page("/admin/customers")
def admin_customers():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    container = admin_layout(current_page="/admin/customers", page_title="Customers")

    with container:
        ui.label("Customers Management").classes("text-2xl font-bold")
        ui.label("View and manage all customers").classes("text-sm text-gray-500")

        loading = ui.label("Loading...").classes("text-gray-500")
        customers_container = ui.column().classes("w-full")

        def load():
            customers_container.clear()
            resp = admin_service.list_customers(limit=100)
            customers = resp.get("data", []) if resp.get("success") else []
            loading.set_text(f"✅ {len(customers)} customers found")
            loading.classes("text-green-600 text-sm")

            with customers_container:
                if not customers:
                    ui.label("No customers yet").classes("text-gray-500 text-center p-8")
                    return

                rows_html = ""
                for c in customers:
                    rows_html += f"""
                    <tr class="border-b hover:bg-gray-50">
                        <td class="p-3">{c.get('full_name', '—')}</td>
                        <td class="p-3">{c.get('phone', '—')}</td>
                        <td class="p-3">{c.get('email', '—') or '—'}</td>
                        <td class="p-3">{c.get('city', '—') or '—'}</td>
                        <td class="p-3">{c.get('customer_type', '—')}</td>
                    </tr>
                    """

                ui.html(f"""
                <div class="overflow-x-auto">
                <table class="w-full bg-white rounded-lg shadow">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="p-3 text-left">Name</th>
                            <th class="p-3 text-left">Phone</th>
                            <th class="p-3 text-left">Email</th>
                            <th class="p-3 text-left">City</th>
                            <th class="p-3 text-left">Type</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
                </div>
                """).classes("w-full")

        ui.timer(0.3, load, once=True)