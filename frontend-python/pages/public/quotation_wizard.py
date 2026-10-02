"""
NP POWER TECH SOLAR - Quotation Wizard (8-Step Customer Form)

Flow:
1. Solar Requirement
2. Customer Info
3. Electricity Info + PRE-CREATE CUSTOMER
4. Bill Upload (with customer_id)
5. Roof Info
6. Roof Photo Upload (with customer_id)
7. Bank Details (optional)
8. Preferences + Submit
"""

from nicegui import ui
from layouts.public_layout import public_layout
from services.quotation_service import quotation_service
from components.upload_widget import upload_widget


@ui.page("/quotation-request")
def quotation_wizard_page():
    public_layout(current_page="/quotation-request")

    # Wizard state
    state = {
        "step": 1,
        "customer_id": None,
        "uploaded_files": {
            "electricity_bills": [],
            "roof_photos": [],
        },
        "data": {
            "solarRequirement": {
                "systemSizeKw": 3,
                "customerType": "residential",
                "systemType": "on-grid",
                "batteryRequired": False,
            },
            "customerInfo": {
                "fullName": "",
                "phone": "",
                "whatsapp": "",
                "email": "",
                "address": "",
                "city": "",
                "state": "",
                "pincode": "",
            },
            "electricityInfo": {
                "discomName": "",
                "monthlyBill": None,
                "monthlyUnits": None,
                "sanctionedLoad": None,
                "connectionType": "",
            },
            "roofInfo": {
                "roofArea": None,
                "roofType": "",
                "buildingType": "",
                "roofOwnership": "",
                "additionalInfo": "",
            },
            "bankDetails": {
                "bankName": "",
                "bankAccountNo": "",
                "bankIfsc": "",
                "bankBranch": "",
            },
            "preferences": {
                "financingRequired": False,
                "notes": "",
            },
        },
    }

    with ui.column().classes("w-full max-w-4xl mx-auto px-4 py-8 gap-6"):
        ui.label("Request a Solar Quotation").classes("text-4xl font-bold text-gray-900")
        ui.label(
            "Fill this 8-step form and our team will prepare a personalized quotation for you."
        ).classes("text-gray-600")

        # Progress indicator (8 steps)
        with ui.row().classes("w-full justify-between items-center gap-1 my-4 flex-wrap"):
            steps = ["Solar", "Contact", "Power", "Bill", "Roof", "Photos", "Bank", "Review"]
            step_labels = []
            for i, name in enumerate(steps, 1):
                with ui.column().classes("items-center gap-1 flex-1 min-w-[60px]"):
                    label = ui.label(str(i)).classes(
                        "w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm"
                    )
                    ui.label(name).classes("text-xs text-gray-600 text-center")
                    step_labels.append(label)

        def update_progress():
            for i, label in enumerate(step_labels, 1):
                if i < state["step"]:
                    label.classes(replace="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm bg-green-500 text-white")
                elif i == state["step"]:
                    label.classes(replace="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm bg-yellow-500 text-white")
                else:
                    label.classes(replace="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm bg-gray-200 text-gray-600")

        content = ui.column().classes("w-full gap-4")
        result_label = ui.label("").classes("text-sm mt-4")

        # ---------- Step 1: Solar Requirement ----------
        def step1():
            content.clear()
            with content:
                ui.label("Step 1: Solar Requirement").classes("text-2xl font-bold")
                state["data"]["solarRequirement"]["systemSizeKw"] = ui.number(
                    "Required System Size (kW) *",
                    value=state["data"]["solarRequirement"]["systemSizeKw"],
                    min=1, max=1000,
                ).classes("w-full")
                state["data"]["solarRequirement"]["customerType"] = ui.select(
                    ["residential", "commercial", "industrial"],
                    value=state["data"]["solarRequirement"]["customerType"],
                    label="Customer Type *",
                ).classes("w-full")
                state["data"]["solarRequirement"]["systemType"] = ui.select(
                    ["on-grid", "off-grid", "hybrid"],
                    value=state["data"]["solarRequirement"]["systemType"],
                    label="System Type *",
                ).classes("w-full")
                state["data"]["solarRequirement"]["batteryRequired"] = ui.checkbox(
                    "Battery Required?",
                    value=state["data"]["solarRequirement"]["batteryRequired"],
                )

        # ---------- Step 2: Customer Info ----------
        def step2():
            content.clear()
            with content:
                ui.label("Step 2: Your Information").classes("text-2xl font-bold")
                state["data"]["customerInfo"]["fullName"] = ui.input(
                    "Full Name *", value=state["data"]["customerInfo"]["fullName"]
                ).classes("w-full")
                state["data"]["customerInfo"]["phone"] = ui.input(
                    "Mobile Number *", value=state["data"]["customerInfo"]["phone"]
                ).classes("w-full")
                state["data"]["customerInfo"]["whatsapp"] = ui.input(
                    "WhatsApp Number", value=state["data"]["customerInfo"]["whatsapp"]
                ).classes("w-full")
                state["data"]["customerInfo"]["email"] = ui.input(
                    "Email", value=state["data"]["customerInfo"]["email"]
                ).classes("w-full")
                state["data"]["customerInfo"]["address"] = ui.textarea(
                    "Installation Address *", value=state["data"]["customerInfo"]["address"]
                ).classes("w-full")
                with ui.row().classes("w-full gap-4"):
                    state["data"]["customerInfo"]["city"] = ui.input(
                        "City *", value=state["data"]["customerInfo"]["city"]
                    ).classes("flex-1")
                    state["data"]["customerInfo"]["state"] = ui.input(
                        "State *", value=state["data"]["customerInfo"]["state"]
                    ).classes("flex-1")
                state["data"]["customerInfo"]["pincode"] = ui.input(
                    "Pincode *", value=state["data"]["customerInfo"]["pincode"]
                ).classes("w-full")

        # ---------- Step 3: Electricity Info ----------
        def step3():
            content.clear()
            with content:
                ui.label("Step 3: Electricity Information").classes("text-2xl font-bold")
                state["data"]["electricityInfo"]["discomName"] = ui.input(
                    "Electricity Provider (DISCOM)",
                    value=state["data"]["electricityInfo"]["discomName"],
                ).classes("w-full")
                state["data"]["electricityInfo"]["monthlyBill"] = ui.number(
                    "Monthly Bill (₹)",
                    value=state["data"]["electricityInfo"]["monthlyBill"] or 0,
                    min=0,
                ).classes("w-full")
                state["data"]["electricityInfo"]["monthlyUnits"] = ui.number(
                    "Monthly Units (kWh)",
                    value=state["data"]["electricityInfo"]["monthlyUnits"] or 0,
                    min=0,
                ).classes("w-full")
                state["data"]["electricityInfo"]["sanctionedLoad"] = ui.number(
                    "Sanctioned Load (kW)",
                    value=state["data"]["electricityInfo"]["sanctionedLoad"] or 0,
                    min=0,
                ).classes("w-full")
                state["data"]["electricityInfo"]["connectionType"] = ui.input(
                    "Connection Type (e.g., Single Phase)",
                    value=state["data"]["electricityInfo"]["connectionType"],
                ).classes("w-full")

        # ---------- Step 4: Bill Upload ----------
        def step4():
            content.clear()
            with content:
                ui.label("Step 4: Upload Electricity Bill").classes("text-2xl font-bold")
                ui.label(
                    "Optional but recommended — helps us prepare an accurate quotation."
                ).classes("text-sm text-gray-500")

                if state.get("customer_id"):
                    ui.label(f"✅ Linked to customer (ID: {state['customer_id'][:8]}...)").classes(
                        "text-xs text-green-600"
                    )

                def on_bill_upload(result):
                    url = result.get("data", {}).get("relativePath", "")
                    if url and url not in state["uploaded_files"]["electricity_bills"]:
                        state["uploaded_files"]["electricity_bills"].append(url)
                    ui.notify("Bill uploaded ✅", type="positive")

                upload_widget(
                    upload_type="electricity_bills",
                    label="📄 Upload Electricity Bill (PDF or Image)",
                    accept="image/*,application/pdf",
                    max_size_mb=10,
                    customer_id=state.get("customer_id"),
                    on_success=on_bill_upload,
                )

        # ---------- Step 5: Roof Info ----------
        def step5():
            content.clear()
            with content:
                ui.label("Step 5: Roof / Site Information").classes("text-2xl font-bold")
                state["data"]["roofInfo"]["roofArea"] = ui.number(
                    "Approximate Roof Area (sq ft)",
                    value=state["data"]["roofInfo"]["roofArea"] or 0,
                    min=0,
                ).classes("w-full")
                state["data"]["roofInfo"]["roofType"] = ui.select(
                    ["RCC", "Metal Sheet", "Tiled", "Other"],
                    value=state["data"]["roofInfo"]["roofType"] or "RCC",
                    label="Roof Type",
                ).classes("w-full")
                state["data"]["roofInfo"]["buildingType"] = ui.select(
                    ["Independent House", "Apartment", "Commercial Building", "Factory"],
                    value=state["data"]["roofInfo"]["buildingType"] or "Independent House",
                    label="Building Type",
                ).classes("w-full")
                state["data"]["roofInfo"]["roofOwnership"] = ui.select(
                    ["Owned", "Rented", "Leased"],
                    value=state["data"]["roofInfo"]["roofOwnership"] or "Owned",
                    label="Roof Ownership",
                ).classes("w-full")
                state["data"]["roofInfo"]["additionalInfo"] = ui.textarea(
                    "Additional Site Information",
                    value=state["data"]["roofInfo"]["additionalInfo"],
                ).classes("w-full")

        # ---------- Step 6: Roof Photo Upload ----------
        def step6():
            content.clear()
            with content:
                ui.label("Step 6: Upload Roof / Site Photos").classes("text-2xl font-bold")
                ui.label(
                    "Upload 1-3 photos of your roof/site. This helps us design the right system."
                ).classes("text-sm text-gray-500")

                if state.get("customer_id"):
                    ui.label(f"✅ Linked to customer (ID: {state['customer_id'][:8]}...)").classes(
                        "text-xs text-green-600"
                    )

                def on_photo_upload(result):
                    url = result.get("data", {}).get("relativePath", "")
                    if url and url not in state["uploaded_files"]["roof_photos"]:
                        state["uploaded_files"]["roof_photos"].append(url)
                    ui.notify("Photo uploaded ✅", type="positive")

                upload_widget(
                    upload_type="roof_photos",
                    label="🏠 Upload Roof / Site Photo",
                    accept="image/*",
                    max_size_mb=10,
                    customer_id=state.get("customer_id"),
                    on_success=on_photo_upload,
                )

                ui.label("You can upload multiple photos one by one.").classes(
                    "text-xs text-gray-400 mt-2"
                )

        # ---------- Step 7: Bank Details (optional) ----------
        def step7():
            content.clear()
            with content:
                ui.label("Step 7: Bank Details (Optional)").classes("text-2xl font-bold")
                ui.label(
                    "Ye details PDF quotation mein dikhengi. Agar aap skip karte ho, toh "
                    "company ki default bank details use hongi."
                ).classes("text-sm text-gray-500")

                state["data"]["bankDetails"]["bankName"] = ui.input(
                    "Bank Name (e.g., SBI, HDFC)",
                    value=state["data"]["bankDetails"]["bankName"],
                    placeholder="SBI BANK",
                ).classes("w-full").props("outlined")
                state["data"]["bankDetails"]["bankAccountNo"] = ui.input(
                    "Account Number",
                    value=state["data"]["bankDetails"]["bankAccountNo"],
                    placeholder="44941015635",
                ).classes("w-full").props("outlined")
                state["data"]["bankDetails"]["bankIfsc"] = ui.input(
                    "IFSC Code",
                    value=state["data"]["bankDetails"]["bankIfsc"],
                    placeholder="SBIN0031042",
                ).classes("w-full").props("outlined")
                state["data"]["bankDetails"]["bankBranch"] = ui.input(
                    "Branch Name",
                    value=state["data"]["bankDetails"]["bankBranch"],
                    placeholder="GOVINDGARH",
                ).classes("w-full").props("outlined")

                with ui.card().classes("w-full p-4 bg-yellow-50 mt-3"):
                    ui.label("ℹ️  Note").classes("text-sm font-bold text-yellow-800")
                    ui.label(
                        "Ye optional hai. Agar aap apni bank details daalenge, toh PDF mein "
                        "aapki details dikhengi (payment ke liye). Warna company ki default bank details use hongi."
                    ).classes("text-xs text-gray-700")

        # ---------- Step 8: Preferences + Submit ----------
        def step8():
            content.clear()
            with content:
                ui.label("Step 8: Final Details").classes("text-2xl font-bold")
                state["data"]["preferences"]["financingRequired"] = ui.checkbox(
                    "Do you need financing/loan assistance?",
                    value=state["data"]["preferences"]["financingRequired"],
                )
                state["data"]["preferences"]["notes"] = ui.textarea(
                    "Additional Notes / Requirements",
                    value=state["data"]["preferences"]["notes"],
                ).classes("w-full")

                ui.separator()
                ui.label("Summary").classes("text-xl font-bold mt-4")

                sol = state["data"]["solarRequirement"]
                ci = state["data"]["customerInfo"]
                bd = state["data"]["bankDetails"]

                with ui.column().classes("gap-1"):
                    ui.label(f"• System Size: {sol['systemSizeKw'].value} kW")
                    ui.label(f"• Type: {sol['customerType'].value} / {sol['systemType'].value}")
                    ui.label(f"• Battery: {'Yes' if sol['batteryRequired'].value else 'No'}")
                    ui.label(f"• Name: {ci['fullName'].value}")
                    ui.label(f"• Phone: {ci['phone'].value}")
                    ui.label(f"• City: {ci['city'].value}")
                    ui.label(f"• Bill uploaded: {len(state['uploaded_files']['electricity_bills'])} file(s)")
                    ui.label(f"• Roof photos: {len(state['uploaded_files']['roof_photos'])} file(s)")
                    bank_info = bd["bankName"].value or "Company default"
                    ui.label(f"• Bank: {bank_info}")
                    if state.get("customer_id"):
                        ui.label(f"• Customer ID: {state['customer_id']}").classes("text-xs text-green-600")

        # ---------- Navigation ----------
        def go_next():
            if state["step"] == 1:
                step2()
                state["step"] = 2
            elif state["step"] == 2:
                ci = state["data"]["customerInfo"]
                if not ci["fullName"].value or not ci["phone"].value or not ci["address"].value:
                    result_label.set_text("Please fill name, phone, and address.")
                    result_label.classes("text-red-600")
                    return
                step3()
                state["step"] = 3
            elif state["step"] == 3:
                # PRE-CREATE CUSTOMER before uploads
                ci = state["data"]["customerInfo"]
                if not state["customer_id"]:
                    pre_resp = quotation_service.pre_create_customer({
                        "fullName": ci["fullName"].value,
                        "phone": ci["phone"].value,
                        "email": ci["email"].value or None,
                        "address": ci["address"].value,
                        "city": ci["city"].value,
                        "state": ci["state"].value,
                        "pincode": ci["pincode"].value,
                        "customerType": state["data"]["solarRequirement"]["customerType"].value,
                    })
                    if pre_resp.get("success"):
                        # FIX: Backend returns data.customer.id
                        customer_data = pre_resp.get("data", {}).get("customer", {})
                        state["customer_id"] = customer_data.get("id")
                        print(f"[WIZARD] Customer pre-created: {state['customer_id']}")
                    else:
                        err_msg = pre_resp.get("error", {}).get("message", "Unknown error")
                        print(f"[WIZARD] Pre-create failed: {err_msg}")
                        result_label.set_text(f"⚠️ Customer creation failed: {err_msg}")
                        result_label.classes("text-yellow-600")
                step4()
                state["step"] = 4
            elif state["step"] == 4:
                step5()
                state["step"] = 5
            elif state["step"] == 5:
                step6()
                state["step"] = 6
            elif state["step"] == 6:
                step7()
                state["step"] = 7
            elif state["step"] == 7:
                step8()
                state["step"] = 8
            result_label.set_text("")
            update_progress()

        def go_back():
            if state["step"] == 2:
                step1(); state["step"] = 1
            elif state["step"] == 3:
                step2(); state["step"] = 2
            elif state["step"] == 4:
                step3(); state["step"] = 3
            elif state["step"] == 5:
                step4(); state["step"] = 4
            elif state["step"] == 6:
                step5(); state["step"] = 5
            elif state["step"] == 7:
                step6(); state["step"] = 6
            elif state["step"] == 8:
                step7(); state["step"] = 7
            result_label.set_text("")
            update_progress()

        def submit():
            sol = state["data"]["solarRequirement"]
            ci = state["data"]["customerInfo"]
            ei = state["data"]["electricityInfo"]
            ri = state["data"]["roofInfo"]
            bd = state["data"]["bankDetails"]
            pr = state["data"]["preferences"]

            payload = {
                "solarRequirement": {
                    "systemSizeKw": float(sol["systemSizeKw"].value or 0),
                    "customerType": sol["customerType"].value,
                    "systemType": sol["systemType"].value,
                    "batteryRequired": bool(sol["batteryRequired"].value),
                },
                "customerInfo": {
                    "fullName": ci["fullName"].value,
                    "phone": ci["phone"].value,
                    "whatsapp": ci["whatsapp"].value or None,
                    "email": ci["email"].value or None,
                    "address": ci["address"].value,
                    "city": ci["city"].value,
                    "state": ci["state"].value,
                    "pincode": ci["pincode"].value,
                },
                "electricityInfo": {
                    "discomName": ei["discomName"].value or None,
                    "monthlyBill": float(ei["monthlyBill"].value) if ei["monthlyBill"].value else None,
                    "monthlyUnits": int(ei["monthlyUnits"].value) if ei["monthlyUnits"].value else None,
                    "sanctionedLoad": float(ei["sanctionedLoad"].value) if ei["sanctionedLoad"].value else None,
                    "connectionType": ei["connectionType"].value or None,
                },
                "roofInfo": {
                    "roofArea": float(ri["roofArea"].value) if ri["roofArea"].value else None,
                    "roofType": ri["roofType"].value,
                    "buildingType": ri["buildingType"].value,
                    "roofOwnership": ri["roofOwnership"].value,
                    "additionalInfo": ri["additionalInfo"].value or None,
                },
                "bankDetails": {
                    "bankName": bd["bankName"].value or None,
                    "bankAccountNo": bd["bankAccountNo"].value or None,
                    "bankIfsc": bd["bankIfsc"].value or None,
                    "bankBranch": bd["bankBranch"].value or None,
                },
                "preferences": {
                    "financingRequired": bool(pr["financingRequired"].value),
                    "notes": pr["notes"].value or None,
                },
            }

            resp = quotation_service.create_request(payload)

            if resp.get("success"):
                qnum = resp.get("data", {}).get("quotation_number", "")
                qid = resp.get("data", {}).get("id", "")
                result_label.set_text(f"✅ Submitted! Reference: {qnum}")
                result_label.classes("text-green-600 font-semibold")
                ui.navigate.to(f"/quotation-status/{qid}")
            else:
                err = resp.get("error", {}).get("message", "Try again.")
                result_label.set_text(f"❌ {err}")
                result_label.classes("text-red-600")

        with ui.row().classes("w-full gap-3 mt-4"):
            ui.button("← Back", on_click=go_back).props("outline")
            ui.button("Next →", on_click=go_next).classes("bg-yellow-500 text-white")
            ui.button("Submit", on_click=submit).classes("bg-green-500 text-white")

        # Initial render
        step1()
        update_progress()