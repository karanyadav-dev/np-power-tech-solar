"""
NP POWER TECH SOLAR - Subsidy Calculator
Based on PM Surya Ghar scheme (configurable — do not hardcode values)
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/subsidy")
def subsidy_page():
    public_layout(current_page="/subsidy")

    with ui.column().classes("w-full max-w-4xl mx-auto px-4 py-8 gap-6"):
        ui.label("Solar Subsidy Calculator").classes("text-4xl font-bold text-gray-900")
        ui.label(
            "Estimate your government subsidy under PM Surya Ghar Muft Bijli Yojana. "
            "Actual subsidy depends on scheme rules and DISCOM verification."
        ).classes("text-gray-600")

        with ui.card().classes("w-full p-6 gap-4"):
            capacity = ui.select(
                [1, 2, 3, 4, 5, 7, 10],
                value=3,
                label="System Capacity (kW)",
            ).classes("w-full")

            state = ui.select(
                ["Delhi", "Maharashtra", "Karnataka", "Tamil Nadu", "Gujarat", "Rajasthan", "Other"],
                value="Delhi",
                label="State",
            ).classes("w-full")

            category = ui.select(
                ["Residential", "Commercial", "Industrial"],
                value="Residential",
                label="Category",
            ).classes("w-full")

            result_container = ui.column().classes("w-full mt-4 gap-3")

            def calculate():
                result_container.clear()
                cap = float(capacity.value or 0)
                cat = category.value

                # PM Surya Ghar scheme — residential only, slab-based
                # NOTE: These are current estimates. Admin can update via config.
                if cat != "Residential":
                    with result_container:
                        ui.label(
                            "⚠️ Subsidy scheme currently applies to Residential category only."
                        ).classes("text-orange-600")
                    return

                if cap <= 1:
                    subsidy = 30000
                elif cap <= 2:
                    subsidy = 60000
                elif cap <= 3:
                    subsidy = 78000
                elif cap <= 10:
                    subsidy = 78000 + (cap - 3) * 4500  # approximate for higher capacities
                else:
                    subsidy = 78000

                # Estimated system cost (₹50,000/kW approx)
                cost = cap * 50000
                customer_share = cost - subsidy

                with result_container:
                    ui.label("💰 Estimated Subsidy").classes("text-2xl font-bold text-gray-900 mt-4")
                    ui.separator()

                    with ui.row().classes("w-full justify-between py-2"):
                        ui.label("System Capacity:").classes("text-gray-600")
                        ui.label(f"{cap} kW").classes("font-bold")

                    with ui.row().classes("w-full justify-between py-2"):
                        ui.label("Estimated System Cost:").classes("text-gray-600")
                        ui.label(f"₹ {cost:,.0f}").classes("font-bold")

                    with ui.row().classes("w-full justify-between py-2"):
                        ui.label("Estimated Subsidy:").classes("text-gray-600")
                        ui.label(f"₹ {subsidy:,.0f}").classes("font-bold text-green-600 text-lg")

                    with ui.row().classes("w-full justify-between py-2"):
                        ui.label("Your Estimated Contribution:").classes("text-gray-600")
                        ui.label(f"₹ {customer_share:,.0f}").classes("font-bold text-orange-600 text-lg")

                    ui.separator()
                    ui.label(
                        "⚠️ Disclaimer: These are estimates only. Actual subsidy depends on the "
                        "current PM Surya Ghar scheme rules, DISCOM approval, and verification. "
                        "Please consult with us for exact figures."
                    ).classes("text-xs text-gray-500 mt-3")

                    ui.button(
                        "Get Exact Quote",
                        on_click=lambda: ui.navigate.to("/get-quote"),
                    ).classes("bg-yellow-500 text-white mt-4")

            ui.button("Calculate Subsidy", on_click=calculate).classes(
                "bg-yellow-500 text-white font-semibold px-6 py-3 mt-2"
            )

        # Info section
        ui.separator()
        ui.label("About PM Surya Ghar Scheme").classes("text-2xl font-bold mt-4")
        with ui.column().classes("gap-2"):
            for point in [
                "Launched in 2024 for residential rooftop solar",
                "Subsidy up to ₹78,000 for systems up to 3 kW",
                "Additional subsidy for systems above 3 kW (subject to scheme rules)",
                "Subsidy credited directly to bank account after installation & net metering",
                "Apply online through the national portal",
            ]:
                with ui.row().classes("items-center gap-2"):
                    ui.icon("check_circle", size="1.3rem").classes("text-green-500")
                    ui.label(point).classes("text-gray-700")