"""
NP POWER TECH SOLAR - Admin Settings
Manage website content and company information.
"""

from nicegui import ui, app
from layouts.admin_layout import admin_layout
from api.client import api_client


@ui.page("/admin/settings")
def admin_settings():
    token = app.storage.user.get("access_token")
    if not token:
        ui.navigate.to("/login")
        return
    api_client.set_token(token)

    container = admin_layout(current_page="/admin/settings", page_title="Website Settings")

    with container:
        ui.label("Website Settings").classes("text-2xl font-bold")
        ui.label("Manage company info, contact details, and website content").classes(
            "text-sm text-gray-500"
        )

        loading = ui.label("Loading settings...").classes("text-gray-500")
        settings_container = ui.column().classes("w-full gap-4")

        inputs = {}

        def load_settings():
            settings_container.clear()
            inputs.clear()

            resp = api_client.get("/api/v1/settings")

            if not resp.get("success"):
                loading.set_text("❌ Failed to load settings. Please re-login.")
                loading.classes("text-red-600")
                return

            settings = resp.get("data", [])
            loading.set_text(f"✅ {len(settings)} settings loaded")
            loading.classes("text-green-600 text-sm")

            # Group by category
            grouped = {}
            for s in settings:
                cat = s.get("category") or "general"
                if cat not in grouped:
                    grouped[cat] = []
                grouped[cat].append(s)

            with settings_container:
                for category in sorted(grouped.keys()):
                    items = grouped[category]
                    with ui.card().classes("w-full p-5"):
                        ui.label(f"📁 {category.replace('_', ' ').title()}").classes(
                            "text-lg font-bold mb-3 text-yellow-700"
                        )

                        for s in items:
                            key = s["key"]
                            value = s["value"] or ""
                            desc = s.get("description") or key
                            vtype = s.get("value_type", "string")

                            with ui.row().classes("w-full items-center gap-3"):
                                with ui.column().classes("w-72 gap-0"):
                                    ui.label(key).classes("text-sm font-semibold text-gray-700")
                                    ui.label(desc).classes("text-xs text-gray-400")

                                # Different input based on type
                                if vtype == "boolean":
                                    is_true = str(value).lower() == "true"
                                    inputs[key] = ui.checkbox("Enabled", value=is_true).classes("flex-1")
                                elif vtype == "number":
                                    try:
                                        num = float(value) if value else 0
                                    except Exception:
                                        num = 0
                                    inputs[key] = ui.number(value=num).classes("flex-1").props("outlined dense")
                                else:
                                    inputs[key] = ui.input(value=value).classes("flex-1").props("outlined dense")

                # Save button
                def save_all():
                    updates = []
                    for key, inp in inputs.items():
                        val = inp.value
                        if isinstance(val, bool):
                            val = "true" if val else "false"
                        elif val is None:
                            val = ""
                        else:
                            val = str(val)
                        updates.append({"key": key, "value": val})

                    resp = api_client.patch("/api/v1/settings/bulk", json={"settings": updates})

                    if resp.get("success"):
                        ui.notify(f"✅ {len(updates)} settings updated", type="positive")
                    else:
                        err = resp.get("error", {}).get("message", "Failed")
                        ui.notify(f"❌ {err}", type="negative")

                with ui.row().classes("w-full justify-end mt-4"):
                    ui.button(
                        "💾 Save All Settings",
                        on_click=save_all,
                    ).classes("bg-yellow-500 text-white font-semibold px-6 py-3")

        ui.timer(0.3, load_settings, once=True)