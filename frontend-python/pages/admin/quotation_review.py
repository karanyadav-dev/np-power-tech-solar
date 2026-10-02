"""
NP POWER TECH SOLAR - Admin Quotations
List + Detail + Review actions with new admin layout.
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.quotation_service import quotation_service
from services.whatsapp_service import whatsapp_service
from config.settings import settings
from api.client import api_client


# ============================================================
# QUOTATIONS LIST
# ============================================================
@ui.page("/admin/quotations")
def admin_quotations_list():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    container = admin_layout(current_page="/admin/quotations", page_title="Quotations")

    with container:
        ui.label("Quotation Requests").classes("text-2xl font-bold")
        ui.label("Review, approve, and manage customer quotations").classes("text-sm text-gray-500")

        loading = ui.label("Loading...").classes("text-gray-500")
        quotes_container = ui.column().classes("w-full")

        def load():
            quotes_container.clear()
            loading.set_text("Loading...")
            loading.classes("text-gray-500 text-sm")

            resp = quotation_service.list(limit=50)
            quotes = resp.get("data", []) if resp.get("success") else []
            loading.set_text(f"OK - {len(quotes)} quotations found")
            loading.classes("text-green-600 text-sm")

            with quotes_container:
                if not quotes:
                    ui.label("No quotations yet.").classes("text-gray-500 text-center p-8")
                    return

                rows_html = ""
                for q in quotes:
                    qnum = q.get("quotation_number", "-")
                    cust = q.get("customer_name", "-")
                    city = q.get("customer_city", "-") or "-"
                    size = q.get("system_size_kw", "-")
                    amount = float(q.get("final_amount", 0) or 0)
                    status = q.get("status", "-")
                    qid = q.get("id", "")

                    status_color = "bg-yellow-100 text-yellow-800"
                    if status == "CUSTOMER_ACCEPTED":
                        status_color = "bg-green-100 text-green-800"
                    elif status == "CUSTOMER_REJECTED":
                        status_color = "bg-red-100 text-red-800"
                    elif status == "APPROVED":
                        status_color = "bg-blue-100 text-blue-800"

                    rows_html += f"""
                    <tr class="border-b hover:bg-gray-50">
                        <td class="p-3 font-mono text-xs">{qnum}</td>
                        <td class="p-3">{cust}</td>
                        <td class="p-3">{city}</td>
                        <td class="p-3">{size} kW</td>
                        <td class="p-3">Rs {amount:,.0f}</td>
                        <td class="p-3">
                            <span class="px-2 py-1 rounded text-xs {status_color}">{status}</span>
                        </td>
                        <td class="p-3 text-center">
                            <a href="/admin/quotation/{qid}"
                               class="text-blue-600 hover:text-blue-800 no-underline text-xs font-semibold">
                                Review
                            </a>
                        </td>
                    </tr>
                    """

                ui.html(f"""
                <div class="overflow-x-auto">
                <table class="w-full bg-white rounded-lg shadow">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="p-3 text-left">Quotation #</th>
                            <th class="p-3 text-left">Customer</th>
                            <th class="p-3 text-left">City</th>
                            <th class="p-3 text-left">Size</th>
                            <th class="p-3 text-left">Amount</th>
                            <th class="p-3 text-left">Status</th>
                            <th class="p-3 text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
                </div>
                """).classes("w-full")

        ui.timer(0.3, load, once=True)


# ============================================================
# QUOTATION DETAIL
# ============================================================
@ui.page("/admin/quotation/{quotation_id}")
def admin_quotation_detail(quotation_id: str):
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    container = admin_layout(current_page="/admin/quotations", page_title="Quotation Detail")

    with container:
        ui.link("<- Back to Quotations", "/admin/quotations").classes("text-yellow-600 text-sm no-underline")

        main = ui.column().classes("w-full gap-4 mt-2")

        def refresh():
            main.clear()
            resp = quotation_service.get(quotation_id)
            if not resp.get("success"):
                with main:
                    ui.label("Quotation not found").classes("text-red-600 text-lg")
                return

            q = resp.get("data", {})

            with main:
                # ---------- Header ----------
                with ui.card().classes("w-full p-5"):
                    with ui.row().classes("w-full justify-between items-center"):
                        with ui.column().classes("gap-0"):
                            ui.label(f"Quotation #{q.get('quotation_number')}").classes("text-2xl font-bold")
                            ui.label(f"Created: {q.get('created_at', '')[:19]}").classes("text-xs text-gray-500")
                        ui.chip(q.get("status", "")).classes("bg-yellow-100 text-yellow-800 text-sm")

                    ui.separator()

                    with ui.row().classes("gap-6 mt-2 flex-wrap"):
                        with ui.column().classes("gap-0"):
                            ui.label("Customer").classes("text-xs text-gray-500")
                            ui.label(q.get("customer_name", "-")).classes("font-semibold")
                        with ui.column().classes("gap-0"):
                            ui.label("Phone").classes("text-xs text-gray-500")
                            ui.label(q.get("customer_phone", "-")).classes("font-semibold")
                        with ui.column().classes("gap-0"):
                            ui.label("City").classes("text-xs text-gray-500")
                            ui.label(q.get("customer_city", "-") or "-").classes("font-semibold")
                        with ui.column().classes("gap-0"):
                            ui.label("System Size").classes("text-xs text-gray-500")
                            ui.label(f"{q.get('system_size_kw', '-')} kW").classes("font-semibold")
                        with ui.column().classes("gap-0"):
                            ui.label("Type").classes("text-xs text-gray-500")
                            ui.label(q.get("system_type", "-") or "-").classes("font-semibold")

                # ---------- Line Items ----------
                if q.get("items"):
                    with ui.card().classes("w-full p-5"):
                        ui.label("Line Items").classes("text-lg font-bold mb-2")
                        rows_html = ""
                        for it in q["items"]:
                            rows_html += f"""
                            <tr class="border-b">
                                <td class="p-2">{it.get('item_name', '')}</td>
                                <td class="p-2 text-center">{it.get('quantity', 0)}</td>
                                <td class="p-2 text-right">Rs {float(it.get('unit_price', 0)):,.0f}</td>
                                <td class="p-2 text-right font-semibold">Rs {float(it.get('total_price', 0)):,.0f}</td>
                            </tr>
                            """
                        ui.html(f"""
                        <table class="w-full">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="p-2 text-left">Item</th>
                                    <th class="p-2 text-center">Qty</th>
                                    <th class="p-2 text-right">Price</th>
                                    <th class="p-2 text-right">Total</th>
                                </tr>
                            </thead>
                            <tbody>{rows_html}</tbody>
                        </table>
                        """).classes("w-full")

                        ui.separator()
                        with ui.column().classes("items-end gap-1 mt-2"):
                            ui.label(f"Subtotal: Rs {float(q.get('subtotal', 0)):,.0f}")
                            ui.label(f"Discount: - Rs {float(q.get('discount', 0)):,.0f}")
                            ui.label(f"GST: Rs {float(q.get('gst_amount', 0)):,.0f}")
                            ui.label(f"Subsidy: - Rs {float(q.get('subsidy_amount', 0)):,.0f}")
                            ui.label(f"Final Amount: Rs {float(q.get('final_amount', 0)):,.0f}").classes(
                                "text-xl font-bold text-green-600 mt-2"
                            )

                # ---------- PDF / WhatsApp Section ----------
                if q.get("pdf_url"):
                    with ui.card().classes("w-full p-5 bg-green-50 border-2 border-green-300"):
                        ui.label("Send via WhatsApp").classes("text-lg font-bold text-green-800")
                        ui.label("PDF is ready. Send to customer via WhatsApp:").classes(
                            "text-sm text-gray-600 mt-1"
                        )

                        pdf_abs_url = f"{settings.BACKEND_API_BASE_URL}/api/v1/quotations/{quotation_id}/pdf/download"

                        wa_link = whatsapp_service.send_quotation_pdf(
                            phone=q.get("customer_phone", ""),
                            quotation_number=q.get("quotation_number", ""),
                            pdf_url=pdf_abs_url,
                            amount=float(q.get("final_amount", 0) or 0),
                        )

                        with ui.row().classes("gap-3 mt-3 flex-wrap"):
                            ui.button(
                                "Send on WhatsApp",
                                on_click=lambda: ui.run_javascript(f'window.open("{wa_link}", "_blank")'),
                            ).classes("bg-green-500 text-white font-semibold")

                            ui.button(
                                "Preview PDF",
                                on_click=lambda: ui.run_javascript(f'window.open("{pdf_abs_url}", "_blank")'),
                            ).props("outline").classes("border-blue-500 text-blue-600")

                            def copy_link():
                                ui.run_javascript(
                                    f'navigator.clipboard.writeText("{pdf_abs_url}"); '
                                    f'alert("Link copied: {pdf_abs_url}")'
                                )
                            ui.button("Copy Link", on_click=copy_link).props(
                                "outline"
                            ).classes("border-gray-500 text-gray-600")
                else:
                    with ui.card().classes("w-full p-5 bg-yellow-50"):
                        ui.label("PDF not generated yet").classes("text-yellow-800 font-semibold")
                        ui.label("Click 'Generate PDF' below to create the quotation PDF.").classes(
                            "text-sm text-gray-600"
                        )
                        ui.button(
                            "Generate PDF",
                            on_click=lambda: generate_pdf(),
                        ).classes("bg-yellow-500 text-white mt-2")

                # ---------- Action Functions ----------
                def generate_pdf():
                    try:
                        print(f"[PDF] Calling API for: {quotation_id}")
                        r = quotation_service.generate_pdf(quotation_id)
                        print(f"[PDF] Response: {r}")
                        if r.get("success"):
                            ui.notify("PDF generated successfully", type="positive")
                            try:
                                refresh()
                            except Exception as refresh_err:
                                print(f"[PDF] refresh() failed: {refresh_err}")
                                ui.navigate.to(f"/admin/quotation/{quotation_id}")
                        else:
                            err = r.get("error", {}).get("message", "PDF generation failed")
                            ui.notify(f"Failed: {err}", type="negative")
                            print(f"[PDF] Failed: {err}")
                    except Exception as e:
                        print(f"[PDF] Exception: {e}")
                        ui.notify(f"Error: {str(e)}", type="negative")

                def do_action(fn, *args, label="Action", **kwargs):
                    try:
                        r = fn(*args, **kwargs)
                        if r.get("success"):
                            ui.notify(f"{label} successful", type="positive")
                            refresh()
                        else:
                            err = r.get("error", {}).get("message", "Failed")
                            ui.notify(f"{err}", type="negative")
                    except Exception as e:
                        ui.notify(f"Error: {e}", type="negative")

                # ---------- Actions ----------
                with ui.card().classes("w-full p-5"):
                    ui.label("Actions").classes("text-lg font-bold mb-3")
                    status = q.get("status")

                    with ui.row().classes("gap-2 flex-wrap"):
                        if status == "CUSTOMER_SUBMITTED":
                            ui.button(
                                "Start Review",
                                on_click=lambda: do_action(quotation_service.start_review, quotation_id, label="Review started"),
                            ).classes("bg-yellow-500 text-white")
                        if status == "ADMIN_REVIEW":
                            ui.button(
                                "Verify Info",
                                on_click=lambda: do_action(quotation_service.verify_info, quotation_id, label="Verified"),
                            ).classes("bg-green-500 text-white")
                        if status == "VERIFIED":
                            ui.button(
                                "Configure Pricing",
                                on_click=lambda: ui.navigate.to(f"/admin/quotation/{quotation_id}/pricing"),
                            ).classes("bg-blue-500 text-white")
                        if status == "PENDING_APPROVAL":
                            ui.button(
                                "Approve",
                                on_click=lambda: do_action(quotation_service.approve, quotation_id, label="Approved"),
                            ).classes("bg-green-600 text-white")
                        if status == "APPROVED":
                            ui.button(
                                "Generate PDF", on_click=generate_pdf
                            ).classes("bg-purple-500 text-white")
                        if status == "PDF_GENERATED":
                            ui.button(
                                "Send to Customer",
                                on_click=lambda: do_action(quotation_service.send_to_customer, quotation_id, label="Sent"),
                            ).classes("bg-orange-500 text-white")

        ui.timer(0.3, refresh, once=True)