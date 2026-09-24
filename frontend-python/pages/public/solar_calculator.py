"""
NP POWER TECH SOLAR - Solar Calculator
"""

from nicegui import ui
from layouts.public_layout import public_layout


@ui.page("/calculator")
def calculator_page():
    public_layout(current_page="/calculator")

    with ui.column().classes("w-full max-w-4xl mx-auto px-4 py-8 gap-6"):
        ui.label("Solar Calculator").classes("text-4xl font-bold text-gray-900")
        ui.label(
            "Estimate your solar system size and savings. "
            "Results are estimates — final quotation requires site survey."
        ).classes("text-gray-600")

        with ui.card().classes("w-full p-6 gap-4"):
            monthly_bill = ui.number("Monthly Electricity Bill (₹) *", min=0, value=2000).classes("w-full")
            tariff = ui.number("Electricity Tariff (₹/unit)", min=0, value=8.0).classes("w-full")
            roof_area = ui.number("Available Roof Area (sq. ft.)", min=0, value=300).classes("w-full")

            result_container = ui.column().classes("w-full mt-4 gap-2")

            def calculate():
                result_container.clear()
                bill = float(monthly_bill.value or 0)
                t = float(tariff.value or 8)
                area = float(roof_area.value or 0)

                if bill <= 0 or t <= 0:
                    with result_container:
                        ui.label("Please enter valid values.").classes("text-red-600")
                    return

                # Simple estimate logic
                monthly_units = bill / t
                daily_units = monthly_units / 30
                system_size = round(daily_units / 4, 1)  # 4 units per kW per day avg

                # Roof constraint (approx 100 sq ft per kW)
                max_from_roof = round(area / 100, 1)
                final_size = min(system_size, max_from_roof) if area > 0 else system_size

                panels = int(round(final_size * 1000 / 540))  # 540W panels

                # Estimate cost (₹50,000/kW approx)
                cost = final_size * 50000

                # Subsidy estimate (simplified)
                subsidy = 0
                if final_size <= 3:
                    subsidy = final_size * 18000
                elif final_size <= 10:
                    subsidy = 3 * 18000 + (final_size - 3) * 9000

                net_cost = cost - subsidy

                monthly_savings = final_size * 4 * 30 * t
                annual_savings = monthly_savings * 12
                payback_years = round(net_cost / annual_savings, 1) if annual_savings > 0 else 0

                with result_container:
                    ui.label("📊 Estimated Results").classes("text-2xl font-bold text-gray-900 mt-4")
                    ui.separator()

                    with ui.row().classes("w-full justify-between"):
                        ui.label("Recommended System Size:").classes("text-gray-600")
                        ui.label(f"{final_size} kW").classes("font-bold text-green-600")

                    with ui.row().classes("w-full justify-between"):
                        ui.label("Number of Panels (540W):").classes("text-gray-600")
                        ui.label(f"{panels} panels").classes("font-bold")

                    with ui.row().classes("w-full justify-between"):
                        ui.label("Estimated System Cost:").classes("text-gray-600")
                        ui.label(f"₹ {cost:,.0f}").classes("font-bold")

                    with ui.row().classes("w-full justify-between"):
                        ui.label("Estimated Subsidy:").classes("text-gray-600")
                        ui.label(f"₹ {subsidy:,.0f}").classes("font-bold text-blue-600")

                    with ui.row().classes("w-full justify-between"):
                        ui.label("Net Investment:").classes("text-gray-600")
                        ui.label(f"₹ {net_cost:,.0f}").classes("font-bold text-orange-600")

                    with ui.row().classes("w-full justify-between"):
                        ui.label("Estimated Monthly Savings:").classes("text-gray-600")
                        ui.label(f"₹ {monthly_savings:,.0f}").classes("font-bold text-green-600")

                    with ui.row().classes("w-full justify-between"):
                        ui.label("Estimated Annual Savings:").classes("text-gray-600")
                        ui.label(f"₹ {annual_savings:,.0f}").classes("font-bold text-green-600")

                    with ui.row().classes("w-full justify-between"):
                        ui.label("Estimated Payback Period:").classes("text-gray-600")
                        ui.label(f"{payback_years} years").classes("font-bold")

                    ui.separator()
                    ui.label(
                        "⚠️ These are estimates only. Actual values depend on site survey, "
                        "electricity tariff, DISCOM rules, and current subsidy policies."
                    ).classes("text-xs text-gray-500 mt-2")

                    ui.button(
                        "Get Exact Quote",
                        on_click=lambda: ui.navigate.to("/get-quote"),
                    ).classes("bg-yellow-500 text-white mt-4")

            ui.button("Calculate", on_click=calculate).classes(
                "bg-yellow-500 text-white font-semibold px-6 py-3 mt-2"
            )