"""
NP POWER TECH SOLAR - Quotation Status (Customer View)
"""

from nicegui import ui
from layouts.public_layout import public_layout
from services.quotation_service import quotation_service


@ui.page("/quotation-status/{quotation_id}")
def quotation_status_page(quotation_id: str):
    public_layout(current_page="/quotation-status")

    with ui.column().classes("w-full max-w-4xl mx-auto px-4 py-8 gap-6"):
        ui.label("Quotation Status").classes("text-4xl font-bold text-gray-900")

        loading = ui.row().classes("w-full justify-center py-8")
        with loading:
            ui.spinner("dots", size="lg", color="yellow")

        content = ui.column().classes("w-full gap-4")

        def load():
            loading.set_visibility(False)
            resp = quotation_service.view_quotation(quotation_id)

            if not resp.get("success"):
                with content:
                    ui.label("❌ Quotation not found.").classes("text-red-600 text-lg")
                return

            q = resp.get("data", {})
            with content:
                with ui.card().classes("w-full p-6 gap-3"):
                    with ui.row().classes("w-full justify-between items-center"):
                        ui.label(f"Quotation #{q.get('quotation_number', '')}").classes(
                            "text-xl font-bold"
                        )
                        ui.chip(q.get("status", "").replace("_", " ")).classes(
                            "bg-yellow-100 text-yellow-800"
                        )

                    ui.separator()
                    ui.label(f"Customer: {q.get('customer_name', '')}").classes("text-gray-700")
                    ui.label(f"Phone: {q.get('customer_phone', '')}").classes("text-gray-700")
                    ui.label(f"System Size: {q.get('system_size_kw', '')} kW").classes("text-gray-700")

                    if q.get("final_amount"):
                        ui.label(f"Final Amount: ₹ {q['final_amount']}").classes(
                            "text-2xl font-bold text-green-600 mt-3"
                        )

                    if q.get("valid_until"):
                        ui.label(f"Valid Until: {q['valid_until']}").classes(
                            "text-sm text-gray-500 mt-2"
                        )

                # Accept/Reject buttons (if applicable)
                if q.get("status") in ["SENT_TO_CUSTOMER", "CUSTOMER_VIEWED"]:
                    with ui.card().classes("w-full p-6"):
                        ui.label("Your Response").classes("text-lg font-bold")
                        reason = ui.textarea("Reason (optional)").classes("w-full")

                        def accept():
                            resp = quotation_service.respond(quotation_id, "accept")
                            if resp.get("success"):
                                ui.notify("Quotation accepted! Our team will contact you.", type="positive")
                                ui.navigate.to(f"/quotation-status/{quotation_id}")
                            else:
                                ui.notify("Error accepting", type="negative")

                        def reject():
                            resp = quotation_service.respond(
                                quotation_id, "reject", reason.value
                            )
                            if resp.get("success"):
                                ui.notify("Quotation rejected.", type="info")
                                ui.navigate.to(f"/quotation-status/{quotation_id}")
                            else:
                                ui.notify("Error rejecting", type="negative")

                        with ui.row().classes("gap-3 mt-3"):
                            ui.button("✓ Accept", on_click=accept).classes("bg-green-500 text-white")
                            ui.button("✗ Reject", on_click=reject).classes("bg-red-500 text-white")

        ui.timer(0.1, load, once=True)