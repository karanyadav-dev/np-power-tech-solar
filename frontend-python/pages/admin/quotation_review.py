"""
NP POWER TECH SOLAR - Admin Quotation Review
"""

from nicegui import ui, app
from services.quotation_service import quotation_service
from api.client import api_client


@ui.page("/admin/quotations")
def admin_quotations_list():
    # Auth check
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return

    api_client.set_token(token)

    with ui.header().classes("bg-gray-900 text-white py-3"):
        with ui.row().classes("w-full max-w-7xl mx-auto justify-between items-center px-4"):
            with ui.row().classes("items-center gap-2"):
                ui.icon("solar_power", size="1.5rem").classes("text-yellow-500")
                ui.label("Quotations").classes("text-lg font-bold")
            with ui.row().classes("gap-2"):
                ui.button("Dashboard", on_click=lambda: ui.navigate.to("/admin/dashboard")).props("flat").classes("text-white")
                ui.button("Logout", on_click=lambda: (app.storage.user.clear(), ui.navigate.to("/"))).props("flat").classes("text-white")

    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-6"):
        ui.label("Quotation Requests").classes("text-3xl font-bold")

        container = ui.column().classes("w-full")

        def load():
            container.clear()
            resp = quotation_service.list(limit=50)
            quotes = resp.get("data", []) if resp.get("success") else []

            with container:
                if not quotes:
                    ui.label("No quotations yet.").classes("text-gray-500")
                    return

                columns = [
                    {"name": "quotation_number", "label": "Quotation #", "field": "quotation_number", "align": "left"},
                    {"name": "customer_name", "label": "Customer", "field": "customer_name", "align": "left"},
                    {"name": "customer_city", "label": "City", "field": "customer_city", "align": "left"},
                    {"name": "system_size_kw", "label": "Size (kW)", "field": "system_size_kw", "align": "left"},
                    {"name": "status", "label": "Status", "field": "status", "align": "left"},
                    {"name": "actions", "label": "Actions", "field": "id", "align": "left"},
                ]
                rows = [{"id": q["id"], **q} for q in quotes]
                table = ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")

                table.add_slot("body-cell-actions", r"""
                    <q-td :props="props">
                        <q-btn dense color="primary" label="Review"
                               :href="'/admin/quotation/' + props.row.id" />
                    </q-td>
                """)

        ui.timer(0.1, load, once=True)


@ui.page("/admin/quotation/{quotation_id}")
def admin_quotation_detail(quotation_id: str):
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return

    api_client.set_token(token)

    with ui.column().classes("w-full max-w-5xl mx-auto px-4 py-8 gap-6"):
        ui.link("← Back to Quotations", "/admin/quotations").classes("text-yellow-600")

        container = ui.column().classes("w-full gap-4")

        def refresh():
            container.clear()
            resp = quotation_service.get(quotation_id)
            if not resp.get("success"):
                with container:
                    ui.label("Quotation not found").classes("text-red-600")
                return

            q = resp.get("data", {})

            with container:
                # Header
                with ui.card().classes("w-full p-6"):
                    with ui.row().classes("w-full justify-between items-center"):
                        ui.label(f"Quotation #{q.get('quotation_number')}").classes("text-2xl font-bold")
                        ui.chip(q.get("status")).classes("bg-yellow-100 text-yellow-800")

                    with ui.row().classes("gap-4 mt-2"):
                        ui.label(f"Customer: {q.get('customer_name')}").classes("text-gray-700")
                        ui.label(f"Phone: {q.get('customer_phone')}").classes("text-gray-700")
                        ui.label(f"City: {q.get('customer_city')}").classes("text-gray-700")
                        ui.label(f"Pincode: {q.get('customer_pincode')}").classes("text-gray-700")

                # Customer info
                with ui.card().classes("w-full p-6"):
                    ui.label("Customer Information").classes("text-xl font-bold mb-2")
                    with ui.column().classes("gap-1"):
                        ui.label(f"Name: {q.get('customer_name')}")
                        ui.label(f"Phone: {q.get('customer_phone')}")
                        ui.label(f"Email: {q.get('customer_email') or 'N/A'}")
                        ui.label(f"Address: {q.get('customer_address')}")

                # Solar & system
                with ui.card().classes("w-full p-6"):
                    ui.label("System Requirements").classes("text-xl font-bold mb-2")
                    ui.label(f"System Size: {q.get('system_size_kw')} kW")
                    ui.label(f"System Type: {q.get('system_type')}")

                # Items & pricing (if configured)
                if q.get("items"):
                    with ui.card().classes("w-full p-6"):
                        ui.label("Line Items").classes("text-xl font-bold mb-2")
                        for it in q["items"]:
                            with ui.row().classes("w-full justify-between border-b py-1"):
                                ui.label(f"{it['item_name']} × {it['quantity']}")
                                ui.label(f"₹ {it['total_price']}")
                        ui.separator()
                        ui.label(f"Subtotal: ₹ {q.get('subtotal', 0)}").classes("font-semibold")
                        ui.label(f"Discount: ₹ {q.get('discount', 0)}")
                        ui.label(f"GST: ₹ {q.get('gst_amount', 0)}")
                        ui.label(f"Subsidy: ₹ {q.get('subsidy_amount', 0)}")
                        ui.label(f"Final: ₹ {q.get('final_amount', 0)}").classes("text-2xl font-bold text-green-600")

                # Actions based on status
                with ui.card().classes("w-full p-6"):
                    ui.label("Actions").classes("text-xl font-bold mb-3")
                    status = q.get("status")

                    def do_action(fn, *args, label=""):
                        try:
                            r = fn(*args)
                            if r.get("success"):
                                ui.notify(f"{label} OK", type="positive")
                                refresh()
                            else:
                                ui.notify(f"{label} failed: {r.get('error', {}).get('message', '')}", type="negative")
                        except Exception as e:
                            ui.notify(f"Error: {e}", type="negative")

                    with ui.row().classes("gap-2 flex-wrap"):
                        if status == "CUSTOMER_SUBMITTED":
                            ui.button("Start Review",
                                      on_click=lambda: do_action(quotation_service.start_review, quotation_id, label="Review")).classes("bg-yellow-500 text-white")
                        if status == "ADMIN_REVIEW":
                            ui.button("Verify Info",
                                      on_click=lambda: do_action(quotation_service.verify_info, quotation_id, label="Verify")).classes("bg-green-500 text-white")
                        if status == "VERIFIED":
                            ui.button("Configure Pricing",
                                      on_click=lambda: ui.navigate.to(f"/admin/quotation/{quotation_id}/pricing")).classes("bg-blue-500 text-white")
                        if status == "PENDING_APPROVAL":
                            ui.button("Approve",
                                      on_click=lambda: do_action(quotation_service.approve, quotation_id, label="Approve")).classes("bg-green-600 text-white")
                        if status == "APPROVED":
                            ui.button("Mark PDF Generated",
                                      on_click=lambda: do_action(quotation_service.mark_pdf_generated, quotation_id, label="PDF")).classes("bg-purple-500 text-white")
                        if status == "PDF_GENERATED":
                            ui.button("Send to Customer",
                                      on_click=lambda: do_action(quotation_service.send_to_customer, quotation_id, label="Send")).classes("bg-orange-500 text-white")

        ui.timer(0.1, refresh, once=True)