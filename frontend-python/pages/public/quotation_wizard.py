"""
NP POWER TECH SOLAR - Quotation Wizard (5-Step Customer Form)
"""

from nicegui import ui
from layouts.public_layout import public_layout
from services.quotation_service import quotation_service


@ui.page("/quotation-request")
def quotation_wizard_page():
    public_layout(current_page="/quotation-request")

    # Wizard state
    state = {
        "step": 1,
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
            "preferences": {
                "financingRequired": False,
                "notes": "",
            },
        },
    }

    with ui.column().classes("w-full max-w-4xl mx-auto px-4 py-8 gap-6"):
        ui.label("Request a Solar Quotation").classes("text-4xl font-bold text-gray-900")
        ui.label(
            "Fill this 5-step form and our team will prepare a personalized quotation for you."
        ).classes("text-gray-600")

        # Progress indicator
        with ui.row().classes("w-full justify-between items-center gap-2 my-4"):
            steps = ["Solar", "Contact", "Electricity", "Roof", "Preferences"]
            step_labels = []
            for i, name in enumerate(steps, 1):
                with ui.column().classes("items-center gap-1 flex-1"):
                    label = ui.label(str(i)).classes(
                        "w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm"
                    )
                    ui.label(name).classes("text-xs text-gray-600")
                    step_labels.append(label)

        def update_progress():
            for i, label in enumerate(step_labels, 1):
                if i < state["step"]:
                    label.classes(replace="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm bg-green-500 text-white")
                elif i == state["step"]:
                    label.classes(replace="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm bg-yellow-500 text-white")
                else:
                    label.classes(replace="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm bg-gray-200 text-gray-600")

        # Content area
        content = ui.column().classes("w-full gap-4")

        # ---- Step 1: Solar Requirement ----
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

        # ---- Step 2: Customer Info ----
        def step2():
            content.clear()
            with content:
                ui.label("Step 2: Your Information").classes("text-2xl font-bold")
                state["data"]["customerInfo"]["fullName"] = ui.input("Full Name *").classes("w-full")
                state["data"]["customerInfo"]["phone"] = ui.input("Mobile Number *").classes("w-full")
                state["data"]["customerInfo"]["whatsapp"] = ui.input("WhatsApp Number").classes("w-full")
                state["data"]["customerInfo"]["email"] = ui.input("Email").classes("w-full")
                state["data"]["customerInfo"]["address"] = ui.textarea("Installation Address *").classes("w-full")
                with ui.row().classes("w-full gap-4"):
                    state["data"]["customerInfo"]["city"] = ui.input("City *").classes("flex-1")
                    state["data"]["customerInfo"]["state"] = ui.input("State *").classes("flex-1")
                state["data"]["customerInfo"]["pincode"] = ui.input("Pincode *").classes("w-full")

        # ---- Step 3: Electricity Info ----
        def step3():
            content.clear()
            with content:
                ui.label("Step 3: Electricity Information").classes("text-2xl font-bold")
                state["data"]["electricityInfo"]["discomName"] = ui.input(
                    "Electricity Provider (DISCOM)"
                ).classes("w-full")
                state["data"]["electricityInfo"]["monthlyBill"] = ui.number(
                    "Monthly Bill (₹)", min=0
                ).classes("w-full")
                state["data"]["electricityInfo"]["monthlyUnits"] = ui.number(
                    "Monthly Units (kWh)", min=0
                ).classes("w-full")
                state["data"]["electricityInfo"]["sanctionedLoad"] = ui.number(
                    "Sanctioned Load (kW)", min=0
                ).classes("w-full")
                state["data"]["electricityInfo"]["connectionType"] = ui.input(
                    "Connection Type (e.g., Single Phase)"
                ).classes("w-full")
                ui.label("You can upload your electricity bill later (via WhatsApp/email).").classes(
                    "text-xs text-gray-500"
                )

        # ---- Step 4: Roof Info ----
        def step4():
            content.clear()
            with content:
                ui.label("Step 4: Roof / Site Information").classes("text-2xl font-bold")
                state["data"]["roofInfo"]["roofArea"] = ui.number(
                    "Approximate Roof Area (sq ft)", min=0
                ).classes("w-full")
                state["data"]["roofInfo"]["roofType"] = ui.select(
                    ["RCC", "Metal Sheet", "Tiled", "Other"],
                    value="RCC",
                    label="Roof Type",
                ).classes("w-full")
                state["data"]["roofInfo"]["buildingType"] = ui.select(
                    ["Independent House", "Apartment", "Commercial Building", "Factory"],
                    value="Independent House",
                    label="Building Type",
                ).classes("w-full")
                state["data"]["roofInfo"]["roofOwnership"] = ui.select(
                    ["Owned", "Rented", "Leased"],
                    value="Owned",
                    label="Roof Ownership",
                ).classes("w-full")
                state["data"]["roofInfo"]["additionalInfo"] = ui.textarea(
                    "Additional Site Information"
                ).classes("w-full")
                ui.label("Roof photos can be shared later (via WhatsApp/email).").classes(
                    "text-xs text-gray-500"
                )

        # ---- Step 5: Preferences ----
        def step5():
            content.clear()
            with content:
                ui.label("Step 5: Your Preferences").classes("text-2xl font-bold")
                state["data"]["preferences"]["financingRequired"] = ui.checkbox(
                    "Do you need financing/loan assistance?"
                )
                state["data"]["preferences"]["notes"] = ui.textarea(
                    "Additional Notes / Requirements"
                ).classes("w-full")

                ui.separator()
                ui.label("Summary").classes("text-xl font-bold mt-4")
                with ui.column().classes("gap-1"):
                    sol = state["data"]["solarRequirement"]
                    ui.label(f"• System Size: {sol['systemSizeKw'].value} kW")
                    ui.label(f"• Type: {sol['customerType'].value} / {sol['systemType'].value}")
                    ui.label(f"• Battery: {'Yes' if sol['batteryRequired'].value else 'No'}")

        # ---- Navigation Buttons ----
        result_label = ui.label("").classes("text-sm mt-4")

        def go_next():
            if state["step"] == 1:
                step2()
                state["step"] = 2
            elif state["step"] == 2:
                # Validate customer info
                ci = state["data"]["customerInfo"]
                if not ci["fullName"].value or not ci["phone"].value:
                    result_label.set_text("Please fill name and phone.")
                    result_label.classes("text-red-600")
                    return
                step3()
                state["step"] = 3
            elif state["step"] == 3:
                step4()
                state["step"] = 4
            elif state["step"] == 4:
                step5()
                state["step"] = 5
            result_label.set_text("")
            update_progress()

        def go_back():
            if state["step"] == 2:
                step1()
                state["step"] = 1
            elif state["step"] == 3:
                step2()
                state["step"] = 2
            elif state["step"] == 4:
                step3()
                state["step"] = 3
            elif state["step"] == 5:
                step4()
                state["step"] = 4
            result_label.set_text("")
            update_progress()

        def submit():
            # Build payload
            sol = state["data"]["solarRequirement"]
            ci = state["data"]["customerInfo"]
            ei = state["data"]["electricityInfo"]
            ri = state["data"]["roofInfo"]
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
                "preferences": {
                    "financingRequired": bool(pr["financingRequired"].value),
                    "notes": pr["notes"].value or None,
                },
            }

            resp = quotation_service.create_request(payload)

            if resp.get("success"):
                qnum = resp.get("data", {}).get("quotation_number", "")
                qid = resp.get("data", {}).get("id", "")
                result_label.set_text(
                    f"✅ Quotation request submitted! Reference: {qnum}. "
                    f"Save this for your records: {qid}"
                )
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

        # Init
        step1()
        update_progress()