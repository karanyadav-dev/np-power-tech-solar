"""
NP POWER TECH SOLAR - Admin Quotation Pricing
Add line items + configure pricing + set all PDF fields.
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from services.quotation_service import quotation_service
from services.settings_service import settings_service
from api.client import api_client


@ui.page("/admin/quotation/{quotation_id}/pricing")
def admin_quotation_pricing(quotation_id: str):
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    container = admin_layout(current_page="/admin/quotations", page_title="Configure Pricing")

    resp = quotation_service.get(quotation_id)
    if not resp.get("success"):
        with container:
            ui.label("Quotation not found").classes("text-red-600 text-xl")
        return

    q = resp.get("data", {})
    items_state = []

    # Load existing global settings (public only)
    existing_settings = settings_service.get_public()

    # Load ALL settings (admin only) for pre-fill
    all_settings_resp = api_client.get("/api/v1/settings")
    all_settings = {}
    if all_settings_resp.get("success"):
        for s in all_settings_resp.get("data", []):
            all_settings[s["key"]] = s.get("value", "")

    with container:
        ui.link("<- Back to Quotation", f"/admin/quotation/{quotation_id}").classes(
            "text-yellow-600 text-sm no-underline"
        )

        ui.label(f"Configure Pricing — {q.get('quotation_number', '')}").classes(
            "text-2xl font-bold mt-2"
        )
        ui.label(f"Customer: {q.get('customer_name', '')} | System: {q.get('system_size_kw', '')} kW").classes(
            "text-sm text-gray-500"
        )

        # ============================================================
        # LINE ITEMS
        # ============================================================
        with ui.card().classes("w-full p-5 mt-4"):
            ui.label("Line Items (BOM)").classes("text-lg font-bold mb-3")

            items_container = ui.column().classes("w-full gap-2")

            def refresh_items():
                items_container.clear()
                with items_container:
                    if not items_state:
                        ui.label("No items yet. Click 'Add Item' below or 'Load Default BOM'.").classes(
                            "text-gray-500 italic"
                        )
                        return

                    with ui.row().classes("w-full gap-2 font-bold text-xs text-gray-600 border-b pb-1"):
                        ui.label("Technical Details").classes("flex-[3]")
                        ui.label("Make").classes("w-32")
                        ui.label("Capacity").classes("w-32")
                        ui.label("Qty").classes("w-20 text-center")
                        ui.label("Unit Price").classes("w-28 text-right")
                        ui.label("").classes("w-16")

                    for idx, it in enumerate(items_state):
                        with ui.row().classes("w-full gap-2 items-center"):
                            it["name_input"] = ui.input(value=it.get("name", ""), placeholder="Item name").classes("flex-[3]").props("outlined dense")
                            it["make_input"] = ui.input(value=it.get("make", "STANDARD")).classes("w-32").props("outlined dense")
                            it["capacity_input"] = ui.input(value=it.get("capacity", "-")).classes("w-32").props("outlined dense")
                            it["qty_input"] = ui.number(value=it.get("qty", 1), min=1, format="%.0f").classes("w-20").props("outlined dense")
                            it["price_input"] = ui.number(value=it.get("price", 0), min=0, format="%.0f").classes("w-28").props("outlined dense")

                            def make_delete(i):
                                def do_delete():
                                    items_state.pop(i)
                                    refresh_items()
                                return do_delete

                            ui.button(icon="delete", on_click=make_delete(idx)).props("flat dense color=negative").classes("w-16")

            def add_item():
                items_state.append({
                    "name": "",
                    "make": "STANDARD",
                    "capacity": "-",
                    "qty": 1,
                    "price": 0,
                })
                refresh_items()

            def load_default_bom():
                items_state.clear()
                defaults = [
                    {"name": "SOLAR MODULE", "make": "INA", "capacity": "600W", "qty": 5, "price": 13500},
                    {"name": "PCU/INVERTER", "make": "FESTON", "capacity": "5 KW", "qty": 1, "price": 45000},
                    {"name": "COMPLETE SET OF STRUCTURE", "make": "G. I STANDARD", "capacity": "TATA", "qty": 1, "price": 15000},
                    {"name": "DC CABLE", "make": "POLYCAB", "capacity": "1C*4sq mm", "qty": 1, "price": 3500},
                    {"name": "AC CABLE", "make": "POLYCAB", "capacity": "10sq mm", "qty": 1, "price": 2500},
                    {"name": "EARTHING SET WITH LA", "make": "STANDARD", "capacity": "SET", "qty": 3, "price": 1500},
                    {"name": "DCBB", "make": "STANDARD", "capacity": "SET", "qty": 1, "price": 4500},
                    {"name": "ACDB", "make": "STANDARD", "capacity": "SET", "qty": 1, "price": 5500},
                    {"name": "BALANCE OF SYSTEM", "make": "STANDARD", "capacity": "SET", "qty": 1, "price": 8000},
                    {"name": "NET/SOLAR METER", "make": "L&T", "capacity": "SET", "qty": 1, "price": 12000},
                ]
                for d in defaults:
                    items_state.append(d)
                refresh_items()

            with ui.row().classes("gap-3 mt-3"):
                ui.button("+ Add Item", on_click=add_item).classes("bg-blue-500 text-white")
                ui.button("Load Default BOM (10 items)", on_click=load_default_bom).classes("bg-gray-700 text-white")

        # ============================================================
        # COMMERCIALS
        # ============================================================
        with ui.card().classes("w-full p-5 mt-4"):
            ui.label("Commercials").classes("text-lg font-bold mb-3")

            with ui.row().classes("w-full gap-4 flex-wrap"):
                discount = ui.number("Discount (Rs)", value=0, min=0).classes("w-48").props("outlined")
                gst_pct = ui.number("GST %", value=18, min=0, max=28).classes("w-32").props("outlined")
                subsidy = ui.number("Subsidy (Rs)", value=78000, min=0).classes("w-48").props("outlined")
                validity = ui.number("Validity (days)", value=30, min=1).classes("w-40").props("outlined")

            with ui.row().classes("w-full gap-4 flex-wrap mt-3"):
                gst_status = ui.input("GST Paid Extra Status", value="NIL").classes("w-48").props("outlined")
                discom_status = ui.input("DISCOM Charge Status", value="INCLUDED").classes("w-48").props("outlined")

        # ============================================================
        # PAYMENT TERMS
        # ============================================================
        with ui.card().classes("w-full p-5 mt-4"):
            ui.label("Payment Terms").classes("text-lg font-bold mb-3")
            with ui.row().classes("w-full gap-4 flex-wrap"):
                pay_advance = ui.number("Advance %", value=10, min=0, max=100).classes("w-32").props("outlined")
                pay_delivery = ui.number("Before Delivery %", value=85, min=0, max=100).classes("w-40").props("outlined")
                pay_commissioning = ui.number("After Commissioning %", value=5, min=0, max=100).classes("w-48").props("outlined")

        # ============================================================
        # PROJECT COMPLETION + VALIDITY
        # ============================================================
        with ui.card().classes("w-full p-5 mt-4"):
            ui.label("Project Completion & Validity").classes("text-lg font-bold mb-3")

            with ui.row().classes("w-full gap-4 flex-wrap"):
                completion_days = ui.input("Completion Days", value="10-15").classes("w-40").props("outlined")
                completion_start = ui.input(
                    "Completion Start Condition",
                    value="FROM THE CLEAR ORDER AND ADVANCE PAYMENT",
                ).classes("flex-1").props("outlined")

            with ui.row().classes("w-full gap-4 flex-wrap mt-3"):
                validity_days = ui.input("Validity Days", value="2").classes("w-32").props("outlined")
                validity_msg = ui.input(
                    "Custom Validity Message (optional)",
                    value="AFTER THIS PERIOD A CONFIRMATION MUST BE TAKEN.",
                ).classes("flex-1").props("outlined")

        # ============================================================
        # WARRANTY
        # ============================================================
        with ui.card().classes("w-full p-5 mt-4"):
            ui.label("Warranty").classes("text-lg font-bold mb-3")

            warranty_system = ui.input(
                "Complete System Warranty",
                value="5 YEAR COMPLETE SYSTEM WARRANTY.",
            ).classes("w-full").props("outlined")

            warranty_module = ui.input(
                "Solar Module Performance Warranty",
                value="SOLAR MODULE PERFORMANCE WARRANTY 25 YEAR (AS PER MNRE NORMS)",
            ).classes("w-full mt-2").props("outlined")

            warranty_inverter = ui.input(
                "Solar Inverter Warranty",
                value="SOLAR INVERTER 10 YEAR.",
            ).classes("w-full mt-2").props("outlined")

            warranty_other = ui.input(
                "Other Warranty (optional)",
                value="",
            ).classes("w-full mt-2").props("outlined")

        # ============================================================
        # TRANSPORTATION + OFFICIAL FEES
        # ============================================================
        with ui.card().classes("w-full p-5 mt-4"):
            ui.label("Transportation & Official Fees").classes("text-lg font-bold mb-3")

            with ui.row().classes("w-full gap-4 flex-wrap"):
                transportation_status = ui.input("Transportation", value="INCLUDED").classes("w-48").props("outlined")
                transportation_details = ui.input("Transportation Details", value="").classes("flex-1").props("outlined")

            with ui.row().classes("w-full gap-4 flex-wrap mt-3"):
                official_fees = ui.input("Official Fees", value="AS APPLICABLE").classes("w-48").props("outlined")
                official_fees_amount = ui.input("Fee Amount", value="").classes("w-40").props("outlined")
                official_fees_details = ui.input("Fee Details", value="").classes("flex-1").props("outlined")

        # ============================================================
        # CLIENT SCOPE
        # ============================================================
        with ui.card().classes("w-full p-5 mt-4"):
            ui.label("Client Scope (8-10 points)").classes("text-lg font-bold mb-3")

            cs1 = ui.input("1. Solar Module Cleaning", value="CLEANING OF SOLAR MODULES IN YOUR SCOPE.").classes("w-full").props("outlined dense")
            cs2 = ui.input("2. Basic Training", value="ONE PERSON FROM CLIENT SIDE FOR BASIC TRAINING OF OPERATION OF SOLAR PV SYSTEM.").classes("w-full mt-2").props("outlined dense")
            cs3 = ui.input("3. Roof Arrangement", value="ROOF TO BE ARRANGED AND PROVIDED BY THE CLIENT.").classes("w-full mt-2").props("outlined dense")
            cs4 = ui.input("4. Electricity & Water", value="ELECTRICITY & WATER SHALL BE PROVIDED BY CLIENT DURING THE CONSTRUCTION.").classes("w-full mt-2").props("outlined dense")
            cs5 = ui.input("5. Material Storage", value="PROVIDE SAFE STORAGE SPACE FOR THE MATERIAL BEING USED FOR SOLAR POWER PLANT.").classes("w-full mt-2").props("outlined dense")
            cs6 = ui.input("6. Inverter Synchronization", value="PROVIDE ELECTRICITY SUPPLY TO SYNCHRONIZE THE INVERTER ON COMMISSIONING AND COMMISSIONING ONWARD.").classes("w-full mt-2").props("outlined dense")
            cs7 = ui.input("7. LT Panel Connection", value="PROVIDE CONNECTION SPACE IN THE LT PANEL TO CONNECT THE INVERTER OUTPUT.").classes("w-full mt-2").props("outlined dense")
            cs8 = ui.input("8. Internet Connection", value="INTERNET CONNECTION TO BE PROVIDED BY THE CLIENT FOR REMOTE MONITORING OF THE SYSTEM.").classes("w-full mt-2").props("outlined dense")
            cs9 = ui.input("9. Transportation", value="ALL TRANSPORTATION INCLUDED OF ABOVE MENTIONED BOM UP TO SITE OF INSTALLATION.").classes("w-full mt-2").props("outlined dense")
            cs10 = ui.input("10. Other (optional)", value="").classes("w-full mt-2").props("outlined dense")

        # ============================================================
        # SPACE REQUIREMENT
        # ============================================================
        with ui.card().classes("w-full p-5 mt-4"):
            ui.label("Space Requirement").classes("text-lg font-bold mb-3")

            space_required = ui.input(
                "Space Required",
                value="SHADOW FREE SPACE FOR INSTALLATION OF SOLAR MODULE.",
            ).classes("w-full").props("outlined")

            shadow_free = ui.input(
                "Shadow-Free Requirement",
                value="SHADOW FREE SPACE FOR INSTALLATION OF SOLAR MODULE.",
            ).classes("w-full mt-2").props("outlined")

            site_requirements = ui.input(
                "Other Site Requirements",
                value="",
            ).classes("w-full mt-2").props("outlined")

        # ============================================================
        # 🏦 BANK DETAILS (NEW)
        # ============================================================
        with ui.card().classes("w-full p-5 mt-4 bg-blue-50"):
            ui.label("🏦 Company's Bank Details").classes("text-lg font-bold mb-3 text-blue-900")
            ui.label("These details will appear on the quotation PDF (Page 3)").classes(
                "text-xs text-gray-600 mb-3"
            )

            with ui.row().classes("w-full gap-4 flex-wrap"):
                bank_name_input = ui.input(
                    "Bank Name",
                    value=all_settings.get("bank_name", "SBI BANK"),
                ).classes("flex-1 min-w-[200px]").props("outlined")

                bank_account_input = ui.input(
                    "A/C No.",
                    value=all_settings.get("bank_account_no", ""),
                ).classes("flex-1 min-w-[200px]").props("outlined")

            with ui.row().classes("w-full gap-4 flex-wrap mt-3"):
                bank_branch_input = ui.input(
                    "Branch",
                    value=all_settings.get("bank_branch", "GOVINDGARH"),
                ).classes("flex-1 min-w-[200px]").props("outlined")

                bank_ifsc_input = ui.input(
                    "IFSC Code",
                    value=all_settings.get("bank_ifsc", "SBIN0031042"),
                ).classes("flex-1 min-w-[200px]").props("outlined")

            bank_status = ui.label("").classes("text-sm mt-2")

            def save_bank_details_only():
                updates = [
                    {"key": "bank_name", "value": bank_name_input.value or ""},
                    {"key": "bank_account_no", "value": bank_account_input.value or ""},
                    {"key": "bank_branch", "value": bank_branch_input.value or ""},
                    {"key": "bank_ifsc", "value": bank_ifsc_input.value or ""},
                ]
                resp = api_client.patch("/api/v1/settings/bulk", json={"settings": updates})
                if resp.get("success"):
                    bank_status.set_text("✅ Bank details saved to global settings")
                    bank_status.classes("text-green-600 text-sm font-semibold")
                    ui.notify("Bank details saved ✅", type="positive")
                else:
                    bank_status.set_text("❌ Failed to save bank details")
                    bank_status.classes("text-red-600 text-sm font-semibold")

            ui.button(
                "💾 Save Bank Details (Global)",
                on_click=save_bank_details_only,
            ).classes("bg-blue-500 text-white font-semibold mt-3")

        # ============================================================
        # SUMMARY (Auto-calculated)
        # ============================================================
        summary_container = ui.column().classes("w-full mt-4")

        def update_summary():
            summary_container.clear()

            subtotal = 0
            for it in items_state:
                try:
                    qty = float(it["qty_input"].value) if it.get("qty_input") and it["qty_input"].value else 1
                    price = float(it["price_input"].value) if it.get("price_input") and it["price_input"].value else 0
                    subtotal += qty * price
                except Exception:
                    pass

            disc = float(discount.value or 0)
            gst_amt = (subtotal - disc) * float(gst_pct.value or 18) / 100
            subs_amt = float(subsidy.value or 0)
            final = subtotal - disc + gst_amt - subs_amt

            with summary_container:
                with ui.card().classes("w-full p-5 bg-yellow-50"):
                    ui.label("Summary").classes("text-lg font-bold mb-2")
                    with ui.row().classes("w-full justify-between"):
                        ui.label("Subtotal:")
                        ui.label(f"Rs {subtotal:,.0f}").classes("font-semibold")
                    with ui.row().classes("w-full justify-between"):
                        ui.label("Discount:")
                        ui.label(f"- Rs {disc:,.0f}").classes("font-semibold")
                    with ui.row().classes("w-full justify-between"):
                        ui.label(f"GST ({gst_pct.value}%):")
                        ui.label(f"Rs {gst_amt:,.0f}").classes("font-semibold")
                    with ui.row().classes("w-full justify-between"):
                        ui.label("Subsidy:")
                        ui.label(f"- Rs {subs_amt:,.0f}").classes("font-semibold text-green-600")
                    ui.separator()
                    with ui.row().classes("w-full justify-between text-lg"):
                        ui.label("Final Amount:").classes("font-bold")
                        ui.label(f"Rs {final:,.0f}").classes("font-bold text-green-700")

        ui.button("Refresh Summary", on_click=update_summary).classes("bg-gray-500 text-white mt-3")

        # ============================================================
        # SAVE
        # ============================================================
        result_label = ui.label("").classes("text-sm mt-4")

        def save_pricing():
            items_data = []
            for it in items_state:
                name = it["name_input"].value if it.get("name_input") else it.get("name", "")
                if not name:
                    continue
                items_data.append({
                    "itemName": name,
                    "make": it["make_input"].value if it.get("make_input") else "STANDARD",
                    "capacity": it["capacity_input"].value if it.get("capacity_input") else "-",
                    "quantity": float(it["qty_input"].value) if it.get("qty_input") and it["qty_input"].value else 1,
                    "unit": "pcs",
                    "unitPrice": float(it["price_input"].value) if it.get("price_input") and it["price_input"].value else 0,
                })

            if not items_data:
                result_label.set_text("At least one item is required")
                result_label.classes("text-red-600")
                return

            payload = {
                "items": items_data,
                "discount": float(discount.value or 0),
                "gstPercentage": float(gst_pct.value or 18),
                "subsidyAmount": float(subsidy.value or 0),
                "paymentTerms": f"{int(pay_advance.value or 0)}% advance, {int(pay_delivery.value or 0)}% before delivery, {int(pay_commissioning.value or 0)}% after commissioning",
                "warrantyTerms": warranty_system.value or "",
                "termsConditions": "",
                "validUntilDays": int(validity.value or 30),
                "gstStatus": gst_status.value or "NIL",
                "discomStatus": discom_status.value or "INCLUDED",
                "transportationStatus": transportation_status.value or "INCLUDED",
                "transportationDetails": transportation_details.value or "",
                "officialFees": official_fees.value or "AS APPLICABLE",
                "officialFeesAmount": official_fees_amount.value or "",
                "officialFeesDetails": official_fees_details.value or "",
                "completionDays": completion_days.value or "10-15",
                "completionStart": completion_start.value or "",
                "validityDays": validity_days.value or "2",
                "validityMessage": validity_msg.value or "",
                "warrantySystem": warranty_system.value or "",
                "warrantyModule": warranty_module.value or "",
                "warrantyInverter": warranty_inverter.value or "",
                "warrantyOther": warranty_other.value or "",
                "spaceRequired": space_required.value or "",
                "shadowFree": shadow_free.value or "",
                "siteRequirements": site_requirements.value or "",
                "clientScope": [cs1.value, cs2.value, cs3.value, cs4.value, cs5.value, cs6.value, cs7.value, cs8.value, cs9.value, cs10.value],
            }

            resp = quotation_service.configure_pricing(quotation_id, payload)

            if resp.get("success"):
                result_label.set_text("Pricing saved successfully")
                result_label.classes("text-green-600 font-semibold")
                ui.notify("Pricing configured", type="positive")
                ui.navigate.to(f"/admin/quotation/{quotation_id}")
            else:
                err = resp.get("error", {}).get("message", "Failed")
                result_label.set_text(f"Failed: {err}")
                result_label.classes("text-red-600")

        with ui.row().classes("w-full justify-end gap-3 mt-6"):
            ui.button("Cancel", on_click=lambda: ui.navigate.to(f"/admin/quotation/{quotation_id}")).props("outline")
            ui.button("Save Pricing", on_click=save_pricing).classes("bg-yellow-500 text-white font-semibold px-6 py-3").style("color: white !important;")

        # Initial render
        refresh_items()
        update_summary()