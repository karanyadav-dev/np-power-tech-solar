"""
NP POWER TECH SOLAR - Admin Leads
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.admin_service import admin_service
from api.client import api_client


@ui.page("/admin/leads")
def admin_leads():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    container = admin_layout(current_page="/admin/leads", page_title="Leads")

    with container:
        ui.label("Leads Management").classes("text-2xl font-bold")
        ui.label("View and manage all incoming leads").classes("text-sm text-gray-500")

        loading = ui.label("Loading...").classes("text-gray-500")

        leads_container = ui.column().classes("w-full")

        def load():
            leads_container.clear()
            resp = admin_service.list_leads(limit=100)
            leads = resp.get("data", []) if resp.get("success") else []
            loading.set_text(f"✅ {len(leads)} leads found")
            loading.classes("text-green-600 text-sm")

            with leads_container:
                if not leads:
                    ui.label("No leads yet").classes("text-gray-500 text-center p-8")
                    return

                rows_html = ""
                for l in leads:
                    rows_html += f"""
                    <tr class="border-b hover:bg-gray-50">
                        <td class="p-3">{l.get('lead_number', '—')}</td>
                        <td class="p-3">{l.get('full_name', '—')}</td>
                        <td class="p-3">{l.get('phone', '—')}</td>
                        <td class="p-3">{l.get('city', '—')}</td>
                        <td class="p-3">{l.get('status', '—')}</td>
                    </tr>
                    """

                ui.html(f"""
                <div class="overflow-x-auto">
                <table class="w-full bg-white rounded-lg shadow">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="p-3 text-left">Lead #</th>
                            <th class="p-3 text-left">Name</th>
                            <th class="p-3 text-left">Phone</th>
                            <th class="p-3 text-left">City</th>
                            <th class="p-3 text-left">Status</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
                </div>
                """).classes("w-full")

        ui.timer(0.3, load, once=True)